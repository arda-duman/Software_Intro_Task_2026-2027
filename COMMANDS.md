# 1. Go to your project folder (only needed if the terminal isn't already there)
cd ~/Documents/Software_Intro_Task_2026-2027

# 2. Build the package (only needed after you change files)
colcon build

# 3. Tell this terminal about your package (needed once per new terminal)
source install/setup.bash

# 4. Launch the rover in RViz
ros2 launch urdf_tutorial display.launch.py model:=$PWD/src/intro_rover_description/urdf/intro_rover_description.urdf