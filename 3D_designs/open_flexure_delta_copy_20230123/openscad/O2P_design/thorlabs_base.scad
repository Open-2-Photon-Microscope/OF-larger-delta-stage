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
 translate([0,0,5]){   
cube([50.5,74,10],center=true);
 }
for(x=[-1*cage_size,cage_size]){
    for(y=[-1*cage_size,cage_size]){
    translate([x,y,-1]){
    cylinder(d=6.26,h=25);//h=12
    }//end translate
}//end for
}//end for
translate([0,0,5]){
cube([55,30,12],center=true);
cube([32,80,12],center=true);
}//end translate
}//end difference

translate([0,-60,0])rotate([0,0,45])cube(100); // a big cube to chop off pesky corners
} // end intersection
union(){
    translate([cage_size,-1*cage_size,5])triangle(2.5,42,0.1);
    translate([-1*cage_size,-1*cage_size,5])triangle(2.5,42,0.1);
}//end union
} //end difference
}//end module


cage_adapter();

