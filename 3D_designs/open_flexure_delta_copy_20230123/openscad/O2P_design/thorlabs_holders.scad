// Holders for attaching the delta stage to Thorlabs Columns via m6 screws

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

//triple(10);

module holder_slant(){
    translate([0,-9.5,7.5])difference(){
        translate([0,2,5]){intersection(){
            translate([0,0,-15])cube([36,15,25], center=true);
            translate([0,10,5]){rotate([45,0,0])cube([36,50,50],center=true);}
        }//end intersection
        }// end translate
    union(){
    cylinder(h=50,d=6.26,center=true);
    translate([13,0,0])cylinder(h=50,d=6.26,center=true);
    translate([-13,0,0])cylinder(h=50,d=6.26,center=true);
    }// end union
} // end difference
} // end module

holder_slant();

module triple_slant(radius){
    union(){
    translate([0,-1*radius,0])holder_slant();
    rotate([0,0,120])translate([0,-1*radius,0])holder_slant();
    rotate([0,0,-120])translate([0,-1*radius,0])holder_slant();
    } // end union
} //end module

//triple_slant(15);
