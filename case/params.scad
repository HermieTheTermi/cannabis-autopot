// ============================================================================
//  Smart Grow Topf — zentrale Parameter
//  Alle Maße in mm. Verbindliche Werte: docs/02_architektur-und-geometrie.md
//  Hier aendern, nichts in den Bauteilen hart verdrahten.
// ============================================================================

// ---- Render-Qualitaet -------------------------------------------------------
$fn = 96;          // Zylinder-/Rotationsaufloesung (Druck: 96 genuegt)

// ---- Grundkoerper -----------------------------------------------------------
shell_od    = 140.0;                 // Aussen-Durchmesser Topf
wall        = 3.0;                   // Wandstaerke
shell_or    = shell_od / 2;          // 70.0
shell_ir    = shell_or - wall;       // 67.0  Innen-Durchmesser = 134
total_h     = 278.0;                 // Gesamthoehe ohne Pflanze
floor_t     = 3.0;                   // Bodenstaerke Tank

// ---- Wassertank -------------------------------------------------------------
tank_h      = 82.0;                  // Innenhoehe bis Rostauflage
max_water   = 71.0;                  // max. Wasserstand (1,0 L)

// Einfuellstutzen — Wasser nachfuellen, ohne die obere Schale abzunehmen
fill_ang      = 45.0;   // Neigung der Achse ueber der Horizontalen
fill_z_wall   = 68.0;   // Hoehe der Achse beim Durchtritt durch die Aussenwand (r = shell_or)
fill_bore_d   = 16.0;   // lichte Bohrung des Stutzens
fill_wall     = 4.5;    // Wandstaerke des Stutzens
fill_len      = 18.0;   // Laenge ab der Aussenwand, entlang der Achse gemessen
fill_mouth_d  = 22.0;   // Aufweitung (Trichterlippe) am Mund, 45-Grad-Kegel
fill_cs_len   = 3.0;    // Laenge der Aufweitung entlang der Achse
fill_start    = 10.0;   // wie weit der Stutzenkoerper in die Wand hineinreicht (von r = shell_or nach innen)

// ---- Auflagerost / Trennplatte ---------------------------------------------
grid_t      = 4.0;                   // Dicke
grid_od     = 132.0;                 // Aussen-Durchmesser
grid_or     = grid_od / 2;           // 66.0
grid_z0     = tank_h;                // 82.0
grid_z1     = grid_z0 + grid_t;      // 86.0
grid_hole_d = 4.0;                   // Lochung (haelt Blahton zurueck)
grid_pitch  = 9.0;
grid_rim    = 4.0;                   // ungelochter Rand
ledge_ir    = 60.0;                  // Auflagering innen (Tankseite)
ledge_h     = 3.0;
ledge_z1    = grid_z0;               // 82.0
ledge_z0    = ledge_z1 - ledge_h;    // 79.0

// ---- Luftspalt / Innentopf --------------------------------------------------
air_gap     = 30.0;                  // 86 -> 116 ueber max. Wasserstand
pot_z0      = grid_z1 + air_gap;     // 116.0
pot_h       = 150.0;                 // Erdbehaelterhoehe
pot_od      = 132.0;
pot_or      = pot_od / 2;            // 66.0
pot_wall    = 2.5;
pot_ir      = pot_or - pot_wall;     // 63.5
pot_floor_t = 3.0;
pot_z1      = pot_z0 + pot_h;        // 266.0
foot_h      = air_gap;               // Giessfuesse
n_feet      = 6;
foot_r      = 58.0;                  // Fussradius
foot_w      = 12.0;                  // tangentiale Fussbreite
foot_d      = 8.0;                   // radiale Fusstiefe
drain_hole_d = 4.0;
drain_pitch  = 10.0;
pot_hose_w   = 6.0;                  // Schlauchdurchlass am Rand oben (Breite X)
pot_hose_h   = 6.0;                  // Schlauchdurchlass am Rand oben (Tiefe Z)

// ---- Kragen / Ringauflage ---------------------------------------------------
collar_z0   = pot_z1;                // 266.0
collar_z1   = total_h;               // 278.0
collar_h    = collar_z1 - collar_z0;// 12.0
collar_r    = shell_or + 2.0;        // 72.0 Ausstellungsradius

// LST-Ankerloecher im Kragen (Schnur durchfaedeln, Low-Stress-Training)
lst_rows      = 2;                  // Anzahl Lochreihen
lst_holes     = 24;                 // Loecher je Reihe, gleichmaessig ueber den Umfang
lst_hole_d    = 2.2;                // gezeichnet: gedruckt bleiben davon ca. 2,0 mm
lst_row_z     = [269.5, 274.5];     // Hoehe der Reihen (Kragenmitte)
lst_gap_deg   = 8.0;                // Freihaltung um den Sensorkabel-Ausschnitt (+Y = 90 Grad)
lst_drill_len = 10.0;               // radiale Bohrtiefe (grosszuegig durch die Kragenwand)

