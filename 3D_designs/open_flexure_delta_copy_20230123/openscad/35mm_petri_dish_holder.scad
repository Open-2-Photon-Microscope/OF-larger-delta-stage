// Design for a 35mm diameter petri dish holder

use <./stage_adaptor_base.scad>;
use <./delta_stage.scad>;
use <../openflexure-microscope/openscad/utilities.scad>;

difference(){
    stage_adaptor_base(height = 1+7.5, screws_center=false);
    each_stage_mounting_hole_without_center(z_translate = 0){trylinder_selftap(nominal_d=3, h=999);}
    each_stage_mounting_hole_just_center(z_translate = 2){cylinder(r=3.01, h=999,$fn=100);}
    each_stage_mounting_hole_just_center(z_translate = -1){cylinder(d=3, h=999,$fn=100);}

    cylinder(r=24/2, h=999);  //bottom hole
    translate([0,0,1])cylinder(r=35.5/2, h=999,$fn=200); //hole for dish
}