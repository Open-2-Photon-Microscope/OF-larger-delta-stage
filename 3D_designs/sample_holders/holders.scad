//models of the glass pieces used to hold samples
// and respective holders

tol = 0.1;
$fn = 30;

wall_t = 2;

//slide 1 ("traditional")
mic_slide_l = 75.7;
mic_slide_w = 25.9;
mic_slide_h = 1.1;


//slide 2 (slide cover)
mc_s = 22;

//slide 3 (slide cover round)
mc_d = 21.7;
mc_h = 0.15;


module mic_slide(){
    difference(){
    cube([mic_slide_l+2*wall_t,mic_slide_w+2*wall_t,mic_slide_h+mic_slide_h+0.2],center=true);
  union(){
    translate([0,0,wall_t/2]){
        cube([mic_slide_l,mic_slide_w,wall_t],center=true);
    }//end translate
    
    translate([0,0,0]){
        cube([mic_slide_l-wall_t,mic_slide_w-wall_t,mic_slide_h+10],center=true);
    }//end translate
    translate([0,0,wall_t/2]){
        cube([mic_slide_l*0.8,mic_slide_w+10,wall_t],center=true);
    }//end translate
}//end union
}//end difference
}//end module

//mic_slide();