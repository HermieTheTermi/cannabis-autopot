#!/usr/bin/env python3
"""Leiterbahnbreiten-Spezifikation fuer die PCB-Phase (SmartGrowTopf V1).

Rechnet die noetigen Mindestbreiten aus der Netzliste + den Stroemen der
Datenblaetter nach IPC-2221A (aussen, 1 oz Kupfer = 35 um, dT = 10 K) und
prueft zusaetzlich den Spannungsabfall auf dem langen Pumpen-/Akkupfad.

Quellen der Stroeme:
  * Pumpe OEM ABC-12527 (anodas.lt): "Current: 3V - 400mA, 6V - 540mA"
  * Lader MCP73831T (R_PROG 3,9k): ~256 mA, Chip-Maximum 500 mA
  * LDO ME6211C33: 500 mA Ausgang (ESP32-C6 TX-Spitze 382 mA, Espressif Tab. 6-4)
  * Zelle EFASO 503759, 1S, 3,0-4,2 V, 1500 mAh

Ergebnis: hardware/easyeda/netclass_spec.json (maschinenlesbar, PCB-Phase liest das)
"""
import json, math, os

# --- Prozess / Material -----------------------------------------------------
OZ = 1.0                    # Kupferdicke aussen bei JLCPCB Standard
THICK_MIL = 1.378 * OZ      # 1 oz = 1,378 mil = 35 um
K_OUTER = 0.048             # IPC-2221A, aussen
K_INNER = 0.024             # IPC-2221A, innen (nur zur Info)
DT = 10.0                   # zulaessige Erwaermung in K
RHO20 = 1.72e-8             # Kupfer, Ohm*m
ALPHA = 0.00393             # 1/K
T_OP = 70.0                 # angenommene Leiterbahntemperatur fuer IR-Drop

# --- Stroeme (aus den Datenblaettern, s. Kopf) ------------------------------
I_PUMP_NOM = 0.54           # Pumpe @6 V (Datenblatt-Worstcase); an 1S real ~0.45 A
I_PUMP_CELL = 0.45          # Pumpe an 4,2-V-Zelle
I_PUMP_INRUSH = 1.50        # Motor-Anlauf (Datenblatt schweigt -> 2,8x Nennstrom)
I_LDO = 0.50                # ME6211 Maximalstrom
I_TX = 0.382                # ESP32-C6 WLAN-TX-Spitze
I_CHG = 0.256               # MCP73831 mit R_PROG 3,9k
I_VBAT_WORST = I_PUMP_NOM + I_LDO      # Pumpe + MCU-Versorgung gleichzeitig
I_VBAT_ALL = I_PUMP_NOM + I_LDO + I_CHG  # zusaetzlich laden (Firmware verbietet das)

def width_mm(I, dt=DT, k=K_OUTER):
    """IPC-2221A: A[mil^2] = (I/(k*dT^0.44))^(1/0.725); Breite = A/Dicke."""
    A = (I / (k * dt ** 0.44)) ** (1 / 0.725)
    return A / THICK_MIL * 0.0254

def ampacity(w_mm, dt=DT, k=K_OUTER):
    """Umkehrung: wieviel Strom traegt diese Breite bei dT?"""
    A = (w_mm / 0.0254) * THICK_MIL
    return k * dt ** 0.44 * A ** 0.725

def drop_mv(w_mm, I, L_mm, t_op=T_OP):
    rho = RHO20 * (1 + ALPHA * (t_op - 20))
    R = rho * (L_mm / 1000) / ((w_mm / 1000) * (THICK_MIL * 25.4e-6))
    return R * I * 1000, R * 1000

# --- Netze: Rolle -> Breite -------------------------------------------------
# Rollen wie im easyeda-agent-Netklassen-Modell (pcb_netclass.go):
# signal / power-branch / power-trunk / high-current / gnd
W_SIGNAL, W_BRANCH, W_TRUNK, W_HIGH = 0.25, 0.25, 0.40, 0.50   # mm

