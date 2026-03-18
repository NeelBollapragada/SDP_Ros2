import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/SDP_Ros2/install/tracksense_robot_pkg'
