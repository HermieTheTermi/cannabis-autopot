#!/usr/bin/env python3
"""S3: layout-input für `easyeda sch lib-layout` bauen.

Verbindet die kanonische Connectivity-IR (Netze/Pins aus der Netzliste) mit der am
lebenden Symbol gemessenen Geometrie (bbox, Pin-XY, Rotation) der bereits platzierten
Seite. Ergebnis ist die Eingabe für lib-layout → compose (Design-Flow S3).

Eingang:  raw/ir_numbered.json    (Connectivity 1.4, kanonische Refs)
          s3/page_placed.json     (`sch list --include-device-identity --include-pins --include-bbox`)
          raw/modules.json        (Originalname -> Modul)
Ausgang:  raw/layout_input.json
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw')

POWER_NETS = {'+3V3': 'local_power', 'VBAT': 'local_power', 'VBUS': 'local_power', 'GND': 'local_ground'}

# Modul -> (Titel, Core-Originalname)
MODULE_CORE = {
    'USB':      ('USB-C Eingang & ESD-Schutz',      'J5'),
    'LADER':    ('Laden (MCP73831)',                'U3'),
    'AKKU':     ('Akku & Puffer',                   'J1'),
    'WAEChTER': ('Unterspannungswächter (MAX809)',  'U7'),
    'LDO':      ('3V3-LDO (ME6211)',                'U4'),
    'MCU':      ('ESP32-C6-MCU + Beschaltung',      'U1'),
    'TASTER':   ('Taster & LEDs',                   'J6'),
    'PUMPE':    ('Pumpentreiber (Low-Side)',        'Q1'),
    'SENSOR':   ('Sensor-Eingang',                  'J2'),
    'DEBUG':    ('UART-Debug-Pads (DNP)',           'R_UART'),
}
MODULE_ORDER = ['USB', 'LADER', 'AKKU', 'WAEChTER', 'LDO', 'MCU',
                'TASTER', 'PUMPE', 'SENSOR', 'DEBUG']

# peripheral(Originalname) -> (Referenz-Originalname, PinNummer) ; None = kein Anker
ATTACH = {
    # Schluessel/Werte in ORIGINAL-Bezeichnern (so heissen die IDs und modules.json)
    'U6': ('J5', 'A7'),        # ESD an D- (USB_DM)
    'R5a': ('J5', 'A5'),       # CC1-Pulldown
    'R5b': ('J5', 'B5'),       # CC2-Pulldown
    'C7': ('U3', '4'),         # VBUS/Ladereingang
    'C8': ('U3', '3'),         # VBAT
    'R_PROG': ('U3', '5'),     # PROG
    'D_LEDCHG': ('U3', '1'),   # STAT
    'R_LEDCHG': ('D_LEDCHG', '2'),   # Vorwiderstand in Reihe vor der LED
    'C3': ('J1', '1'),         # VBAT-Puffer
    'TP4': ('J1', '1'),        # VBAT-Testpad
    'TP3': ('J1', '2'),        # GND-Testpad
    'C12': ('U7', '3'),        # Decoupling am Wächter
    'R3a': ('U7', '3'),        # Teiler oben an VBAT
    'R3b': ('R3a', '2'),       # Teiler unten in Reihe
    'C5': ('U4', '1'),         # VIN
    'C6': ('U4', '5'),         # VOUT
    'TP5': ('U4', '5'),        # +3V3-Testpad
    'C1a': ('U1', '3'), 'C1b': ('U1', '3'), 'C2': ('U1', '3'),
    'C4': ('U1', '8'), 'R_EN': ('U1', '8'), 'SW1': ('U1', '8'),
    'R_BOOT': ('U1', '23'), 'SW2': ('U1', '23'),
    'R_GPIO8': ('U1', '22'),
    'C9': ('U1', '12'), 'C10': ('U1', '13'),
    'R4': ('U1', '19'), 'D2': ('R4', '2'),
    'R_TANK': ('U1', '16'), 'D5': ('R_TANK', '2'),
    'TP2': ('U1', '30'),
    'R_BTN': ('J6', '1'), 'C_BTN': ('J6', '1'),
    'R1': ('Q1', '1'), 'R2': ('Q1', '1'), 'D3': ('Q1', '1'),
    'D1': ('Q1', '3'), 'C11': ('Q1', '3'), 'J4': ('Q1', '3'),
    'R6': ('J2', '2'),
    'TP6': ('R6', '2'),
    'TP1': ('R_UART', '2'),
}


def main():
    ir = json.load(open(os.path.join(RAW, 'ir_numbered.json')))
    live = json.load(open(os.path.join(ROOT, 's3', 'page_placed.json')))['result']['components']
    modules = json.load(open(os.path.join(RAW, 'modules.json')))

    live_by_ref = {c['designator']: c for c in live if c.get('componentType') == 'part'}
    ir_by_id = {c['id']: c for c in ir['components']}
    net_name = {n['id']: n['name'] for n in ir['nets']}
    pin_net = {(c['componentId'], c['pinNumber']): net_name[c['netId']] for c in ir['connections']}

    orig_of = {c['id']: c['id'][4:] for c in ir['components']}
    core_ref = {v[1]: k for k, v in MODULE_CORE.items()}

    # --- measurements aus der lebenden Seite + Netze aus der IR -------------
    measurements = []
    for comp in ir['components']:
        ref = comp['ref']
        lc = live_by_ref.get(ref)
        if lc is None:
            raise SystemExit(f"{ref} nicht auf der Seite gefunden")
        bb = lc['bbox']
        pins = []
        for p in lc['pins']:
            pins.append({'number': p['pinNumber'], 'name': p['pinName'],
                         'net': pin_net.get((comp['id'], p['pinNumber']), ''),
                         'x': p['x'], 'y': p['y']})
        measurements.append({'designator': ref,
                             'x': lc['x'], 'y': lc['y'],
                             'rotation': lc.get('rotation', 0),
                             'mirror': bool(lc.get('mirror', False)),
                             'bbox': {'minX': bb['minX'], 'minY': bb['minY'],
                                      'maxX': bb['maxX'], 'maxY': bb['maxY']},
                             'pins': pins})

    # --- Modulmitglieder + Netzpolitik -------------------------------------
    members = {}
    for comp in ir['components']:
        members.setdefault(modules[orig_of[comp['id']]], []).append(comp['id'])

    # Netz -> Module, in denen es vorkommt
    net_modules = {}
    for (cid, pin), net in pin_net.items():
        net_modules.setdefault(net, set()).add(modules[orig_of[cid]])

    layout_modules, connectivity_modules = [], []
    for mod in MODULE_ORDER:
        title, core_orig = MODULE_CORE[mod]
        core_id = f"cmp-{core_orig}"
        if core_id not in members.get(mod, []):
            raise SystemExit(f"Core {core_orig} nicht in Modul {mod}")
        policies = {}
        for net, mods in net_modules.items():
            if mod not in mods:
                continue
            if net in POWER_NETS:
                policies[net_id(net)] = POWER_NETS[net]
            elif len(mods) > 1:
                policies[net_id(net)] = 'module_port'
            else:
                policies[net_id(net)] = 'direct'
        periph = []
        for cid in members[mod]:
            if cid == core_id:
                continue
            orig = orig_of[cid]
            anchor = ATTACH.get(orig)
            if anchor is None:
                raise SystemExit(f"kein Anker fuer {orig} ({mod})")
            ref_orig, pin = anchor
            ref_cid = f"cmp-{ref_orig}"
            if ref_cid not in members[mod]:
                raise SystemExit(f"{orig}: Anker {ref_orig} nicht im Modul {mod}")
            periph.append({'componentId': cid, 'attachTo': {'componentId': ref_cid, 'pinNumber': pin}})
        layout_modules.append({'id': mod, 'title': title,
                               'coreComponentId': core_id,
                               'netPolicies': policies,
                               'peripherals': periph})
        connectivity_modules.append({'id': mod, 'name': title,
                                     'coreComponents': [core_id],
                                     'peripheralComponents': [c for c in members[mod] if c != core_id]})

    ir_with_modules = dict(ir)
    ir_with_modules['modules'] = connectivity_modules

    doc = {
        'schemaVersion': 1,
        'connectivity': ir_with_modules,
        'sheet': {'minX': 0, 'minY': 0, 'maxX': 1170, 'maxY': 825},
        'sheetBorder': {'minX': 30, 'minY': 20, 'maxX': 1150, 'maxY': 810},
        'keepouts': [{'minX': 468, 'minY': 0, 'maxX': 1170, 'maxY': 198}],
        'measurements': measurements,
        'layoutModules': layout_modules,
    }
    out = os.path.join(RAW, 'layout_input.json')
    json.dump(doc, open(out, 'w'), ensure_ascii=False, indent=1)
    print(f"layout-input: {out}")
    for lm in layout_modules:
        print(f"  {lm['id']:<9} core={lm['coreComponentId']:<10} "
              f"peripherals={len(lm['peripherals'])} netPolicies={len(lm['netPolicies'])}")
    return 0


def net_id(name):
    import hashlib
    return "net-" + hashlib.sha1(("SmartGrowTopf_V1/" + name).encode()).hexdigest()


if __name__ == '__main__':
    raise SystemExit(main())
