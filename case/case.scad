// ============================================================================
//  Smart Grow Topf — Gesamtansicht aller Druckteile (Explosions-/Drucklayout)
//  Einzelteile separat rendern: shell_upper.scad, shell_lower.scad,
//  inner_pot.scad, grid.scad, distribution_ring.scad, wulst_lid.scad,
//  cover.scad.  outer_shell.scad = Aussenschale gesamt (Vorschau).
// ============================================================================
include <modules.scad>

layout_dx = 175;

// Untere Aussenschale
translate([0, 0, 0]) shell_lower();

// Obere Aussenschale (Wulst/Kragen), zur Ansicht nach oben versetzt
translate([0, 0, split_z]) shell_upper();

// Innentopf
translate([layout_dx, 0, 0]) inner_pot();

// Rost
translate([2*layout_dx, 0, 0]) grid();

// Verteilerring
translate([3*layout_dx, 0, 0]) distribution_ring();

// Wulstdeckel (flach)
translate([3*layout_dx + 70, 0, 0]) wulst_lid();

// Abdeckung (flach)
translate([3*layout_dx + 230, 0, 0]) cover();

// Kappe fuer den Einfuellstutzen
translate([3*layout_dx + 380, 0, 0]) fill_cap();
