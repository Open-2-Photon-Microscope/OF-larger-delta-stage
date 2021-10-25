/////////////////////////////////////////
// Lens Holder for Thor Lab Equipment  //
// This design holds a XX mm lens      //
// into a 30 mm cage system            //
// Design by F. Janiak, with support   //
// from M. Zimmermman and A. Chagas    //
//     CC BY SA 4.0                    // 
/////////////////////////////////////////

/// PARAMETERS FOR THE CUSTOMIZER ///

L_r = 9.1; // Lens Width was 15.5
S_r = 2; // Holding Screw Width (Defined here for M4 Bolts)

//Lens Support Dimension
L_x = 41;
L_y = 41;
L_z = 7;


////////////////////////////////////////////////////////////////////////

Rods = 15; // Rods Relative x/y Position to Center as defined by Thor Lab
R_r = 3.075; // Rods Radius as defined by Thor Lab - was 3.125
s_r = 1.25; // Rod Holding Screw Radius as defined by Thor Lab




module Base_pos(){
   cube ([L_x,L_y,L_z], center=true);  
   //translate([0,-L_y/2,-L_z/2]); 
   //cube ([47.95,L_y,L_z]); //fkj do mocowania
}
module Base_neg(){
    
    translate([0,0,-L_z/2-0.5]){cylinder ($fn=500, r=L_r-0.5, h=L_z+1);}//end translate
    translate([0,0,-L_z/2-0.5]){cylinder ($fn=500, r=L_r, h=2.5);}//end translate
   
    translate([-Rods,-Rods,-L_z/2-0.5]){cylinder ($fn=100, r=R_r, h=L_z+1);}//end translate
     translate([+Rods,-Rods,-L_z/2-0.5]){cylinder ($fn=100, r=R_r, h=L_z+1);}//end translate
      translate([-Rods,Rods,-L_z/2-0.5]){cylinder ($fn=100, r=R_r, h=L_z+1);}//end translate
       translate([+Rods,Rods,-L_z/2-0.5]){cylinder ($fn=100, r=R_r, h=L_z+1);}//end translate
     //  translate([+Rods+20,7.55,-L_z/2]){cylinder ($fn=100, r=2.15, h=L_z);}//mocowanie do mikroskopu  
    //   translate([+Rods+20,-7.55,-L_z/2]){cylinder ($fn=100, r=2.15, h=L_z);}//mocowanie do mikroskopu 
       
 //   translate([-L_x/2,0,0]){rotate ([0,90,0])cylinder ($fn=100, r=S_r, h=L_x+100);}
  //   translate([-L_x/2,12,0]){rotate ([0,90,0])cylinder ($fn=100, r=S_r/2, h=L_x+100);} //FKJ mocowanie
  //    translate([-L_x/2,-12,0]){rotate ([0,90,0])cylinder ($fn=100, r=S_r/2, h=L_x+100);} //FKJ mocowanie
    
  //   translate([0,-L_y/2,0]){rotate ([270,0,0])cylinder ($fn=100, r=S_r, h=L_y);}
     
  //    translate([Rods,L_y/2,0]){rotate ([90,0,0])cylinder ($fn=100, r=s_r, h=L_y/2-Rods);}
       translate([-Rods,L_y/2+0.5,0]){rotate ([90,0,0])cylinder ($fn=100, r=s_r, h=L_y/2-Rods);} //end translate
  //      translate([Rods,-L_y/2,0]){rotate ([270,0,0])cylinder ($fn=100, r=s_r, h=L_y/2-Rods);}
         translate([-Rods,-L_y/2-0.5,0]){rotate ([270,0,0])cylinder ($fn=100, r=s_r, h=L_y/2-Rods);}//end translate

}
difference() {
    Base_pos();
    Base_neg();
}

    
   