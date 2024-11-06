"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

target_shoulder_position = 0.6
target_elbow_position = -2.1
target_wrist_position = 1
target_shoulder_roll = 27
target_left_finger = 0.7
target_right_finger = 0.7


shoulder_pitch_motor = robot.getDevice("joint_2")
shoulder_pitch_sensor = robot.getDevice("joint_2_sensor")
shoulder_pitch_sensor.enable(timestep)
shoulder_pitch_motor.setPosition(target_shoulder_position)
shoulder_pitch_motor.setVelocity(0.5)

elbow_pitch_motor = robot.getDevice("joint_3")
elbow_pitch_sensor = robot.getDevice("joint_3_sensor")
elbow_pitch_sensor.enable(timestep)
elbow_pitch_motor.setPosition(target_elbow_position)
elbow_pitch_motor.setVelocity(0.5)

wrist_pitch_motor = robot.getDevice("joint_5")
wrist_pitch_sensor = robot.getDevice("joint_5_sensor")
wrist_pitch_sensor.enable(timestep)
wrist_pitch_motor.setPosition(target_wrist_position)
wrist_pitch_motor.setVelocity(0.5)


shoulder_roll_motor = robot.getDevice("joint_1")
shoulder_roll_sensor = robot.getDevice("joint_1_sensor")
shoulder_roll_sensor.enable(timestep)
shoulder_roll_motor.setVelocity(0.5)

left_finger_motor = robot.getDevice("ROBOTIQ 2F-140 Gripper::left finger joint")
right_finger_motor = robot.getDevice("ROBOTIQ 2F-140 Gripper::right finger joint")
left_finger_sensor = robot.getDevice("ROBOTIQ 2F-140 Gripper left finger joint sensor")
right_finger_sensor = robot.getDevice("ROBOTIQ 2F-140 Gripper right finger joint sensor")
left_finger_sensor.enable(timestep)
right_finger_sensor.enable(timestep)

while robot.step(timestep) != -1:

    # gripper grips when in place
    if abs(shoulder_pitch_sensor.getValue() - target_shoulder_position) < 0.01:
        if abs(elbow_pitch_sensor.getValue() - target_elbow_position) < 0.01:
            if abs(wrist_pitch_sensor.getValue() - target_wrist_position) < 0.01:
                # print(shoulder_roll_sensor.getValue())
                
                left_finger_motor.setPosition(target_left_finger)
                left_finger_motor.setVelocity(0.3)
                right_finger_motor.setPosition(target_right_finger)
                right_finger_motor.setVelocity(0.3)
                
    # start line drawing once its gripped
    if abs(left_finger_sensor.getValue() - target_left_finger) < 0.01:
        if abs(right_finger_sensor.getValue() - target_right_finger) < 0.01:
                shoulder_roll_motor.setPosition(target_shoulder_roll)
                break
                
                
   