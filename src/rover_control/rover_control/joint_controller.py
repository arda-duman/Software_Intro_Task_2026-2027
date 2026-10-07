import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

JOINT_NAMES = [
    'shoulder_yaw', 'shoulder_pitch', 'elbow_pitch', 'elbow_roll',
    'wrist_pitch', 'wrist_roll',
    'fr_swerve_yaw', 'fr_wheel', 'br_swerve_yaw', 'br_wheel',
    'fl_swerve_yaw', 'fl_wheel', 'bl_swerve_yaw', 'bl_wheel',
]


class JointController(Node):
    def __init__(self):
        super().__init__('joint_controller')
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.positions = {name: 0.0 for name in JOINT_NAMES}
        self.positions['fl_swerve_yaw'] = 1.5
        self.timer = self.create_timer(0.1, self.publish_joints)

    def publish_joints(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = JOINT_NAMES
        msg.position = [self.positions[name] for name in JOINT_NAMES]
        self.publisher.publish(msg)


def main():
    rclpy.init()
    node = JointController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()