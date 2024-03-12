//MAGNET HOLES
// current project uses magnets of diameter 3, height 2mm

module magnet_holes(radius){
    translate([0,0,1])union(){ //d=3.3 for tolerance
    translate([0,-1*radius,0])cylinder(d=3.3,h=2,center=true, $fn=12);
    rotate([0,0,120])translate([0,-1*radius,0])cylinder(d=3.3,h=2,center=true, $fn=12);
    rotate([0,0,-120])translate([0,-1*radius,0])cylinder(d=3.3,h=2,center=true, $fn=12);
    } // end union
} //end module

magnet_holes(10); // just an illustration