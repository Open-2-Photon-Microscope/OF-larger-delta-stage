$fn=3;

m = 5.5;

difference(){
    cube([35,10,5]);
    translate([5,5,0])cylinder(d=m-0.1,h=10,center=true);
    translate([10,5,0])cylinder(d=m,h=10,center=true);
    translate([15,5,0])cylinder(d=m+.1,h=10,center=true);
    translate([20,5,0])cylinder(d=m+.2,h=10,center=true);
    translate([25,5,0])cylinder(d=m+.3,h=10,center=true);
    translate([30,5,0])cylinder(d=m+.4,h=10,center=true);
}