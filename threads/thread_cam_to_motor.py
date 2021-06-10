#  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/thread

import _thread
from threads import thread_messages as thr_msg
from modules import i2c_slave_addresses as i2csl
from modules.functions import *
import utime
from modules.cuart import CUART


def th_cam_to_motor(threads: dict, thctm_values: dict, m, config: dict):
    _thread.allowsuspend(True)

    cur_name = _thread.getSelfName()
    cur_id = threads[cur_name]

    print("{}: started with id {}".format(cur_name.upper(), cur_id))

    while True:
        """Notification Handling"""
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

        """Line Parsing and Motor controlling"""
        line_angle = thctm_values["line"][1]
        line_type = thctm_values["line"][0]

        l_value = r_value = config["drive_speed"]

        if line_type == CUART.ltype_straight:
            x = line_angle
            # l_value = constrain(maprange([-90, 0], [0, config["drive_speed"]], line_angle), 0, config["drive_speed"])
            # r_value = constrain(maprange([0, 90], [config["drive_speed"], 0], line_angle), 0, config["drive_speed"])
            l_value = int(0.0006911*x*x*x-0.011111*x*x+0.044657*x+20)
            r_value = int(-0.0006911*x*x*x-0.011111*x*x-0.044657*x+20)
            # print(l_value, r_value)

        m.move(l_value, r_value)

        # </MAIN CODE>

        """Message handling"""
        typ, sender, msg = _thread.getmsg()
        if msg:
            if typ == 1 and msg == thr_msg.HEARTBEAT:
                _thread.sendmsg(sender, thr_msg.HEARTBEAT)

            # else:
            #     _thread.sendmsg(threads["log"], "[%s] Received message from '%s'\n'%s'" % (
            #         _thread.getSelfName(), _thread.getThreadName(sender), msg))

        utime.sleep_ms(10)  # Weird bug (was 10 before, trying to minimize)
