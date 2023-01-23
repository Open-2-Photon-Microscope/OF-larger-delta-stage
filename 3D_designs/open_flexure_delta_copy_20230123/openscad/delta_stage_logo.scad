module openflexure_delta_stage_logo(h=1, resize=[0,0]){
    // The full logo, including text
    // This is 47 mm tall in Inkscape, and exported using base units=mm
    // We resize it to be about the right size for the microscope
    // The origin is set to x=38 to centre the emblem on x=0
    // I don't understand the Y origin value...
    linear_extrude(h) scale(1.3) import("openflexure_delta_stage_logo.dxf", origin=[38,3]);
}