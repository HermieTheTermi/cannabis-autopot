"""Kleine Simulationen / Rechenproben in reinem Python (Stand 2S-Umbau).

Keine externen Solver.  Alle Eingangswerte kommen aus :mod:`design.circuit`.
Getroffene Modellannahmen stehen in ``circuit.ASSUMPTIONS`` und werden in der
Ausgabe als Annahme genannt.
"""
from __future__ import annotations

import re

from . import circuit

# IP2326-Datenblatt V1.11 §"充电电流设置" S. 11: ICHG = 90000/R_ISET[Ohm].
IP2326_ICHG_K = 90000.0


def gate_driver(r1, r2, ciss, vgpio, vtarget, pwm_hz):
    """Gate-Treiber R1/R2 mit Ciss: Einschaltzeit und GPIO-Strom.

    Euler-Integration von Ciss·dV/dt = (VGPIO - V)/R1 - V/R2.
    """
    vth = vgpio * r2 / (r1 + r2)
    r_th = r1 * r2 / (r1 + r2)
    tau = r_th * ciss
    dt = tau / 1000.0
    v = 0.0
    t = 0.0
    charge = 0.0
    limit = 20.0 * tau
    while v < vtarget and t < limit:
        i_gpio = (vgpio - v) / r1
        i_r2 = v / r2
        v += (i_gpio - i_r2) / ciss * dt
        charge += i_gpio * dt
        t += dt
    return {
        "v_ziel": vth,
        "tau_us": tau * 1e6,
        "t_ein_us": t * 1e6,
        "i_peak_ma": vgpio / r1 * 1000.0,
        "i_mittel_ma": (charge / t * 1000.0) if t > 0 else 0.0,
        "periode_us": 1e6 / pwm_hz,
        "anteil_prozent": t * pwm_hz * 100.0,
    }


def charge_time(capacity_mah, i_charge_a, cc_frac, cv_i_frac):
    """Grobe Ladezeit: CC-Phase (cc_frac) + CV-Phase (Rest bei gemitteltem I)."""
    q = capacity_mah / 1000.0
    t_cc = cc_frac * q / i_charge_a
    t_cv = (1.0 - cc_frac) * q / (i_charge_a * cv_i_frac)
    return {
        "i_charge_a": i_charge_a,
        "capacity_mah": capacity_mah,
        "t_cc_h": t_cc,
        "t_cv_h": t_cv,
        "t_total_h": t_cc + t_cv,
    }


def pump_runtime(v_rail, i_pump, dose_ml, flow_ml_min, usable_wh):
    """Energie pro Dosis und Anzahl der Dosiervorgaenge pro Ladung (5-V-Schiene)."""
    p_w = v_rail * i_pump
    t_min = dose_ml / flow_ml_min
    wh_dose = p_w * t_min / 60.0
    doses = usable_wh / wh_dose
    return {
        "p_w": p_w,
        "t_min": t_min,
        "wh_dosis": wh_dose,
        "dosen": doses,
    }


def pump_inrush(v_bat, v_rail, i_pump, eff, r_bat):
    """Einbruch der Packspannung beim Pumpenanlauf ueber den Innenwiderstand."""
    i_bat = v_rail * i_pump / (eff * v_bat)
    sag = i_bat * r_bat
    return {
        "i_bat": i_bat,
        "r_bat": r_bat,
        "einbruch_v": sag,
        "v_min": v_bat - sag,
    }


def buck_ripple(v_in, v_out, inductance_h, f_sw_hz, i_load):
    """Rippelstrom und Spitzenstrom eines Abwaertswandlers.

    D = Vout/Vin; dI = (Vin-Vout)*D/(L*f); I_peak = I_load + dI/2.
    """
    d = v_out / v_in
    di = (v_in - v_out) * d / (inductance_h * f_sw_hz)
    return {"d": d, "di": di, "i_peak": i_load + di / 2.0}


def divider_currents(v_bat, r_top, r_bot):
    """Strom durch einen Spannungsteiler."""
    return v_bat / (r_top + r_bot)


def standby_mah_per_day(total_ua):
    """Tagesverbrauch eines Ruhestroms in mAh."""
    return total_ua / 1000.0 * 24.0


def ldo_heat(vbat, vout, current_a):
    """Verlustleistung, falls (rechnerisch) ein LDO an dieser Stelle saesse."""
    return (vbat - vout) * current_a


def tank_led_blink(i_continuous, pulses, on_time_s, period_s):
    """Mittlerer Strom der Tank-LED im Blinkbetrieb und Tagesverbrauch."""
    duty = pulses * on_time_s / period_s
    i_mean = i_continuous * duty
    return {
        "pulse": pulses,
        "t_on_ms": on_time_s * 1000.0,
        "periode_s": period_s,
        "tastverhaeltnis_prozent": duty * 100.0,
        "i_dauer_ma": i_continuous * 1000.0,
        "i_mittel_ma": i_mean * 1000.0,
        "dauer_mah_pro_tag": i_continuous * 1000.0 * 24.0,
        "mittel_mah_pro_tag": i_mean * 1000.0 * 24.0,
    }


def light_adc(r_load, vref_v, lux_values):
    """ADC-Counts des ALS-PT19 am Lastwiderstand R_LIGHT (12 Bit, ATTEN3)."""
    rows = []
    for lux in lux_values:
        i = circuit.LIGHT_SENS_UA_REF * 1e-6 * (lux / circuit.LIGHT_SENS_LUX_REF)
        v = min(i * r_load, vref_v)
        rows.append({"lux": lux, "v": v,
                     "counts": v / vref_v * circuit.ADC_COUNTS_12BIT})
    return rows