// ---- Wulst (Elektronik + Kanaele) -------------------------------------------
wulst_z0      = 90.0;
wulst_h       = 160.0;
wulst_z1      = wulst_z0 + wulst_h;  // 250.0
wulst_w       = 60.0;                // tangential (X)
wulst_d       = 40.0;                // radial, ab Mantel
wulst_y_outer = shell_or + wulst_d;  // 110.0
wulst_cr      = 8.0;                 // Eckradius (vertikal)
wulst_wall    = 6.0;                 // Wandstaerke Wulst
wulst_taper   = 40.0;                // 45-Grad-Bodenfase (stuetztragfrei)

// Innenraum (Elektronikkammer)
wc_x   = 20.0;                       // halbe Breite
wc_y0  = 72.0;                       // innen (hinter der Mantelwand)
wc_y1  = wulst_y_outer + 2.0;        // vorne (durch Deckeloeffnung)
wc_z0  = wulst_z0 + 2.0;             // 92.0
wc_z1  = wulst_z1 - wulst_wall;      // 244.0

// Kanaele
cable_d  = 4.5;                      // Sensorkabel
cable_z  = 246.0;
hose_w   = 6.0;                      // Schlauchkanal
hose_z   = 100.0;
pressure_hole_d = 6.5;               // Druckschlauch nach oben
pressure_x = 14.0;
pressure_y = 98.0;

// Deckel-Verschraubung (Innengewinde-Platzhalter fuer M2.5)
boss_d    = 7.0;
boss_hole_d = 2.4;
boss_x    = 17.0;
boss_z    = [100.0, 234.0];

// Tropfkante Wulstboden
drip_band = 1.6;                     // radiale Ueberlappung
drip_h    = 1.6;
drip_z    = wulst_z0 + wulst_taper - 1.0;  // 129.0

// ---- Bauteil-Footprints (Elektronik) ---------------------------------------
xiao_w   = 21.0;                     // XIAO ESP32-C6
xiao_l   = 17.5;
pcb_l    = 52.0;                     // Eigenbau-PCB
pcb_w    = 42.0;
pcb_t    = 1.6;
batt_l   = 59.0;                     // EFASO 503759
batt_w   = 37.0;
batt_t   = 5.0;
pump_d   = 27.8;                     // Adafruit 3910
pump_l   = 66.8;
pump_mount_d = 3.7;                  // Montagebohrungen
pump_mount_cc = 50.0;                // Lochabstand
usb_w    = 9.5;                      // USB-C Durchbruch
usb_h    = 3.6;
led_d    = 5.0;

// ---- Verteilerring ----------------------------------------------------------
ring_od       = 105.0;               // <= 105
ring_or       = ring_od / 2;         // 52.5
ring_ir       = 38.0;                // innere Oeffnung
ring_h        = 16.0;
ring_wall     = 2.2;
ring_holes    = 10;                  // 8..12
ring_hole_d   = 2.6;
ring_hole_r   = ring_ir + 5.0;       // Bohrkreis (innen/ unten)
ring_barb_len = 7.5;                 // Stutzenlaenge (max. 8, gekuerzt wegen Topfwand)
ring_barb_dir = 90.0;                // Stutzenrichtung: 0=+X, 90=+Y (Richtung Wulst)
ring_barb_od  = 5.6;
ring_barb_id  = 3.8;

// ---- Abdeckung (optional) ---------------------------------------------------
cover_od   = 136.0;
cover_t    = 3.0;
cover_hole = 45.0;

// ---- Kappe fuer den Einfuellstutzen -----------------------------------------
cap_od     = 30.0;                   // Aussen-Durchmesser
cap_h      = 12.0;                   // Hoehe (Drucklage, offene Seite nach oben)
cap_id     = 24.8;                   // Sackloch-Bohrung, Klemmsitz auf Stutzen-Aussenmass 25,0
cap_depth  = 9.0;                    // Tiefe der Sackloch-Bohrung (3,0 mm Deckel bleibt)
cap_vent_d = 2.0;                    // Lueftungsloch im Deckel (Druckausgleich)
cap_rib_w  = 3.0;                    // Rippenbreite (tangential)
cap_rib_t  = 1.5;                    // Rippendicke (radial)

// ---- Segmentierung (Bauraum 220 x 220 x 250) --------------------------------
split_z    = wulst_z0;               // 90.0  Trennebene unten/oben
spigot_h   = 6.0;                    // Steckzapfen
spigot_or  = shell_or - 2.0;         // 68.0
socket_ir  = spigot_or + 0.6;        // 68.6 Einsteck-Spiel
