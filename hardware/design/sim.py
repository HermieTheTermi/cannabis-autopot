"""Kleine Simulationen in reinem Python (Euler, feste Schrittweite).

Keine externen Solver.  Alle Eingangswerte kommen aus :mod:`design.circuit`.
"""
from __future__ import annotations

from . import circuit


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


def pump_inrush(c_buffer, vbat, i_load, duration_s, r_bat):
    """Spannungseinbruch auf VBAT bei einem Lastsprung.

    Modell: Zelle als Quellenspannung mit Innenwiderstand R_BAT, parallel der
    Pufferelko C3.  C·dV/dt = (VBAT - V)/R_BAT - I_load.
    """
    steps = 1000
    dt = duration_s / steps
    v = vbat
    for _ in range(steps):
        i_cap = (vbat - v) / r_bat - i_load
        v += i_cap / c_buffer * dt
    return {
        "v_start": vbat,
        "v_ende": v,
        "einbruch_mv": (vbat - v) * 1000.0,
        "r_bat": r_bat,
        "kapazitaet_ideal_mv": i_load * duration_s / c_buffer * 1000.0,
    }


def battery_runtime(power_w, flow_ml_min, dose_ml, usable_wh):
    """Energie pro Dosis und Anzahl der Dosiervorgaenge pro Ladung."""
    t_min = dose_ml / flow_ml_min
    wh_dose = power_w * t_min / 60.0
    doses = usable_wh / wh_dose
    return {
        "zeit_min": t_min,
        "wh_dosis": wh_dose,
        "dosen": doses,
    }


def ldo_heat(vbat, vout, current_a):
    """Verlustleistung des LDO im Burst: P = (VBAT - VOUT) · I."""
    return (vbat - vout) * current_a


def run_all():
    """Fuehrt alle Simulationen mit den echten Schaltplandaten aus."""
    sys = circuit.load_system()

    r1 = circuit.parse_ohm(circuit.part("R1")["value"])
    r2 = circuit.parse_ohm(circuit.part("R2")["value"])
    ciss = 630e-12  # AO3400A-Datenblatt: Ciss ca. 630 pF
    gate = gate_driver(r1, r2, ciss, sys["rail_3v3"], 2.5, sys["pwm_hz"])

    c3 = circuit.parse_farad(circuit.part("C3")["value"])
    # Annahme: Innenwiderstand einer 1S-1500-mAh-Zelle, kein Datenblattwert.
    r_bat = 0.1
    inrush = pump_inrush(c3, sys["battery_voltage"], 1.0, 1e-3, r_bat)

    runtime = battery_runtime(sys["pump_power_w"], sys["pump_flow_ml_min"],
                              sys["dose_ml"], sys["battery_usable_wh"])

    heat_max = ldo_heat(sys["charge_voltage"], sys["rail_3v3"],
                        sys["tx_peak_ma"] / 1000.0)
    heat_nom = ldo_heat(sys["battery_voltage"], sys["rail_3v3"],
                        sys["tx_peak_ma"] / 1000.0)

    return {
        "gate": gate,
        "inrush": inrush,
        "runtime": runtime,
        "heat_max_w": heat_max,
        "heat_nom_w": heat_nom,
        "rb": {"R1": r1, "R2": r2, "C3": c3, "Ciss": ciss},
    }


if __name__ == "__main__":
    result = run_all()
    for key, value in result.items():
        print(key, value)
