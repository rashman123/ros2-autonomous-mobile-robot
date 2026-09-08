import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

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

        self.get_logger().info('Count Action Server is ready.')

    def execute_callback(self, goal_handle):

        target = goal_handle.request.target

        self.get_logger().info(
            f'Received goal: count until {target}'
        )

        feedback_msg = CountUntil.Feedback()

        for i in range(1, target + 1):

            feedback_msg.current_count = i

            goal_handle.publish_feedback(feedback_msg)

            self.get_logger().info(
                f'Feedback: {i}'
            )

            time.sleep(1)

        goal_handle.succeed()

        result = CountUntil.Result()
        result.final_count = target

        self.get_logger().info(
            f'Finished counting: {target}'
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
