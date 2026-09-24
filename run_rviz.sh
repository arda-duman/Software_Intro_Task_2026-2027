#!/bin/bash
cd ~/Documents/Software_Intro_Task_2026-2027
colcon build
source install/setup.bash
ros2 launch urdf_tutorial display.launch.py model:=$PWD/src/intro_rover_description/urdf/intro_rover_description.urdf