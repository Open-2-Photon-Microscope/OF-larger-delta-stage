// Alignment tool for zeroing the larger delta stage for open 2P

use <magnet_holes.scad>
use <holders.scad>
use <thorlabs_holders.scad>
use <top_stage.scad>

module archway(x,y,z, down){
    intersection(){
        cube([x,y,z],center=true);
        translate([0,0,down]){rotate([0,45,0])cube(z*2,center=true);}
    }// end difference
}// end archway module

//archway(50,60,40,20);

module calibration_body(){
    height = 55;
difference(){
union(){
    hexagon(73.5,height,5);
translate([0,0,-10])triple_slant(62);
} // end union
rotate([0,0,60])union(){
    translate([0,-73.5,0-20])archway(50,50,40,20);
    rotate([0,0,120])translate([0,-73.5,-20])archway(50,50,40,20);
    rotate([0,0,-120])translate([0,-73.5,-20])archway(50,50,40,20);
}// end union
translate([0,0,-1])holes(71, 6, 2.2, 3.3);
}// end difference
translate([0,0,2.5-height])intersection(){
    cylinder(h=5,r=73.5,center=true,$fn=6);
    difference(){
        union(){
            cube([10,150,5],center=true);
            cube([150,10,5], center=true);
        } // end union
        union(){
            cube([1,150,5],center=true);
            cube([150,1,5], center=true);
        } // end union
    }// end difference
}// end intersection

}// end module calibration_body

module holes(radius, number, height, hole_width){
    for(i=[0:360/number:360]){
        rotate([0,0,i]){
        //echo(i);
        translate([radius,0,0])cylinder(height,d = hole_width, $fn=18, center=true);
        }// end rotate
    }// end for
}// end module holes

//holes(10, 6, 5, 1.5);

module calibration_top(){
    
    translate([0,0,-4]){
        rotate([180,0,0])difference(){
        //hexagon(40,4,6);
        translate([0,0,-2])cylinder(h=4,r=40,center=true,$fn=6);
        union(){
            translate([0,0,-2])magnet_holes(32);
            holes(15,4,10,3.3);
            //translate([0,0,-3]){rotate([0,0,45])holes(15,4,2,5.6);}
            rotate([0,0,45])holes(15,4,10,3.5); // screw holes
            rotate([0,0,45])cube([20,20,6.2],center=true);
        }// end union
    } // end difference
}// end translation

}// end calibration_top module


module top_cap(){ // has slits and screw holes only
    slit_thickness = 0.2;  //changed from 1mm
    difference(){
        translate([0,0,-2.5])cylinder(h=5,r=40, center=true, $fn=6);
        difference(){
        union(){
            translate([0,0,-1.5]){rotate([0,0,45])holes(15,4,3,6);
            rotate([0,0,45])holes(15,4,10,3.5);}//end translate
            translate([0,0,-2.5])cube([slit_thickness,40,10],center=true);
            translate([0,0,-2.5])cube([40,slit_thickness,10],center=true);
        }// end union
            rotate([0,0,40])cube([20,20,5],center=true); // blocks light going too far
    }//end difference
    }//end difference
}// end module top_cap


module full_top(){
union(){
    translate([0,0,5])top_cap();
    calibration_top();
}//end union
}// end module full_top


calibration_body();

//full_top();