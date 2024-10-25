// SAMPLE STAGE TOPPER / ALIGNER
// Aligner to be used in conjunction with alignment card
use <magnet_holes.scad>
use <holders.scad>
use <chamber.scad>

module hexagon(radius,height,thickness){
    translate([0,0,-0.5*height])difference(){
        cylinder(r=radius,h=height,center=true,$fn=6);
        cylinder(r=radius-thickness,h=height,center=true,$fn=6);
    } // end difference
}// end module

module alignment_guide(height, radius){ // used in alignment top
    difference(){
        union(){
            translate([0,0,-4+(height/2)])cylinder(h=height, r=2, center=true, $fn=18);
            translate([0,0,-3.7]){
                cube([2*radius-5,3,0.6], center=true);
                rotate([0,0,90])cube([2*radius-20,3,0.6], center=true);
            }//end translate
        } // end union
        translate([0,0,-4+(height/2)])cylinder(h=height, r=1.5, center=true, $fn=18);
    }// end difference
}// end module

module alignment_top(){
// here's the hexagonal stage-topper
difference(){
hexagon(40,4,6);
translate([0,0,-2])magnet_holes(32);
} // end difference

alignment_guide(4,40);
} // end module

//alignment_top(); // used to roughly align the 

module spirit_level(height, radius){
    translate([0,0,-0.5*4])difference(){
        cylinder(r=40,h=4,center=true,$fn=6);
        translate([12.5,5,0])cylinder(d=5.9,h=30,center=true,$fn=3);
        translate([-12.5,5,0])cylinder(d=5.9,h=30,center=true,$fn=3);
        magnet_holes(32);
        }// end difference
}// end module spirit_level

//spirit_level();

module slide_holder_top(y_offset=15, z_offset=0){
    translate([0,0,-4]){
        rotate([180,0,0])difference(){
        hexagon(40,4,6);
        translate([0,0,-2])magnet_holes(32);
        translate([0,-y_offset,-5.5-z_offset])cube([80,29.8,2.5],center=true);
    } // end difference
}// end translate
    translate([0,y_offset,1+z_offset])mic_slide(); // offset Y may be useful
}// end module slide_holder_top

slide_holder_top(y_offset=0,z_offset=-2.2);

module ch_hold(){
    difference(){
        translate([0,0,-0.5])cube([28,58,4],center=true);
        scale(1.03)egg_chamber();
        cube(14, center=true);
    }//end difference
}//end module ch_hold

//ch_hold();

module cham_holder_top(y_offset=0){
    difference(){
    translate([0,0,-4]){
        rotate([180,0,0])difference(){
        hexagon(40,4,6);
        translate([0,0,-2])magnet_holes(32);
    } // end difference
}// end translate
translate([0,y_offset,-2]){rotate([0,0,90])cube([28,58,4],center=true);}
}// another difference
    translate([0,y_offset,-1.5]){rotate([0,0,90])ch_hold();} // offset Y may be useful
}// end module cham_holder_top

//cham_holder_top(15);
//cham_holder_top(0);