NETS = {
    # Netz        Rolle          Soll   min   Strom(A)  Lage          Zweck
    "VBAT":       ("high-current", W_HIGH, 0.40, I_VBAT_ALL, "TOP", "Akku + -> Lader, LDO, Waechter, Pumpenzweig"),
    "PUMP_N":     ("high-current", W_HIGH, 0.40, I_PUMP_NOM, "TOP", "Q1 Drain -> J4 Pumpe- (geschalteter Rueckweg)"),
    "VBUS":       ("high-current", W_HIGH, 0.40, 0.50, "TOP", "USB-C 5 V -> Ladereingang (max 500 mA)"),
    "+3V3":       ("power-branch", W_TRUNK, 0.25, I_LDO, "TOP", "LDO-Ausgang -> Modul (TX-Spitze 382 mA)"),
    "GND":        ("gnd",          None,    None, I_VBAT_ALL, "BOTTOM", "Masseflaeche unten + kurze Stiche"),
    "PUMP_EN":    ("signal",       W_SIGNAL, 0.15, 0.01, "TOP", "GPIO2 -> R1 Gate-Serie (PWM)"),
    "GATE":       ("signal",       W_SIGNAL, 0.15, 0.01, "TOP", "Gate-Knoten Q1"),
    "RESET_UV":   ("signal",       W_SIGNAL, 0.15, 0.01, "TOP", "MAX809 RESET -> D3"),
    "SENSOR_RAW": ("signal",       W_SIGNAL, 0.15, 0.01, "TOP", "Sensor-AOUT"),
    "SENSOR_AOUT":("signal",       W_SIGNAL, 0.15, 0.01, "TOP", "ADC1_CH0, 100 nF Filter"),
    "SENSOR_PWR": ("signal",       W_SIGNAL, 0.15, 0.02, "TOP", "Sensor-VCC geschaltet"),
    "LIGHT_RAW":  ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "Lichtsensor-Ausgang J7 (R_LIGHT 10k nach GND)"),
    "LIGHT_AOUT": ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "ADC1_CH4 (IO4), 100 nF Filter"),
    "VBAT_SENSE": ("signal",       W_SIGNAL, 0.15, 0.00002, "TOP", "ADC1_CH1, 200k-Teiler"),
    "USB_DP":     ("diff-pair",    W_SIGNAL, 0.15, 0.01, "TOP", "USB D+ (Full Speed), paarweise + laengengleich"),
    "USB_DM":     ("diff-pair",    W_SIGNAL, 0.15, 0.01, "TOP", "USB D- (Full Speed), paarweise + laengengleich"),
    "LED_STAT":   ("signal",       W_SIGNAL, 0.15, 0.003, "TOP", "Status-LED"),
    "LED_TANK":   ("signal",       W_SIGNAL, 0.15, 0.003, "TOP", "Tank-leer-LED"),
    "STAT_CHG":   ("signal",       W_SIGNAL, 0.15, 0.005, "TOP", "Lade-Status"),
    "PROG":       ("signal",       W_SIGNAL, 0.15, 0.0002, "TOP", "Ladestrom-Programmierung"),
    "CC1":        ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "USB-C 5,1k"),
    "CC2":        ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "USB-C 5,1k"),
    "EN":         ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "RC-Glied Reset"),
    "BOOT":       ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "GPIO9 Strapping"),
    "GPIO8_STRAP":("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "GPIO8 Strapping"),
    "BTN":        ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "Taster + Entprellung"),
    "UART_TX":    ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "TXD0 (DNP)"),
    "UART_RX":    ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "RXD0 (DNP)"),
    "UART_TP":    ("signal",       W_SIGNAL, 0.15, 0.001, "TOP", "Testpad TXD0"),
    "LED_CHG":    ("signal",       W_SIGNAL, 0.15, 0.005, "TOP", "Lade-LED"),
    "LED_STAT_A": ("signal",       W_SIGNAL, 0.15, 0.003, "TOP", "LED-Anode"),
    "LED_TANK_A": ("signal",       W_SIGNAL, 0.15, 0.003, "TOP", "LED-Anode"),
}

FAB = {
    "fab": "JLCPCB", "layers": 2, "copper_oz_outer": OZ,
    "min_trace_mm": 0.127, "min_spacing_mm": 0.127,
    "min_via_drill_mm": 0.30, "min_via_pad_mm": 0.60,
    "controlled_impedance": False,
    "hinweis": "2 Lagen 1 oz: 5 mil (0,127 mm) ist das Minimum ohne Aufpreis; "
               "2 oz gibt es erst ab 8 mil (0,2 mm) und kostet extra.",
}

