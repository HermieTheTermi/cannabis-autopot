// ============================================================================
//  Smart Grow Topf — Zusammenbau-Ansicht (montierter Zustand)
//  Reine Ansicht / Kollisionspruefung — KEIN Druckteil.
//  Innentopf auf dem Rost, Aussenschale montiert, Verteilerring auf der
//  Substratoberflaeche, Sensormarker samt Kabelweg, Schlauchweg Wulst->Stutzen.
// ============================================================================
include <modules.scad>

// ---- Ansichts-Marker (nur Zusammenbau, keine Druckmasse) --------------------
sensor_r     = 55.0;                 // radiale Sensorposition
sensor_depth = 75.0;                 // Messtiefe (Elektrodenmitte) unter Substrat
sensor_d     = 5.0;                  // Marker-Stab
route_d      = 3.0;                   // Marker-Durchmesser Schlauch/Kabel

// Schlauchweg: Wulst-Austritt -> ueber Kragen/Topfrand -> Stutzenende (+Y)
hose_path = [
  [pressure_x, pressure_y, wulst_z1],
  [8, 84, 264],
  [2, 74, 280],
  [0, 66, 276],
  [0, ring_or + ring_barb_len, pot_z1 + ring_h/2],
];

// Kabelweg: Sensoroberkante -> Kragenausschnitt -> Kabelkanal Wulst
cable_path = [
  [0, sensor_r, pot_z1],
  [0, 60, pot_z1 + 1],
  [0, shell_or, collar_z0 + 3],
  [0, shell_or, cable_z],
];

// Kette aus Zylindern zwischen Wegpunkten
module chain(pts, d) {
  for (i = [0 : len(pts) - 2]) {
    a = pts[i];
    b = pts[i + 1];
    v = b - a;
    L = norm(v);
    if (L > 0.001)
      translate(a)
        rotate([0, 0, atan2(v[1], v[0])])
          rotate([0, acos(v[2] / L), 0])
            cylinder(d=d, h=L);
  }
}

// ---- Montierter Zustand -----------------------------------------------------
shell_lower();                                  // Tank-Segment
shell_upper();                                  // Wulst-/Kragen-Segment
translate([0, 0, grid_z0]) grid();              // Rost
translate([0, 0, pot_z0]) inner_pot();          // Innentopf, Fuesse auf dem Rost
translate([0, 0, pot_z1]) distribution_ring();  // Ring auf Substratoberflaeche

// Sensormarker (Stab) + Kabelweg
translate([0, sensor_r, pot_z1 - sensor_depth])
  cylinder(d=sensor_d, h=sensor_depth);
chain(cable_path, route_d);

// Schlauchweg Wulst -> Topfrand -> Stutzen
chain(hose_path, route_d);
