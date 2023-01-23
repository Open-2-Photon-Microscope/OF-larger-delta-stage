/******************************************************************
*                                                                 *
* OpenFlexure Delta Stage: Z axis                                 *
*                                                                 *
* This is the Z axis for the OpenFlexure Delta Stage.             *
* It also contains the fitting for the optics module to attach    *
* it to the objective mount, as the objective mount is part of    *
* the Z axis assembly.                                            *
*                                                                 *
* (c) Richard Bowman, January 2018                                *
* Released under the CERN Open Hardware License                   *
*                                                                 *
******************************************************************/

use <../openflexure-microscope/openscad/utilities.scad>;
include <parameters.scad>;

module each_om_contact_plane(){
    // This transform puts y=0 in the plane of contact between the
    // optics module and the mount for it, with the origin at the
    // nominal corner of the wedge.
    reflect([1,0,0]) translate([-objective_mount_nose_w/2,objective_mount_y,0])
                rotate(135) children();
}

module objective_mount(){
    // The fitting to which the optics module is attached
    h = z_flexures_z2 + 4*sqrt(2);
    overlap = 4; // we have this much contact between 
                 // the mount and the wedge on the optics module.
    roc=1.5; // radius of curvature of the arms
    w = objective_mount_nose_w + 2*overlap + 4;//+2*roc; //overall width
    difference(){
        hull(){
            // the back of the mount
            translate([-w/2,objective_mount_back_y,0]) cube([w,d,h]);
            // the front of the mount (this makes contact with the optics module)
            each_om_contact_plane() translate([0,overlap-d,0]) cube([2*roc,d,h]);
        }
        
        // bolt slot to mount objective
        hull(){
            translate([0,0,z_flexures_z1+8]) rotate([-90,0,0]) cylinder(d=3.5, h=999);
            translate([0,0,z_flexures_z2-5]) rotate([-90,0,0]) cylinder(d=3.5, h=999);
        }
        
        // make the bolt slot keyhole-shaped to allow the screw to be easily inserted
        translate([0,0,z_flexures_z1+6]) rotate([-90,0,0]) cylinder(d=6.5, h=999);
        
        objective_fitting_wedge(h=999,nose_shift=-0.25,center=true);

        // cut out the back so it fits in the available space
        //reflect([1,0,0]) translate([objective_mount_back_y,0,-99]) rotate(45) cube(999);

    }
    // Nice rounded fronts either side
    each_om_contact_plane() translate([roc,overlap,0]) cylinder(r=roc,h=h);
}

function objective_mount_screw_pos() = [0, objective_mount_back_y, (z_flexures_z2 + z_flexures_z1)/2];

module objective_mount_screw(){
    translate(objective_mount_screw_pos()) rotate([-90,0,0]){
        cylinder(r=3, h=2.5);
        mirror([0,0,1]) cylinder(d=3, h=12);
    }
}

module objective_fitting_wedge(h=z_flexures_z2+4, nose_shift=0.2, center=false){
    // A trapezoidal wedge that clamps onto the objective mount.  
    // NB you must subtract the objective_fitting_cutout from this to allow
    // the screw and nut to be attached.
    // NB nose_shift moves the tip of the wedge in the -y direction (i.e. increases
    // the gap at the tip, if we are making the optics module).  If subtracting this
    // to make a mount for the optics module, use nose_shift < 0
    nw = objective_mount_nose_w; //width of the pointy end
    translate([0,objective_mount_y,0]) mirror([0,1,0]) hull(){
        translate([-nw/2-nose_shift,nose_shift,center?-h/2:0]) cube([nw+2*nose_shift,d,h]);
        reflect([1,0,0]) translate([-nw/2-5+sqrt(2), 5+sqrt(2), 0]) 
                cylinder(r=2, h=h, $fn=16, center=center);
    }
}

module z_motor_clearance(){
    // clearance for the motor and gears, to be subtracted from the condenser mount
    // This also labels it as "Z"
    translate([0,z_nut_y,0]) rotate([z_actuator_tilt,0,0]) {
        translate([0,0,actuator_h+z_actuator_travel+2-1]) rotate(180){
            motor_and_gear_clearance(gear_h=11);
            linear_extrude(1, center=true) translate([0,15]) {
                text("Z", size=10, font="Sans", halign="center", valign="baseline");
            }
        }
    }
}
