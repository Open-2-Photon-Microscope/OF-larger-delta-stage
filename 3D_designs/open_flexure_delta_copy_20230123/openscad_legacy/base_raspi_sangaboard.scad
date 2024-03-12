include <parameters.scad> //Delta-stage params
use <../openflexure-microscope/openscad/utilities.scad>;
use <../openflexure-microscope/openscad/compact_nut_seat.scad>;
use <delta_stage.scad>
use <delta_stage_logo.scad>;
use <../openflexure-microscope/openscad/logo.scad>;

module base_projection(){
    projection(cut=true){
        union(){
            difference(){
                union(){    // casing around the leg&lever
                    each_lever() minkowski(){
                        leg_and_lever_clearance();
                        cylinder(r1=wall_t, r2=0.5, h=0.9);
                    }
                    reflect([1,0,0]){
                        translate([-(casing_radius+1),0,0])cube([(casing_radius+1),casing_apothem,10]); // This fills in space in the side that are then later cut to give access to side RPi connections.
                    }
                }
                translate([0,sangaboard_center[1]-sangaboard[1]/2,0])cube([100,sangaboard[1],10]); // This squares off the side wall for access to Sangaboard connections
                translate([-(casing_radius+1),2.5,0])cube([(casing_radius+1),casing_apothem,10]); // This squares off the side wall for access to RPi connections
                translate(raspi_center+[0,-(raspi_board[1]+2),-raspi_standoff])cube(raspi_board+[10,0,0],center=true); //This squares off the back wall for access to RPi connections
            }
            // This fills in where the RPi goes with extra space at the front of the microscope as the Sangaboard is bigger that the RPi in that dimension
            translate(raspi_center-[0,-2,raspi_standoff]) cube(raspi_board + [1,8,0], center =true);
        }
    }
}

module feet_projection() {
    projection(cut=true){
        // casing for the actuator
        each_lever() translate([0, nut_y, -49]) screw_seat_shell(h=actuator_h + 99);
    }  
}

module base_extrusion(h) {
    linear_extrude(height=h) {
        union() {
            feet_projection();
            base_projection();
        }
    }
}

module base_hollow(cutout_tolerance=1) {
    difference(){
        union(){
        // Base extrusion, but with an outer wall wall_thickness thick
            minkowski(){
                base_extrusion(base_height);
                cylinder(r=wall_thickness+cutout_tolerance,h=1);
            }
            stage_connection();
        }
        // Base extrusion, but with an outer wall cutout_tolerance thick
        translate([0, 0, wall_thickness]) minkowski(){
            base_extrusion(base_height);
            cylinder(r=cutout_tolerance,h=1);
        }
    }
}

module foot_stands(height=base_height, cutout_tolerance=1) {
    // Creates 3 ledges approximately half the foot size such that the main body of the microscope will start 2mm below the height of the base.
    translate([0,0,height-foot_height+1]){
        each_lever(){
            translate([0, nut_y, 0]){
                intersection(){ 
                    hull(){
                        difference(){
                            minkowski(){
                                linear_extrude(d){
                                    projection(){
                                        screw_seat_shell(10);
                                    }
                                }
                                cylinder(r=cutout_tolerance,h=d);
                            }
                            translate([0,-52.5,0])cube([100,100,100],center = true);
                        }
                        translate([0,10,-20]) cube([30,d,d],center=true);
                    }
                    translate([0,0,-50]){
                        minkowski(){
                            screw_seat_shell(100);
                            cylinder(r=cutout_tolerance+1,h=d);
                        }
                    }
                }
            }
        }    
    }
}

//The walls and floor of the base
module base() {
    union(){
        foot_stands(cutout_tolerance=base_cutout_tolerance);
        base_hollow(cutout_tolerance=base_cutout_tolerance);
    }
}

// All the windows to pass cables through
module window_cubes() {
    //RPi windows
    // Back window
    translate(raspi_center+[0,-50,-raspi_board[2]/2+USB_ethernet_window[2]/2-3]) cube(USB_ethernet_window,center=true);

    //Side window
    translate(raspi_center+[-power_HDMI_window[0]/2,raspi_board[1]/2-power_HDMI_window[1]/2-3.5,-raspi_board[2]/2+power_HDMI_window[2]/2-1]) cube(power_HDMI_window,center = true);
    
    //Vents
    translate([sangaboard_center[0]+50,sangaboard_center[1]+5/2,raspi_center[2]])repeat(delta=[0,(sangaboard[1]-5)/14,0],N=15, center= true) cube([100,1.5,power_HDMI_window[2]],center=true);

