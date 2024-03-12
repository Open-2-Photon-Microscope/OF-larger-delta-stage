/*
  Useful settings/parameters for the OpenFlexure fibre stage
*/

use <../openflexure-microscope/openscad/reflection_illuminator.scad>;
version_numstring = "1.2.1"; 

// Set the overall geometry
leg_strut_l = 32; // inner width of the legs
stage_r = 25; // distance from the centre to the edge of the stage
flex_z1 = 0; // height of lower flexures
flex_z2 = 70; // height of upper flexures

// Thickness of legs
leg_t = 5;

// Set the length of the actuating levers
xy_gain = 2; // ratio of stage motion to Z motion
lever_l = (flex_z2 - flex_z1)/xy_gain;
nut_y = lever_l + 12;

// Motor lugs
motor_lugs = true;

// Condenser mount
transmission_illumination = false;

// Reflection illumination - The hole cut out the side for the reflection illuminator
reflection_illumination = false; 

// Stage connectors - the mounts to connect the stage to the base
stage_connectors = false;

//Objective mount - the dovetail for attaching the optics module
optics_module_mount = true;

// Flexure dimensions - good for PLA and ~0.5mm nozzle
zflex = [6, 1.5, 0.75]; //dimensions of flexure
flex_a = 0.1; //angle through which flexures are bent, radians
dz = 0.5; //thickness before a bridge is printable-on

actuator_h = 30; //height of actuator columns (~screw length)
actuator_travel = (nut_y - zflex[1]/2)*flex_a;

wall_t = 1.6;
d=0.05;

// Mounting stuff
// Mounting holes should be 60 degrees out from the legs (i.e. in between)
// If you extend the line of the solid anchor part in the middle (where each leg
// joins the casing) out sideways, to the middle of the vertical part of the
// leg, then take the midpoint of the line joining each pair, that's the hole)
mounting_hole_r = sin(30)*stage_r + sin(60)*(leg_strut_l/2+zflex[1]+leg_t/2);
// The position of the mounting point between the base and main body (from centre at each 120 degree position of the actuators)
mounting_point = 87;

// Objective mount
objective_mount_y = 18; // y position of clip for optics
objective_mount_back_y = stage_r + wall_t; //back of objective mount
objective_mount_nose_w = 6; // width of the pointy end of the mount

sample_z = 65; // height of the top of the stage
z_flexures_z1 = 8; // height of the lower Z flexure
z_flexures_z2 = min(sample_z - 12, 35); // " upper "

// Feet
feet_endstops = false;
foot_height=feet_endstops?15:15; //the endstops need a bit of extra height (or not)
endstop_extra_ringheight=feet_endstops?1:0;

//Casing 
casing_height = actuator_h+actuator_travel + 5; //flex_z2-24; //the maximum height of the lever casing and 'joining together' casing
casing_radius = nut_y; //the outside radius (to the point) of the hexagon used to join the casing together

// size of cutout for fl cube
top_cutout_w = stage_r/2 + 2*wall_t; // As big as we can get at height 'wall_h' without bridging a corner
mid_cutout_w = illuminator_width() + 1;
bottom_cutout_w = illuminator_width() + 4;

// Base
wall_thickness = 2;
simple_base_height = 35;
base_height = 80;
base_cutout_tolerance = 0.5;
raspi_board = [56,85,16]; // The actual size of the RPi
casing_apothem = casing_radius*sqrt(3)/2; // The apothem of the hexagon used to join up the legs
USB_ethernet_window = [raspi_board[0],100,raspi_board[2]+6]; //The back window for the RPi
power_HDMI_window  = [100,45-3.5,14]; //The side window for the RPi
raspi_standoff = 7; //How high the RPi is from the base (governed by the standoff screw size)
sangaboard = [56,68,25]; // The actual size of the Sangaboard
raspi_center = [0,10,raspi_board[2]/2+raspi_standoff]; // Where the centre of the Raspberry Pi is in its final position
standoff_height = 20; //The height of the standoff between the Rpi and the Sangaboard
sangaboard_center = raspi_center+[0,(raspi_board[1]/2-sangaboard[1]/2),(sangaboard[2]/2-raspi_board[2]/2+standoff_height)]; // Where the centre of the Raspberry Pi is in its final position
sangaboard_window = [100,power_HDMI_window[1],20]; // The back window of Sangaboard
