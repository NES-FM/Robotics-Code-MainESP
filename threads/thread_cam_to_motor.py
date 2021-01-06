#  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/thread

import _thread
from threads import thread_messages as thr_msg
from modules import i2c_slave_addresses as i2csl
from modules.functions import *


def th_cam_to_motor(threads: dict, i2c_slave, m, config: dict):
    _thread.allowsuspend(True)

    cur_name = _thread.getSelfName()
    cur_id = threads[cur_name]

    print("{}: started with id {}".format(cur_name.upper(), cur_id))

    while True:
        ntf = _thread.getnotification()
        if ntf:
            if ntf == _thread.EXIT:
                print("{}: terminated".format(cur_name.upper()))
                return
            elif ntf == _thread.SUSPEND:
                print("{}: suspended".format(cur_name.upper()))
                m.stop()
                # wait for RESUME notification indefinitely, some other thread must
                # send the resume notification: _thread.notify(th_id, _thread.RESUME)
                while _thread.wait() != _thread.RESUME:
                    pass
                print("{}: resumed".format(cur_name.upper()))
            else:
                # Default notification handling
                pass

        # ---------------------------------------------------------------
        # - Using sleep in thread function                              -
        # ---------------------------------------------------------------
        # 'utime.sleep(sec, True)' & 'utime.sleep_ms(ms, True)' functions returns the
        # actual ellapsed sleep time. The sleep will be interrupted if
        # a notification is received and the returned value will be less
        # than the requested one
        # ---------------------------------------------------------------
        # Example:
        # print("TH_FUNC: Loop started")
        # for i in range(0, 5):
        #     print("TH_FUNC: Loop no:", i)
        #     sleep_time = utime.sleep_ms(10000, True)
        #     if sleep_time < 10000:
        #         # Notification received while sleeping
        #         print("TH_FUNC: Notification while sleeping", st)
        #         # Sleep for the remaining interval if needed
        #         utime.sleep_ms(10000 - sleep_time)
        # print("TH_FUNC: Loop ended")

        # ===================================================================================
        # Handle inter thread message
        # Sender thread ID, message type (string or integer) and message itself are available
        # ===================================================================================
        ""

        # <MAIN CODE>

        line_data = i2c_slave.getdata(i2csl.addr_cam_line, i2csl.addr_cam_line_len).decode("UTF-8")  # ||+00
        line_type = line_data[0:2]
        try:
            line_angle = int(line_data[2:5])
        except ValueError as e:
            print("{}: line_angle value error:".format(cur_name.upper()), e)
            line_angle = 0

        l_value = r_value = config["drive_speed"]

        if line_type == "||":
            l_value = constrain(maprange([-90, 0], [0, config["drive_speed"]], line_angle), 0, config["drive_speed"])
            r_value = constrain(maprange([0, 90], [config["drive_speed"], 0], line_angle), 0, config["drive_speed"])

        m.move(l_value, r_value)

        # </MAIN CODE>

        typ, sender, msg = _thread.getmsg()
        if msg:
            if typ == 1 and msg == thr_msg.HEARTBEAT:
                _thread.sendmsg(sender, thr_msg.HEARTBEAT)

            # else:
            #     _thread.sendmsg(threads["log"], "[%s] Received message from '%s'\n'%s'" % (
            #         _thread.getSelfName(), _thread.getThreadName(sender), msg))
