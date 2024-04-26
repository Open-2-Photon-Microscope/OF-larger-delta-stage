##Part 1: Assembling Hardware
###1.1 Delta Stage  
*This is the part that will be holding the sample.*

1. To get started, download our [custom body stl file from github](https://github.com/Open-2-Photon-Microscope/substage/tree/main/3D_designs) and print it out.  
  
1. Follow instructions on [this page](https://build.openflexure.org/openflexure-delta-stage/v1.2.2/pages/index_transmission/pages/assembling_the_actuators.html) - substituting the [main body]{qty:} for the one you just printed.
    * *Make sure motors A, B and C are positioned clockwise from above, otherwise movement will be inverted.*  
  
1. Download and print a [sample holder](https://github.com/Open-2-Photon-Microscope/substage/tree/main/3D_designs/sample_holders) that will suit your needs.

[figure_showing correct_motor_configuration]  
If your stage looks like this: congratulations! Keep going to the next steps!

###1.2 Controller Box
*This holds the electronics and dials you will use to control the stage.*

{{BOM}}
1. Download and print the files of the [3D printed case](https://github.com/Open-2-Photon-Microscope/3-axis-controller/tree/main/box%20design/stl){qty:1}.  
  
1. Use [m3 screws and nuts]{qty:some} to attach the [custom driver board](https://github.com/Open-2-Photon-Microscope/3-axis-controller/tree/main/electronics%2Fintegrated_board){qty:1} to bottom of case.
[figure_of_boards_on_case_highlight_screws]  
  
1. Attach the [ENA1J-B28-L00100L optical encoders](https://uk.farnell.com/bourns/ena1j-b28-l00100l/encoder-rotary-optical-300rpm/dp/2321812){qty:3} to the front part of the case.  
  
1. Use [JST XH cables](cable.md){qty:3} to attach the optical encoders to the board.
    * *Make sure to plug the correct encoder into its corresponding axis port on the board (XYZ).*   
[figure_of_encoder_plugged_in_correctly]  
  
1. Use a [long ribbon cable]{qty:1} to attach the motors to the board.
    * *This cable is 3-in-1 so be sure the ends you are using correspond to the correct motor ports on the board (ABC) and have been assembled correctly.*  
[figure_of_ribbon_cable_labelled]  
  
1. Assemble the rest of the case around the boards and cables.
    * *Make sure the [12V power supply]{qty:1} and [micro USB cable]{qty:1} can plug in through the holes!!!*  
  
[figure_of_assembled_box_and_stage]  
You're all done with hardware! Look at you go!
