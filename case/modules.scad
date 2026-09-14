// ============================================================================
//  Smart Grow Topf — Geometrie-Module (von den Bauteil-Dateien eingebunden)
// ============================================================================
include <params.scad>

// ---------------------------------------------------------------------------
// 2D/3D-Hilfsformen
// ---------------------------------------------------------------------------

// Abgerundeter Quader, in XY zentriert, von z=0 bis z=h
module rrect(w, d, h, r) {
  hull() {
    translate([ w/2-r,  d/2-r, 0]) cylinder(r=r, h=h);
    translate([-w/2+r,  d/2-r, 0]) cylinder(r=r, h=h);
    translate([ w/2-r, -d/2+r, 0]) cylinder(r=r, h=h);
    translate([-w/2+r, -d/2+r, 0]) cylinder(r=r, h=h);
  }
}

// Lochraster (versetzte Reihen), gefiltert auf einen Kreis
module hole_grid(radius, d, pitch, z0, h) {
  $fn = 16;
  dy = pitch * sqrt(3) / 2;
  rows = floor(radius / dy);
  for (r = [-rows : rows]) {
    y    = r * dy;
    xoff = (abs(r) % 2 == 0) ? 0 : pitch / 2;
    cols = floor(radius / pitch);
    for (c = [-cols : cols]) {
      x = c * pitch + xoff;
      if (x*x + y*y <= radius*radius)
        translate([x, y, z0]) cylinder(d=d, h=h);
    }
  }
}

// ---------------------------------------------------------------------------
// Wulst
// ---------------------------------------------------------------------------

// Grundriss der Wulst (X = tangential, Y = radial von 0 bis wulst_y_outer)
module wulst_footprint_2d(off=0) {
  translate([0, wulst_y_outer/2])
    offset(r=off)
      offset(r=wulst_cr)
        square([wulst_w - 2*wulst_cr, wulst_y_outer - 2*wulst_cr], center=true);
}

// Stuetztragfrei: Boden als 45-Grad-Fase ausgebildet (Hull aus duennem
// Ansatz am Mantel und vollem Grundriss ab z = wulst_z0 + wulst_taper).
module wulst_envelope() {
  hull() {
    translate([-wulst_w/2, shell_or - 2, wulst_z0]) cube([wulst_w, 2, 0.01]);
    translate([0, 0, wulst_z0 + wulst_taper])
      linear_extrude(wulst_h - wulst_taper) wulst_footprint_2d();
  }
}

// Elektronikkammer (nach vorne offen, fuer den Deckel)
module wulst_cavity() {
  translate([-wc_x, wc_y0, wc_z0])
    cube([2*wc_x, wc_y1 - wc_y0, wc_z1 - wc_z0]);
}

// Deckel-Verschraubungsposten (innen an der Rueckwand)
module wulst_bosses() {
  for (x = [-boss_x, boss_x], z = boss_z)
    translate([x, wc_y0, z]) rotate([-90, 0, 0])
      cylinder(d=boss_d, h=(wulst_y_outer - 8) - wc_y0);
}

// Tropfkante am Wulstboden (unterbricht den Wasserfilm an der Aussenwand)
module wulst_drip_lip() {
  translate([0, 0, drip_z])
    linear_extrude(drip_h)
      difference() {
        wulst_footprint_2d(off=drip_band);
        wulst_footprint_2d();
      }
}

// ---------------------------------------------------------------------------
// Kragen / Auflagering
// ---------------------------------------------------------------------------
module collar_ring() {
  translate([0, 0, collar_z0])
    difference() {
      cylinder(r=collar_r, h=collar_h);
      translate([0, 0, -1]) cylinder(r=shell_ir, h=collar_h + 2);
    }
}

// LST-Ankerloecher: radiale Bohrungen durch den Kragen, Reihen versetzt,
// um den Sensorkabel-Ausschnitt (+Y = 90 Grad) freigehalten.
module lst_holes() {
  for (row = [0 : lst_rows - 1]) {
    z   = lst_row_z[row];
    off = (row % 2) * (180 / lst_holes);
    for (i = [0 : lst_holes - 1]) {
      a  = off + i * 360 / lst_holes;
      da = min(abs(a - 90), 360 - abs(a - 90));
      if (da >= lst_gap_deg)
        rotate([0, 0, a])
          translate([0, shell_ir - 1, z])
            rotate([-90, 0, 0])
              cylinder(d=lst_hole_d, h=lst_drill_len);
    }
  }
}

// Auflagering fuer den Rost (im Tank, unterhalb des Rostes)
module grid_ledge() {
  difference() {
    cylinder(r=shell_ir, h=ledge_h);
    translate([0, 0, -1]) cylinder(r=ledge_ir, h=ledge_h + 2);
  }
}

