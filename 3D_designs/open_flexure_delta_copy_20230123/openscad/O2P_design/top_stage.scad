// SAMPLE STAGE TOPPER / ALIGNER
// Aligner to be used in conjunction with alignment card
use <magnet_holes.scad>
use <holders.scad>

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

module slide_holder_top(){
    translate([0,0,-4]){
        rotate([180,0,0])difference(){
        hexagon(40,4,6);
        translate([0,0,-2])magnet_holes(32);
    } // end difference
}// end translate
    translate([0,0,1])mic_slide();
}// end module slide_holder_top

slide_holder_top();