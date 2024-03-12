//base design for stage adaptors for the delta stage.  Use this module and create holes/shapes for the sample holder you wish to use with the delta stage.

use <./delta_stage.scad>;


module stage_adaptor_base(height = 10, screws_center = false){
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