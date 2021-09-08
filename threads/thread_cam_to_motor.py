#  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/thread

import _thread
from threads.thread_messages import thread_messages as thr_msg
from modules import i2c_slave_addresses as i2csl
from modules.functions import *
import utime
from modules.cuart import CUART
from modules.display import display


thctm_calibrate_a = 0.00060519
thctm_calibrate_b = -0.016327
thctm_calibrate_c = -0.027072
thctm_calibrate_d = 25


def th_cam_to_motor(threads: dict, thctm_values: dict, m, config: dict, disp: display):
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
            elif ntf == thr_msg.HEARTBEAT:
                _thread.sendmsg(threads["th_heartbeat"], thr_msg.HEARTBEAT_RESPONSE)
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
        line_type, line_angle, line_midfactor = thctm_values["line"]


        if line_type == CUART.ltype_straight:
            x = line_angle
            drive_speed = config["drive_speed"]
            extra = 0.5 * drive_speed
            midextra = line_midfactor * 0.25 * drive_speed
            # l_value = constrain(maprange([-90, 0], [0, config["drive_speed"]], line_angle), 0, config["drive_speed"])
            # r_value = constrain(maprange([0, 90], [config["drive_speed"], 0], line_angle), 0, config["drive_speed"])
            # l_value = int(thctm_calibrate_a * x**3 - thctm_calibrate_b * x**2 + thctm_calibrate_c * x + thctm_calibrate_d)
            # r_value = int(-1 * thctm_calibrate_a * x**3 - thctm_calibrate_b * x**2 - thctm_calibrate_c * x + thctm_calibrate_d)
            if x > 2:
                if x > 15:
                    l_value = drive_speed + extra
                    r_value = -drive_speed - extra
                else:
                    l_value = drive_speed
                    r_value = 0
                # if x < 10:
                #     l_value = drive_speed
                #     r_value = 0
                # elif x < 20:
                #     l_value = drive_speed + extra
                #     r_value = 0
                # elif x < 30:
                #     l_value = drive_speed + extra
                #     r_value = -1 * drive_speed
                # else:
                #     l_value = drive_speed + extra
                #     r_value = -1 * drive_speed - extra

            elif x < -2:
                if x < -15:
                    l_value = -drive_speed - extra
                    r_value = drive_speed + extra
                else:
                    l_value = 0
                    r_value = drive_speed
                # if x > -10:
                #     l_value = 0
                #     r_value = drive_speed
                # elif x > -20:
                #     l_value = 0
                #     r_value = drive_speed + extra
                # elif x > -30:
                #     l_value = -1 * drive_speed
                #     r_value = drive_speed + extra
                # else:
                #     l_value = -1 * drive_speed - extra
                #     r_value = drive_speed + extra
            else:
                l_value = r_value = drive_speed

            l_value += midextra
            r_value -= midextra

            if config["debug"]["thctm_lrvalues"]:
                print(l_value, r_value)

        m.move(l_value, r_value)

        disp.set_values_thctm(l_value, r_value, line_angle, line_midfactor, line_type)

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