def _blinkmuster():
    """Liest das dokumentierte Blinkmuster aus schaltplan_v1.md (Abschnitt 7.4)."""
    text = circuit.SCHEMATIC_PATH.read_text(encoding="utf-8")
    m = re.search(r"([0-9]+)\s*[\u00d7x]\s*([0-9]+)\s*ms\s*alle\s*([0-9]+)\s*s",
                  text)
    if m is None:
        raise circuit.CircuitError(
            "Blinkmuster '3 x 50 ms alle 5 s' nicht gefunden")
    return int(m.group(1)), float(m.group(2)) / 1000.0, float(m.group(3))


def run_all():
    """Fuehrt alle Simulationen mit den echten Schaltplandaten aus."""
    sys = circuit.load_system()
    ann = circuit.ASSUMPTIONS

    r1 = circuit.parse_ohm(circuit.part("R1")["value"])
    r2 = circuit.parse_ohm(circuit.part("R2")["value"])
    ciss = 630e-12  # AO3400A-Datenblatt: Ciss ca. 630 pF
    gate = gate_driver(r1, r2, ciss, circuit.rail_3v3(), 2.5, sys["pwm_hz"])

    # Ladestrom aus R_ISET; Ladezeit mit CC/CV-Annahmen (circuit.ASSUMPTIONS).
    r_iset = circuit.parse_ohm(circuit.part("R_ISET")["value"])
    i_charge = IP2326_ICHG_K / r_iset
    charge = charge_time(sys["pack_capacity_mah"], i_charge,
                         ann["cc_frac"], ann["cv_i_frac"])

    # Nutzbare Energie des 2S-Packs (nominale Zellspannung x2 x Nutzanteil).
    pack_v_nom = 2.0 * sys["cell_v_nom"]
    usable_wh = (sys["pack_capacity_mah"] / 1000.0 * pack_v_nom
                 * ann["usable_frac"])
    runtime = pump_runtime(circuit.rail_5v(), sys["pump_i_nom_a"],
                           sys["dose_ml"], sys["pump_flow_ml_min"], usable_wh)

    inrush = pump_inrush(sys["pack_v_min"], circuit.rail_5v(),
                         sys["pump_i_inrush_a"], 0.90, ann["r_bat_ohm"])

    l5 = circuit.parse_henry(circuit.part("L_BUCK5")["desc"])
    l3 = circuit.parse_henry(circuit.part("L_BUCK3")["desc"])
    ripple5 = buck_ripple(sys["pack_v_max"], circuit.rail_5v(), l5,
                          500e3, sys["pump_i_inrush_a"])
    ripple3 = buck_ripple(sys["pack_v_max"], circuit.rail_3v3(), l3,
                          1.1e6, sys["module_tx_peak_ma"] / 1000.0)

    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    r_top = circuit.parse_ohm(circuit.part("R_SENSE_TOP")["value"])
    r_bot = circuit.parse_ohm(circuit.part("R_SENSE_BOT")["value"])
    div_uvlo = divider_currents(sys["pack_v_max"], r3a, r3b)
    div_adc = divider_currents(sys["pack_v_max"], r_top, r_bot)
    total_ua = (sys["module_sleep_ua"] + sys["iq_buck5_ua"] + sys["iq_buck3_ua"]
                + sys["iq_watchdog_ua"]) + (div_uvlo + div_adc) * 1e6
    standby = {
        "total_ua": total_ua,
        "mah_day": standby_mah_per_day(total_ua),
    }

    vf_led = 2.0  # rote 0805-LED, typische Flussspannung (Datenblatt)
    r_tank = circuit.parse_ohm(circuit.part("R_TANK")["value"])
    i_tank = (circuit.rail_3v3() - vf_led) / r_tank
    pulses, on_time_s, period_s = _blinkmuster()
    tank = tank_led_blink(i_tank, pulses, on_time_s, period_s)

    r_light = circuit.parse_ohm(circuit.part("R_LIGHT")["value"])
    light = light_adc(r_light, circuit.ADC_VREF_MV_ATTEN12 / 1000.0,
                      [0.0, 100.0, 1000.0, circuit.LIGHT_GROW_LUX])

    assumptions = [
        "Innenwiderstand des 2S-Packs R_BAT = %s (Annahme)"
        % ("%.2f Ω" % ann["r_bat_ohm"]).replace(".", ","),
        "Ladezeit: CC-Anteil %s %%, mittlerer CV-Strom %s %% von ICHG (Annahme)"
        % ("%.0f" % (ann["cc_frac"] * 100.0),
           "%.0f" % (ann["cv_i_frac"] * 100.0)),
        "nutzbarer Anteil der Packkapazitaet %s %% (Annahme)"
        % ("%.0f" % (ann["usable_frac"] * 100.0)),
        "Buck-Wirkungsgrad beim Anlauf 90 % (Annahme)",
    ]

    return {
        "gate": gate,
        "charge": charge,
        "runtime": runtime,
        "inrush": inrush,
        "ripple5": ripple5,
        "ripple3": ripple3,
        "divider": {"uvlo_a": div_uvlo, "adc_a": div_adc},
        "standby": standby,
        "tank": tank,
        "light": light,
        "assumptions": assumptions,
        "rb": {"R1": r1, "R2": r2, "ciss": ciss, "pack_v_nom": pack_v_nom,
               "usable_wh": usable_wh, "R_TANK": r_tank, "R_LIGHT": r_light,
               "L_BUCK5": l5, "L_BUCK3": l3},
    }


if __name__ == "__main__":
    result = run_all()
    for key, value in result.items():
        print(key, value)
