import sys

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AdderClient(Node):

    def __init__(self):
        super().__init__('adder_client')

        self.client = self.create_client(
            AddTwoInts,
            'add_two_ints'
        )

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'Waiting for add_two_ints service...'
            )

    def send_request(self, a, b):
        request = AddTwoInts.Request()

        request.a = a
        request.b = b

        return self.client.call_async(request)


def main(args=None):
    rclpy.init(args=args)

    node = AdderClient()

    a = int(sys.argv[1])
    b = int(sys.argv[2])

    future = node.send_request(a, b)

    rclpy.spin_until_future_complete(node, future)

    response = future.result()

    node.get_logger().info(
        f'Result: {a} + {b} = {response.sum}'
    )

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
