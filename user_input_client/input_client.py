import sys

from custom_interfaces.srv import UserInput
import rclpy
from rclpy.node import Node

class UserInputClient(Node):
    def __init__(self):
        super().__init__('user_input_client')

        self.cli = self.create_client(UserInput, 'user_input_srv')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = UserInput.Request()

    def send_request(self, task):
        self.get_logger().info(f"sending task: '{task}'")
        self.req.user_input = task
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)

        return self.future.result() 



def main():
    rclpy.init()

    user_input_client = UserInputClient()

    task = sys.argv[1]
    user_input_client.get_logger().info(f"task given bu user: {task}")
    

    response = user_input_client.send_request(task=task)
    user_input_client.get_logger().info(f"success {response}")

    user_input_client.destroy_node()
    rclpy.shutdown()

        


if __name__ == "__main__":
    main()
