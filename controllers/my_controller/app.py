import streamlit as st
from controller import Robot

# Custom CSS to make the slider color pink
st.markdown(
    """
    <style>
    .stSlider > div > div > div > div {
        background: pink !important; /* Change the slider filled bar color */
    }
    .stSlider > div > div > div > div:nth-child(3) {
        background: #ffc0cb !important; /* Change the slider empty bar color */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define a placeholder for painting initiation logic
def start_painting(thickness):
    st.session_state["output"] += f"Painting initiated with thickness: {thickness}\n"
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

    st.session_state["output"] += "\nRobot initialized for painting.\n"

def update_z_value(z_value):
    st.session_state["output"] += f"Updating Z value to: {z_value}\n"
    # robot = Robot()
    # timestep = int(robot.getBasicTimeStep())
    
    # # Target Z position logic
    # target_z_position = z_value
    
    # # Set Z motor position
    # z_motor = robot.getDevice("joint_z")
    # z_motor_sensor = robot.getDevice("joint_z_sensor")
    # z_motor_sensor.enable(timestep)
    # z_motor.setPosition(target_z_position)
    # z_motor.setVelocity(0.5)
    
    # while robot.step(timestep) != -1:
    #     # Check if Z motor has reached the target position
    #     if abs(z_motor_sensor.getValue() - target_z_position) < 0.01:
    #         st.session_state["output"] += "\nZ position updated successfully."
    #         break

# Initialize session state for output text
if "output" not in st.session_state:
    st.session_state["output"] = "Welcome to MAVA!\n"

# Set the title of the app
st.title("MAVA")

# Define a single slider at the top level
slider_value = st.slider("Input desired value (mm or Z)", min_value=1, max_value=26, value=6)
# st.write(f"Selected value: {slider_value}")

# Add buttons for actions
if st.button("Input Z value"):
    start_painting(slider_value)

if st.button("Update Z Value"):
    update_z_value(slider_value)

# Display persistent output text
st.text_area("Output Log", st.session_state["output"], height=200)
