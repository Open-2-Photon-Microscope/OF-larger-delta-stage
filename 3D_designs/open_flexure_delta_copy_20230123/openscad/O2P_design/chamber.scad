//oocyte chamber
//updated by AM Chagas 20210506 -> larger grid
//designed by AM Chagas 20181001 CC BY 4.0 license
//inspired on the design from J Menzies.

wellx = 0.92;//0.3
welly = 0.92;//0.7
wellz = 0.22;

interwell = 0.4;

nwellsx = 10;
nwellsy = 10;

platey = wellx*nwellsx*5+8;//10

platex = welly*nwellsy*1.5+12;//14  
platez = 3.2        ;

//nwellsx = 10;
//nwellsy = 20;

landmarks = 1;

echo(platey);
echo(platex);
echo(platez);


tol = 0.1;
$fn=20;
module egg_chamber(){

/*
module grid(){
    for (x = [0:nwellsx-1]){
        for (y = [0:nwellsy-1]){
            translate([x*(wellx+interwell),y*(welly+interwell),0]){
                cube([wellx,welly,wellz],center=true);
                }//end translate
            }//end for y
    }//end for x
}//end module
*/
module grid(wellx=wellx,welly=welly,holeThrough=0){
    for (x = [-nwellsx/2+0.5:nwellsx/2-0.5]){
        for (y = [-nwellsy/2+0.5:nwellsy/2-0.5]){
            translate([x*(wellx+interwell),y*(welly+interwell),platez/2-wellz/2+0.01]){
                if(holeThrough==1){
                    cube([wellx,welly,wellz+10],center=true);
                    }//endif
                else{
                 cube([wellx,welly,wellz],center=true);
                    }
                }//end translate
            }//end for y
    }//end for x
}//end module




difference(){

//translate([-platex/2+5,-platey/2+5,-platez+wellz-0.001]){
cube([platex,platey,platez],center=true);

//}

/*
translate([0,0,0.2]){
cube([wellx*nwellsx*2+8,welly*nwellsy*2,platez],center=true);
}

*/
//    translate([0,0,-0.5]){
//        minkowski(){
//            sphere(d=0.5);
//cube([18,14,0.5],center=true);    
//        }
//}//end translate

grid(holeThrough=0);

}//end difference
if(landmarks==1){

for (x=[-platex/2,platex/2]){
translate([x,0,0.4]){
cube([2,2,4],center=true);
}//end translate
}//end for

for(y=[-platey/2,platey/2]){
translate([0,y,0.4]){
cube([2,2,4],center=true);
}//end translate
}//end for
}
} // end module egg_chamber

egg_chamber();

/*
translate([-9.5,0,0.05]){
cube([4,15,platez],center=true);
}

translate([9.5,0,0.05]){
cube([4,15,platez],center=true);
}
*/