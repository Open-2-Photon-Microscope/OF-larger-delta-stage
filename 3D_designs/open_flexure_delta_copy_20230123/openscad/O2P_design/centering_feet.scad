module triangle(side_len, prism_len, corner_rad){
    rotate([270,0,0])hull(){
        cylinder(r=corner_rad, h=prism_len);
        rotate([0,0,60])translate([side_len-corner_rad*2,0,0])cylinder(r=corner_rad, h=prism_len);
        rotate([0,0,120])translate([side_len-corner_rad*2,0,0])cylinder(r=corner_rad, h=prism_len);
    }  
}



    cage_size = 21; //42mm / 2
module cage_adapter(){
    difference(){
intersection(){
    $fn=20;
difference(){
 translate([0,0,4]){   
cube([52,55,8],center=true);
 }
for(x=[-1*cage_size,cage_size]){
    for(y=[-1*cage_size,cage_size]){
    translate([x,y,-1]){
    cylinder(d=6.26,h=25,$fn=28);//h=12
    }//end translate
}//end for
}//end for
translate([0,0,5]){
cube([50,30,12],center=true);
cube([32,53,12],center=true);
}//end translate
}//end difference

translate([0,-60,0])rotate([0,0,45])cube(100); // a big cube to chop off pesky corners
} // end intersection
union(){
    translate([cage_size,-2*cage_size,5])triangle(2.5,200,0.1);
    translate([-1*cage_size,-2*cage_size,5])triangle(2.5,200,0.1);
}//end union
} //end difference
}//end module


//cage_adapter();
//difference(){
//union(){
  //  translate([0,0,3])cylinder(h=6,r=2, center=true, $fn=18);
//translate([0,0,0.2]){
//rotate([0,0,45])cube([3,cage_size*2.3,0.4], center=true);
//rotate([0,0,-45])cube([3,cage_size*2.3,0.4], center=true);
//} // end translate
//} // end union
    //translate([0,0,3])cylinder(r=1.5,h=6,center=true, $fn=18);
//} // end difference

module calibration_card(){
    difference(){
        union(){
        translate([0,0,0.2])cube([52,52,0.4],center=true);
            translate([0,0,2.5])cylinder(r=3,h=5,center=true,$fn=18);
        }// end union
        cylinder(r=2,h=11,center=true,$fn=18);
        for(x=[-1*cage_size,cage_size]){
            for(y=[-1*cage_size,cage_size]){
            translate([x,y,-1]){
                cylinder(d=6.26,h=25,$fn=28);//h=12
            }//end translate
            }//end for
        }//end for
    }// end module
}//end module

calibration_card();