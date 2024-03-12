// Design for a 55mm diameter petri dish holder

use <./delta_stage.scad>;
use <../openflexure-microscope/openscad/utilities.scad>;

difference(){
    cylinder(r=29, h = 9,$fn=200);
    each_stage_mounting_hole_just_center(z_translate=-1)cylinder(d=3,h=999,$fn=100);
    each_stage_mounting_hole_just_center(z_translate=1)cylinder(r=3,h=999,$fn=100);

    cylinder(r=18.5, h=999,$fn=100);  //bottom hole
    translate([0,0,4])cylinder(r=55/2, h=999,$fn=200); //hole for dish
}