// ---------------------------------------------------------------------------
// Einfuellstutzen (Wassertank, -Y-Seite)
// Achse liegt in der YZ-Ebene, 45 Grad nach oben/aussen.
// ---------------------------------------------------------------------------
fill_dir = [0, -cos(fill_ang), sin(fill_ang)];      // Achsenrichtung nach -Y/+Z
fill_p0  = [0, -shell_or, fill_z_wall];             // Achspunkt an der Aussenwand

// Massivkoerper des Stutzens (von innen in der Wand bis zur Mundebene)
module fill_neck() {
  translate(fill_p0)
    rotate([90 - fill_ang, 0, 0])
      translate([0, 0, -fill_start])
        cylinder(d=fill_bore_d + 2*fill_wall, h=fill_start + fill_len);
}

// Bohrung inkl. kegeliger Trichterlippe am Mund (beidseitig ueberstehend)
module fill_bore() {
  translate(fill_p0)
    rotate([90 - fill_ang, 0, 0]) {
      translate([0, 0, -fill_start - 2])
        cylinder(d=fill_bore_d, h=fill_start + fill_len + 4);
      translate([0, 0, fill_len - fill_cs_len])
        cylinder(d1=fill_bore_d, d2=fill_mouth_d, h=fill_cs_len);
    }
}

// ---------------------------------------------------------------------------
// Aussenschale — unteres Segment (Tank)
// ---------------------------------------------------------------------------
module shell_lower() {
  difference() {
    union() {
      difference() {
        union() {
          cylinder(r=shell_or, h=split_z);
          translate([0, 0, split_z])
            cylinder(r=spigot_or, h=spigot_h);
          fill_neck();
        }
        translate([0, 0, floor_t])
          cylinder(r=shell_ir, h=split_z + spigot_h - floor_t + 1);
      }
      translate([0, 0, ledge_z0]) grid_ledge();
    }
    fill_bore();
  }
}

// ---------------------------------------------------------------------------
// Aussenschale — oberes Segment (Wulst, Kragen, Stecksockel)
// ---------------------------------------------------------------------------
module shell_upper() {
  difference() {
    union() {
      difference() {
        union() {
          translate([0, 0, split_z])
            cylinder(r=shell_or, h=total_h - split_z);
          wulst_envelope();
          collar_ring();
        }
        // Stecksockel (groesserer Freistich am unteren Rand)
        translate([0, 0, split_z])
          cylinder(r=socket_ir, h=spigot_h + 0.01);
        // Hauptkavitaet
        translate([0, 0, split_z + spigot_h])
          cylinder(r=shell_ir, h=total_h - split_z - spigot_h + 1);
        wulst_cavity();
      }
      wulst_bosses();
      wulst_drip_lip();
    }
    // Schlauchkanal (Saug- und Druckschlauch) durch Mantel + Wulst
    translate([-hose_w/2, shell_or - 10, hose_z - hose_w/2])
      cube([hose_w, 16, hose_w]);
    // Sensorkabelkanal
    translate([0, shell_or - 10, cable_z]) rotate([-90, 0, 0])
      cylinder(d=cable_d, h=16);
    // Druckschlauch-Austritt nach oben
    translate([pressure_x, pressure_y, wulst_z1 - 8])
      cylinder(d=pressure_hole_d, h=14);
    // Kragenausschnitt fuer den Sensorkabelaustritt
    translate([-3.5, shell_or - 10, collar_z0 + 2])
      cube([7, 16, collar_h + 4]);
    // LST-Ankerloecher im Kragen
    lst_holes();
    // Deckelgewinde (Pilotbohrungen)
    for (x = [-boss_x, boss_x], z = boss_z)
      translate([x, shell_or, z]) rotate([-90, 0, 0])
        cylinder(d=boss_hole_d, h=wulst_y_outer - shell_or + 2);
  }
}

// ---------------------------------------------------------------------------
// Aussenschale gesamt (Vorschau; zum Drucken segmentieren!)
// ---------------------------------------------------------------------------
module outer_shell() {
  union() { shell_lower(); shell_upper(); }
}

// ---------------------------------------------------------------------------
// Rost / Auflagerost
// ---------------------------------------------------------------------------
module grid() {
  difference() {
    cylinder(r=grid_or, h=grid_t);
    translate([0, 0, -1])
      hole_grid(grid_or - grid_rim, grid_hole_d, grid_pitch, 0, grid_t + 2);
    // Durchlass fuer den Saugschlauch
    translate([0, 52, -1]) cylinder(d=14, h=grid_t + 2);
  }
}

// ---------------------------------------------------------------------------
// Innentopf mit Giessfuessen und Drainageloechern
// ---------------------------------------------------------------------------
module inner_pot() {
  union() {
    difference() {
      cylinder(r=pot_or, h=pot_h);
      translate([0, 0, pot_floor_t])
        cylinder(r=pot_ir, h=pot_h - pot_floor_t + 1);
      translate([0, 0, -1])
        hole_grid(pot_ir - 6, drain_hole_d, drain_pitch, 0, pot_floor_t + 2);
      // Schlauchdurchlass am Rand oben (+Y, Richtung Wulst)
      translate([-pot_hose_w/2, pot_ir - 1, pot_h - pot_hose_h])
        cube([pot_hose_w, (pot_or - pot_ir) + 2, pot_hose_h + 1]);
    }
    for (i = [0 : n_feet - 1])
      rotate([0, 0, i * 360 / n_feet])
        translate([foot_r - foot_d/2, 0, -foot_h])
          cube([foot_d, foot_w, foot_h + 1]);
  }
}

