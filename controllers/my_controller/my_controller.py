"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

import subprocess

subprocess.run(['python3', '-m', 'streamlit', 'run', 'app.py'])

