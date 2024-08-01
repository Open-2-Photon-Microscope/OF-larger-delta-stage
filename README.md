
# Substage Sample Manipulator

---
### A substitute for a micromanipulator

Our design is a modification of [Open Flexure's Delta Stage model](https://openflexure.org/projects/deltastage/) combined with a 3-axis controller box. 
The delta stage is a reliable and useful way of manipulating a small sample in X, Y and Z axes without having to move the optics of the microscope, as most current setups do.

Our aim is to use it to replace expensive hardware like [Sutter's MP-285](https://www.sutter.com/MICROMANIPULATION/mp285_frame.html), which costs a lot and effectively has to hold and manipulate the entire microscope in midair.
The setup we detail is applicable to small, low-weight samples. 
    _For larger animals such as mice, we encourage further exploration and experimentation in other projects elsewhere (but we would love know what you find before we delve in to it ourselves!!)._

This part of the project consists of two main pieces:
1. The delta stage itself, to hold and move the sample
1. [The 3-axis controller](https://github.com/Open-2-Photon-Microscope/3-axis-controller/tree/main), which uses rotary encoders to manually adjust the stage position, without the need to interface with a computer (although entirely possible).

We have made modifications to OpenFlexure's original design to allow compatability with a thorlabs cage-based substage light-collection path you can find elsewhere in the Open-2-Photon-Microscope GitHub.
Since we adjusted the scale and a few other things in the design, and since the release paper does not provide data, we have been testing the delta stage's movement, measuring how reliably it makes the same movements in a given direction, and how robust it is to drift over time. These data can be found in the 'Movement Metrics Data' folder.