// ---------------------------------------------------------------------------
// Verteilerring (Top-Drip)
// ---------------------------------------------------------------------------
module ring_barb() {
  rotate([0, 0, ring_barb_dir])
    translate([ring_or - 1, 0, ring_h/2]) rotate([0, 90, 0]) {
      cylinder(d=ring_barb_od, h=ring_barb_len + 1);
      translate([0, 0, ring_barb_len*0.40]) cylinder(d=ring_barb_od + 0.9, h=1.2);
      translate([0, 0, ring_barb_len*0.70]) cylinder(d=ring_barb_od + 0.9, h=1.2);
    }
}

module distribution_ring() {
  difference() {
    union() {
      rotate_extrude()
        translate([ring_ir, 0, 0]) square([ring_or - ring_ir, ring_h]);
      ring_barb();
    }
    // innere Ringkammer
    rotate_extrude()
      translate([ring_ir + ring_wall, ring_wall, 0])
        square([ring_or - ring_ir - 2*ring_wall, ring_h - 2*ring_wall]);
    // Austrittsbohrungen nach unten/innen
    for (i = [0 : ring_holes - 1])
      rotate([0, 0, i * 360 / ring_holes])
        translate([0, ring_hole_r, -1]) cylinder(d=ring_hole_d, h=ring_wall + 2);
    // Schlauchbohrung im Stutzen
    rotate([0, 0, ring_barb_dir])
      translate([ring_ir - 1, 0, ring_h/2]) rotate([0, 90, 0])
        cylinder(d=ring_barb_id, h=(ring_or - ring_ir) + ring_barb_len + 2);
  }
}

// ---------------------------------------------------------------------------
// Wulstdeckel (flach gedruckt; lokal: X=Breite, Y=Hoehe, Z=Dicke)
// ---------------------------------------------------------------------------
lid_t = 4.0;
usb_y = 15.0;
led_y = 40.0;
lid_screw_y = [100 - (wulst_z0 + wulst_h/2), 234 - (wulst_z0 + wulst_h/2)];

module lid_footprint_2d() {
  offset(r=wulst_cr)
    square([wulst_w - 2*wulst_cr, wulst_h - 2*wulst_cr], center=true);
}

module wulst_lid() {
  difference() {
    rrect(wulst_w, wulst_h, lid_t, wulst_cr);
    // Dichtungsnut (umlaufend, auf der Dichtflaeche zum Wulst hin)
    translate([0, 0, lid_t - 1.3])
      linear_extrude(1.4)
        difference() {
          offset(delta=-4) lid_footprint_2d();
          offset(delta=-6) lid_footprint_2d();
        }
    // Verschraubung
    for (x = [-boss_x, boss_x], y = lid_screw_y)
      translate([x, y, -1]) cylinder(d=boss_hole_d, h=lid_t + 2);
    // USB-C
    translate([0, usb_y, -1]) rrect(usb_w, usb_h, lid_t + 2, 1.5);
    // LED-Fenster
    translate([0, led_y, -1]) cylinder(d=led_d, h=lid_t + 2);
  }
}

// ---------------------------------------------------------------------------
// Optionale Abdeckung des Substrats
// ---------------------------------------------------------------------------
module cover() {
  difference() {
    cylinder(d=cover_od, h=cover_t);
    translate([0, 0, -1]) cylinder(d=cover_hole, h=cover_t + 2);
    translate([-4, shell_or - 14, -1]) cube([8, 16, cover_t + 2]);
  }
}

// ---------------------------------------------------------------------------
// Kappe fuer den Einfuellstutzen (Drucklage +Z, offene Seite nach oben)
// ---------------------------------------------------------------------------
module fill_cap() {
  difference() {
    union() {
      cylinder(d=cap_od, h=cap_h);
      // zwei gegenueberliegende Greifrippen (greifen in den Mantel ein)
      for (rx = [cap_od/2 - cap_rib_t, -cap_od/2 - cap_rib_t])
        translate([rx, -cap_rib_w/2, 0]) cube([2*cap_rib_t, cap_rib_w, cap_h]);
    }
    // Sackloch (Klemmsitz auf dem Stutzen)
    translate([0, 0, cap_h - cap_depth])
      cylinder(d=cap_id, h=cap_depth + 1);
    // Lueftungsloch im Deckel (Druckausgleich)
    translate([0, 0, -1]) cylinder(d=cap_vent_d, h=cap_h + 2);
  }
}
