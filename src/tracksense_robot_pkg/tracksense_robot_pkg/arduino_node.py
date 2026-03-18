import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

class ArduinoNode(Node):
    def __init__(self):
        super().__init__('arduino_node')

        self.subscription = self.create_subscription(String, "robot/motor_commands", self.command_callback, 10)

        self.serial_port = SERIAL_PORT
        self.baud_rate = BAUD_RATE

        self.robot_running = False

        self.read_timer = self.create_timer(0.1, self.read_from_arduino)

        try:
            self.arduino = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            time.sleep(2)
            self.get_logger().info(f"Connected to arduino on port {self.serial_port}")
        except Exception as e:
            self.get_logger().error("Failed to connect to arduino")
            self.arduino = None

    def command_callback(self, msg):
        command_str = msg.data
        if command_str == "START":
            self.robot_running = False  # reset until we get confirmation
        if command_str == "STOP":
            self.robot_running = False

        # Always send START and STOP
        # Only send angles if robot confirmed running
        if command_str.startswith("FRONT_ANGLE") and not self.robot_running:
            self.get_logger().warn("Skipping angle command, robot not confirmed running")
            return

        if self.arduino:
            try:
                self.arduino.write(f"{command_str}\n".encode('utf-8'))
                self.arduino.flush()
            except Exception as e:
                self.get_logger().error(f"Failed to write to serial: {e}")
        else:
            self.get_logger().error("Arduino not set up")

    def read_from_arduino(self):

        if self.arduino and self.arduino.in_waiting > 0:
            try:
                arduino_reply = self.arduino.readline().decode('utf-8').strip()
                if arduino_reply:
                    self.get_logger().info(f"ARDUINO SAYS: {arduino_reply}")
                    if "Robot starting via App" in arduino_reply:
                        self.robot_running = True
                    if "Robot stopping via App" in arduino_reply:
                        self.robot_running = False
            except Exception as e:
                self.get_logger().error(f"Failed to read from Arduino: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.arduino:
            node.arduino.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
