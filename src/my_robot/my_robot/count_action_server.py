import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from geometry_msgs.msg import Twist
from my_robot_interfaces.action import CountUntil


class CountActionServer(Node):

    def __init__(self):
        super().__init__('count_action_server')

        self._action_server = ActionServer(
            self,
            CountUntil,
            'count_until',
            self.execute_callback
        )

        self._cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info(
            'Count Action Server is ready.'
        )

    def execute_callback(self, goal_handle):

        target = goal_handle.request.target

        self.get_logger().info(
            f'Executing goal: {target}'
        )

        feedback_msg = CountUntil.Feedback()

        # Robot speed
        twist = Twist()
        twist.linear.x = 0.2
        twist.angular.z = 0.0

        # Count and move
        for count in range(1, target + 1):

            # Move robot
            self._cmd_vel_pub.publish(twist)

            # Feedback
            feedback_msg.current_count = count
            goal_handle.publish_feedback(feedback_msg)

            self.get_logger().info(
                f'Current count: {count}'
            )

            # Wait 1 second
            rclpy.spin_once(self, timeout_sec=1.0)

        # Stop robot
        stop_twist = Twist()
        stop_twist.linear.x = 0.0
        stop_twist.angular.z = 0.0

        self._cmd_vel_pub.publish(stop_twist)

        # Result
        goal_handle.succeed()

        result = CountUntil.Result()
        result.final_count = target

        self.get_logger().info(
            f'Final count: {target}'
        )

        return result


def main(args=None):

    rclpy.init(args=args)

    node = CountActionServer()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
