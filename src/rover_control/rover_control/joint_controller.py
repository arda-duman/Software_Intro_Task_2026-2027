import os
import threading
import xml.etree.ElementTree as ET

import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import JointState

JOINT_NAMES = [
    'shoulder_yaw', 'shoulder_pitch', 'elbow_pitch', 'elbow_roll',
    'wrist_pitch', 'wrist_roll',
    'fr_swerve_yaw', 'fr_wheel', 'br_swerve_yaw', 'br_wheel',
    'fl_swerve_yaw', 'fl_wheel', 'bl_swerve_yaw', 'bl_wheel',
]


def load_limits():
    pkg_share = get_package_share_directory('intro_rover_description')
    urdf_path = os.path.join(pkg_share, 'urdf', 'intro_rover_description.urdf')
    root = ET.parse(urdf_path).getroot()

    limits = {}
    for joint in root.findall('joint'):
        limit = joint.find('limit')
        if joint.get('type') == 'revolute' and limit is not None:
            limits[joint.get('name')] = (float(limit.get('lower')), float(limit.get('upper')))
    return limits


class JointController(Node):
    def __init__(self):
        super().__init__('joint_controller')
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.positions = {name: 0.0 for name in JOINT_NAMES}
        self.limits = load_limits()
        self.timer = self.create_timer(0.1, self.publish_joints)
        threading.Thread(target=self.read_input, daemon=True).start()

    def publish_joints(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = JOINT_NAMES
        msg.position = [self.positions[name] for name in JOINT_NAMES]
        self.publisher.publish(msg)

    def read_input(self):
        print('Joints:', ', '.join(JOINT_NAMES))
        print("Type 'quit' to exit.")
        while True:
            text = input('> ')

            if text.strip() in ('quit', 'exit', 'q'):
                print('Shutting down joint controller.')
                rclpy.try_shutdown()
                return

            parts = text.split()

            if len(parts) != 2:
                print('Type a joint name and an angle, e.g. shoulder_yaw 1.0')
                continue

            name, value = parts

            if name not in JOINT_NAMES:
                print(f'Unknown joint: {name}')
                continue

            try:
                angle = float(value)
            except ValueError:
                print(f'Not a number: {value}')
                continue

            if name in self.limits:
                lower, upper = self.limits[name]
                if not lower <= angle <= upper:
                    print(f'{name} must be between {lower} and {upper}')
                    continue

            self.positions[name] = angle
            print(f'{name} set to {angle}')


def main():
    rclpy.init()
    node = JointController()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()