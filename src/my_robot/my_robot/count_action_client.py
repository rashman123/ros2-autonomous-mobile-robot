import sys

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from my_robot_interfaces.action import CountUntil


class CountActionClient(Node):

    def __init__(self):
        super().__init__('count_action_client')

        self._action_client = ActionClient(
            self,
            CountUntil,
            'count_until'
        )

    def send_goal(self, target):
        self.get_logger().info('Waiting for action server...')

        self._action_client.wait_for_server()

        goal_msg = CountUntil.Goal()
        goal_msg.target = target

        self.get_logger().info(f'Sending goal: {target}')

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(
            self.goal_response_callback
        )

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()

        self._get_result_future.add_done_callback(
            self.result_callback
        )

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        self.get_logger().info(
            f'Current count: {feedback.current_count}'
        )

    def result_callback(self, future):
        result = future.result().result

        self.get_logger().info(
            f'Final count: {result.final_count}'
        )

        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    node = CountActionClient()

    if len(sys.argv) < 2:
        node.get_logger().error(
            'Usage: ros2 run my_robot count_action_client <target>'
        )
        node.destroy_node()
        rclpy.shutdown()
        return

    target = int(sys.argv[1])

    node.send_goal(target)

    rclpy.spin(node)


if __name__ == '__main__':
    main()