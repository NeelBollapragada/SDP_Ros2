import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/SDP_Ros2/src/tracksense_robot_pkg/install/tracksense_robot_pkg'