    //SD card access
    translate(raspi_center+[0,raspi_board[1]/2+5,-10])cube([20,25,20], center=true);


    //Sangaboard windows
    // Back window
    translate(sangaboard_center-[0,50,0]) rotate([0,0,90])cube(sangaboard_window, center=true);

    //Side windows
    translate([raspi_center[0]-power_HDMI_window[0]/2,raspi_center[1]+raspi_board[1]/2-power_HDMI_window[1]/2-3.5,sangaboard_center[2]-sangaboard[2]/2+power_HDMI_window[2]/2+3]) cube(power_HDMI_window+[0,0,6], center = true);
    translate(sangaboard_center+[50,5/2,-sangaboard[2]/2+power_HDMI_window[2]/2+3]) cube([100,sangaboard[1]-5,power_HDMI_window[2]+6],center = true);
    //Reflection gap
    rotate([0,0,-60])translate([0,50,base_height-9])cube([bottom_cutout_w,100,20],center=true);
}

module pi_supports(){
    // position supports for each of the pi's mounting screws
    translate(raspi_center+[0,raspi_center[1],-raspi_center[2]]) repeat([49,0,0],2, center=true) repeat([0,58,0], 2,center=true) children();
}

// The four mounting holes underneath the Raspberry Pi.  
module raspi_supports(){
    difference(){
        pi_supports() cylinder(h=raspi_standoff, d=7);
        pi_supports() trylinder_selftap(2.5, h=999, center=true);
    }
}

module stage_connection(height=base_height){
    // Creates 3 mounting posts to connect to the main body. The top of the post is in line with the top of the base, with the cutout circle 2mm down such that the main body sits 2mm under the top of the base.
    translate([0,0,height+1])
    {
        each_base_mounting_point(){
            difference(){
                hull(){
                    translate([0,0,-2*d])repeat([0,0,-10],2){
                        minkowski(){
                            cube([10,10,d], center = true);
                            cylinder(r = 1, h = d, $fn = 50);
                        }
                    }
                    translate([0,nut_y+stage_r-mounting_point,-20]){
                        difference(){                                
                            linear_extrude(20){
                                projection(){
                                    minkowski(){
                                        screw_seat_shell(10);
                                        cylinder(r=wall_thickness,h=d);
                                    }
                                }
                            }
                        translate([-50,-99,-50])cube([100,100,100]);
                        }
                    }
                }
                translate([0,0,-2])cylinder(d = 8.5, h = 2, $fn=50);
                translate([0,0,-8+d])cylinder(d= 3.5, h = 8, $fn=50);
                translate([0,0,-10-8+d])trylinder_selftap(3, h=20, center=true);
                hull()repeat([0,100,0],2) translate([0,0,-8]) cylinder(d=6.9,h=2.8,$fn=6); 
            }
        }
    }
}

// Used to show position of sangaboard
module sangaboard(){
    translate(sangaboard_center) cube(sangaboard, center =true);
}

//Used to show position of raspberry pi
module raspi(){
    translate(raspi_center)cube(raspi_board, center = true);
}

module logos(){
    //The OSHW and OpenFlexure logos (goes on back of the base)
    rotate(-90)translate([casing_apothem-3.5,8,base_height*0.7])rotate([90,0,-90])scale([0.2,0.2,1])oshw_logo_and_text(version_numstring);
    mirror([1,0,0])rotate(-90)translate([casing_apothem-3.5,4,base_height*0.8])rotate([90,0,-90])scale([0.2,0.2,1])openflexure_delta_stage_logo();
}

module base_windowed() {
    union(){
        difference() {
            base();
            window_cubes();
            translate([-(casing_radius+2),0,base_height-5])cube([casing_radius+2,sangaboard_center[1]+sangaboard[1]/2-sangaboard_window[1]/2,10]); // cutout at top for the base to pass under the mircoscope (side)
            translate([0,sangaboard_center[1]-sangaboard[1]/2,base_height-5])cube([100,sangaboard[1]/2,10]); // cutout at top for the base to pass under the mircoscope (side)
            translate(raspi_center+[0,-(raspi_board[1]+2),base_height-5-raspi_standoff])cube(raspi_board+[10,0,0],center=true); //cutout at top for the base to pass under the mircoscope (back)
            logos();
        }
        raspi_supports();
    }
}


// To build the raspberry pi and sangaboard base
base_windowed();


//#raspi();  // uncomment to see where the raspberry pi fits
//#sangaboard(); //uncomment to see where the sangaboard fits
