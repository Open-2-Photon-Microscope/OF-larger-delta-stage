module holder(){
    translate([0,-9.5,0])difference(){
        translate([0,2,5])cube([36,15,10], center=true);
    union(){
    cylinder(h=20,d=6.26,center=true);
    translate([13,0,0])cylinder(h=20,d=6.26,center=true);
    translate([-13,0,0])cylinder(h=20,d=6.26,center=true);
    }// end union
} // end difference
} // end module

//holder();

module triple(radius){
    union(){
    translate([0,-1*radius,0])holder();
    rotate([0,0,120])translate([0,-1*radius,0])holder();
    rotate([0,0,-120])translate([0,-1*radius,0])holder();
    } // end union
} //end module

triple(10);