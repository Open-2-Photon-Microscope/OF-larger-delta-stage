// Design for a 10mm riser

use <./stage_adaptor_base.scad>;
use <./delta_stage.scad>;
use <../openflexure-microscope/openscad/utilities.scad>;

difference(){
    stage_adaptor_base(height = 10, screws_center = true);
    each_stage_mounting_hole_without_center(z_translate = 0){trylinder_selftap(nominal_d=3, h=999);}
    each_stage_mounting_hole_just_center(z_translate = 2){cylinder(r=3.01, h=999,$fn=100);}
    each_stage_mounting_hole_just_center(z_translate = -1){cylinder(d=3, h=999,$fn=100);}
    cylinder(r=18.5, h=999,$fn=200); //hole for dish
}