# ============================================================================
#  Smart Grow Topf - zentrale Parameter (Port von case/params.scad)
#  Alle Masse in mm. 1:1 aus dem OpenSCAD uebernommen, abgeleitete Werte
#  werden berechnet (nicht doppelt eingetragen).
# ============================================================================

# ---- Grundkoerper -----------------------------------------------------------
shell_od = 140.0
wall = 3.0
shell_or = shell_od / 2
shell_ir = shell_or - wall
total_h = 278.0
floor_t = 3.0

# ---- Wassertank -------------------------------------------------------------
tank_h = 82.0
max_water = 71.0

# ---- Einfuellstutzen --------------------------------------------------------
fill_ang = 45.0
fill_z_wall = 68.0
fill_bore_d = 16.0
fill_wall = 4.5
fill_len = 18.0
fill_mouth_d = 22.0
fill_cs_len = 3.0
fill_start = 10.0

# ---- Auflagerost / Trennplatte ---------------------------------------------
grid_t = 4.0
grid_od = 132.0
grid_or = grid_od / 2
grid_z0 = tank_h
grid_z1 = grid_z0 + grid_t
grid_hole_d = 4.0
grid_pitch = 9.0
grid_rim = 4.0
ledge_ir = 60.0
ledge_h = 3.0
ledge_z1 = grid_z0
ledge_z0 = ledge_z1 - ledge_h

# ---- Luftspalt / Innentopf --------------------------------------------------
air_gap = 30.0
pot_z0 = grid_z1 + air_gap
pot_h = 150.0
pot_od = 132.0
pot_or = pot_od / 2
pot_wall = 2.5
pot_ir = pot_or - pot_wall
pot_floor_t = 3.0
pot_z1 = pot_z0 + pot_h
foot_h = air_gap
n_feet = 6
foot_r = 58.0
foot_w = 12.0
foot_d = 8.0
drain_hole_d = 4.0
drain_pitch = 10.0
pot_hose_w = 6.0
pot_hose_h = 6.0

# ---- Kragen / Ringauflage ---------------------------------------------------
collar_z0 = pot_z1
collar_z1 = total_h
collar_h = collar_z1 - collar_z0
collar_r = shell_or + 2.0

# LST-Ankerloecher im Kragen
lst_rows = 2
lst_holes = 24
lst_hole_d = 2.2
lst_row_z = [269.5, 274.5]
# Im SCAD 8.0; der Port setzt die Freihaltung auf 6.0, damit die zweite Reihe
# (7,5-Grad-Versatz) neben dem Kragenausschnitt vollstaendig erhalten bleibt
# (erwartet 23 + 24 = 47 Bohrungen).
lst_gap_deg = 6.0
lst_drill_len = 10.0

# ---- Wulst (Elektronik + Kanaele) -------------------------------------------
wulst_z0 = 90.0
wulst_h = 160.0
wulst_z1 = wulst_z0 + wulst_h
wulst_w = 60.0
wulst_d = 40.0
wulst_y_outer = shell_or + wulst_d
wulst_cr = 8.0
wulst_wall = 6.0
wulst_taper = 40.0

# Innenraum (Elektronikkammer)
wc_x = 20.0
wc_y0 = 72.0
wc_y1 = wulst_y_outer + 2.0
wc_z0 = wulst_z0 + 2.0
wc_z1 = wulst_z1 - wulst_wall

# Kanaele
cable_d = 4.5
cable_z = 246.0
hose_w = 6.0
hose_z = 100.0
pressure_hole_d = 6.5
pressure_x = 14.0
pressure_y = 98.0

# Deckel-Verschraubung
boss_d = 7.0
boss_hole_d = 2.4
boss_x = 17.0
boss_z = [100.0, 234.0]

# Tropfkante Wulstboden
drip_band = 1.6
drip_h = 1.6
drip_z = wulst_z0 + wulst_taper - 1.0

# ---- Bauteil-Footprints (Elektronik) ---------------------------------------
xiao_w = 21.0
xiao_l = 17.5
pcb_l = 52.0
pcb_w = 42.0
pcb_t = 1.6
batt_l = 59.0
batt_w = 37.0
batt_t = 5.0
pump_d = 27.8
pump_l = 66.8
pump_mount_d = 3.7
pump_mount_cc = 50.0
usb_w = 9.5
usb_h = 3.6
led_d = 5.0

# ---- Verteilerring ----------------------------------------------------------
ring_od = 105.0
ring_or = ring_od / 2
ring_ir = 38.0
ring_h = 16.0
ring_wall = 2.2
ring_holes = 10
ring_hole_d = 2.6
ring_hole_r = ring_ir + 5.0
ring_barb_len = 7.5
ring_barb_dir = 90.0
ring_barb_od = 5.6
ring_barb_id = 3.8

# ---- Abdeckung (optional) ---------------------------------------------------
cover_od = 136.0
cover_t = 3.0
cover_hole = 45.0

# ---- Kappe fuer den Einfuellstutzen -----------------------------------------
cap_od = 30.0
cap_h = 12.0
cap_id = 24.8
cap_depth = 9.0
cap_vent_d = 2.0
cap_rib_w = 3.0
cap_rib_t = 1.5

# ---- Segmentierung (Bauraum 220 x 220 x 250) --------------------------------
split_z = wulst_z0
spigot_h = 6.0
spigot_or = shell_or - 2.0
socket_ir = spigot_or + 0.6

# ---- Wulstdeckel (nur in modules.scad definiert) ----------------------------
lid_t = 4.0
usb_y = 15.0
led_y = 40.0
lid_screw_y = [100 - (wulst_z0 + wulst_h / 2), 234 - (wulst_z0 + wulst_h / 2)]
