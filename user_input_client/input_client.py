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

    test_prompts_raw = open("/home/user1/ros2_ws/src/user_input_client/user_input_client/LLM_test_prompts.txt").read()
    test_prompts_sep_by_cat = test_prompts_raw.split("###")
    full_sep_prompt_arr = []

    for test_cat in test_prompts_sep_by_cat:
        full_sep_prompt_arr.append(test_cat.split("\n"))
    
    for test_cat in full_sep_prompt_arr:
        for task in test_cat:
            response = user_input_client.send_request(task=task)
            user_input_client.get_logger().info(f"recived: success:{response.success}, msg:{response.msg}")

    user_input_client.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
