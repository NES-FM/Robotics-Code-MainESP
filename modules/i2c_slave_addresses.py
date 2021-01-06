addr_cam_green = 0x00  # len =          / 0x53   tl:f|tr:f|dl:f|dr:f
addr_cam_green_len = 19

addr_cam_line  = addr_cam_green + addr_cam_green_len  # len =          / 0x56   +00 /XX \XX |XX L00 R00 T00 L|0 R|0
addr_cam_line_len = 5

addr_cam_angle_start_point = addr_cam_line + addr_cam_line_len
addr_cam_angle_start_point_len = 2

addr_cam_angle_end_point = addr_cam_angle_start_point + addr_cam_angle_start_point_len
addr_cam_angle_end_point_len = 2

addr_bufferend = 0xF7  # len =          / 0xFF

addr_addr = 0x40
