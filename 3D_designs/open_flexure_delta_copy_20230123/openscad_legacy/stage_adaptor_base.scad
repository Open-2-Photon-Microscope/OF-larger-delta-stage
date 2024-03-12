//base design for stage adaptors for the delta stage.  Use this module and create holes/shapes for the sample holder you wish to use with the delta stage.

use <./delta_stage.scad>;
include <parameters.scad> //Delta-stage params
use <z_axis.scad>;
use <delta_stage_logo.scad>;
use <../openflexure-microscope/openscad/utilities.scad>;
use <../openflexure-microscope/openscad/compact_nut_seat.scad>;
use <../openflexure-microscope/openscad/reflection_illuminator.scad>;
use <../openflexure-microscope/openscad/z_axis.scad>;
use <../openflexure-microscope/openscad/illumination.scad>;
use <../openflexure-microscope/openscad/logo.scad>;


tol=0.1;


module stage_adaptor_base(height = 4, screws_center = false){
    //height: the height of the riser
    //screws_centre: whether there should be two mounting screw points per leg (leaving the centre one for sample clip) (false, default) or one mounting point in the center (true)
difference(){
    union(){
        // Fill in the stage
        hull(){
            intersection(){
                hull() stage_flexures(h=999,z=0);
                stage_edges(z=0, h = height);
            }
            intersection(){
                stage_flexures(h=999,z=0);
                hull() stage_edges(z=0, h = height);
            }
        }
    }
/*  */
    
    
    }
}




difference(){
stage_adaptor_base(screws_center=false);

    translate([0,0,-1]){
        scale([0.75,0.75,1.5]){
            stage_adaptor_base(screws_center=false);}//end scale
    }//end translate

for(angle = [0 : 120 : 240]){
    rotate([0,0,angle]){
        translate([0,-24,+0.1]){
            cylinder(d=5+2*tol,h=4,$fn=30);
        }//end rotate
    }//end translate
}//end for

for(angle = [0 : 120 : 240]){
    rotate([0,0,angle]){
        translate([0,22,+0.1]){
            cylinder(d=5+2*tol,h=4,$fn=30);
        }//end rotate
    }//end translate
}//end for

translate([0,0,-80]){stage_mounting_holes(z_translate=flex_z2+4*dz);
}//end translate
}//end difference