def build():
    nets = {}
    for name, (role, target, wmin, I, layer, why) in NETS.items():
        entry = {
            "role": role, "width_mm": target, "width_mil": round(target / 0.0254, 1) if target else None,
            "min_width_mm": wmin, "layer": layer, "current_a": I,
            "ampacity_a_at_10k": round(ampacity(target), 2) if target else None,
            "dt_k_at_current": round(DT * (I / ampacity(target)) ** (1 / 0.44), 2) if target else None,
            "purpose": why,
        }
        if target and I:
            d, R = drop_mv(target, I, 40.0)
            entry["drop_mv_at_40mm"] = round(d, 1)
            entry["resistance_mohm_at_40mm"] = round(R, 1)
        nets[name] = entry
    return {
        "project": "SmartGrowTopf_V1",
        "stand": "2026-09-14",
        "basis": "IPC-2221A (aussen), dT = 10 K, 1 oz Kupfer, 2 Lagen",
        "formula": "A[mil^2] = (I / (k * dT^0.44))^(1/0.725), k=0.048 aussen; Breite = A / 1,378 mil",
        "inputs_a": {
            "pumpe_nenn_6v": I_PUMP_NOM, "pumpe_an_zelle_4v2": I_PUMP_CELL,
            "pumpe_anlauf_angenommen": I_PUMP_INRUSH, "ldo_max": I_LDO,
            "esp32c6_tx_peak": I_TX, "lader_programmiert": I_CHG,
            "vbat_gleichzeitig_pumpe_und_mcu": round(I_VBAT_WORST, 3),
            "vbat_inkl_laden_firmware_verbietet": round(I_VBAT_ALL, 3),
        },
        "fab": FAB,
        "nets": nets,
        "mindestbreiten": {f"{w:.2f}mm": round(ampacity(w), 2) for w in (0.127, 0.2, 0.25, 0.4, 0.5, 0.8)},
        "hinweise": [
            "PUMP_N wird vom easyeda-agent-Netklassen-Modell als SIGNAL eingestuft "
            "(Heuristik nach Netznamen: nur VBUS/VIN/VBAT/VSYS gelten als high-current). "
            "PUMP_N traegt aber den vollen Pumpenstrom -> beim Verdrahten explizit "
            "'pcb track --width 20' (0,5 mm) oder Schiene als Fuellflaeche legen.",
            "GND nicht als duenne Leiterbahn fuehren: Masseflaeche auf der Unterseite "
            "(pcb power-pour), Stiche >= 0,5 mm, Via-Stitching an Lader/LDO/Pumpenrueckweg.",
            "Am MOSFET-Pad (SOT-23) darf die Bahn kurz auf Padbreite verjuengen "
            "(neck-down) - das ist bei Leistungspfaden normal und nur ein 'pcb check'-Hinweis.",
            "Anlaufstrom der Pumpe ist nicht dokumentiert -> am Prototyp messen und "
            "die 0,5 mm gegen 1,5 A (dT 10,9 K) gegenpruefen.",
            "USB_DP/USB_DM als Paar (diff-pair) deklarieren und laengengleich fuehren; "
            "kontrollierte Impedanz bietet JLCPCB nur ab 4 Lagen, bei 12 Mbit/s FS-USB "
            "ist ein kurzes, paralleles Paar ausreichend.",
        ],
    }

if __name__ == "__main__":
    spec = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "netclass_spec.json")
    with open(os.path.abspath(out), "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"geschrieben: {os.path.abspath(out)}")
    print(f"\n{'Netz':<12} {'Rolle':<13} {'Soll':>7} {'min':>6} {'I [A]':>7} {'dT [K]':>7} {'Abfall@40mm':>12}")
    for name, e in spec["nets"].items():
        if not e["width_mm"]:
            print(f"{name:<12} {e['role']:<13} {'Flaeche':>7} {'-':>6} {e['current_a']:7.3f}")
            continue
        print(f"{name:<12} {e['role']:<13} {e['width_mm']:6.2f}mm {e['min_width_mm']:5.2f} "
              f"{e['current_a']:7.3f} {e['dt_k_at_current']:7.2f} {e.get('drop_mv_at_40mm', 0):9.1f} mV")
