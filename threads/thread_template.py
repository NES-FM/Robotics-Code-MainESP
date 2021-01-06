#  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/thread

import _thread
from threads import thread_messages as thr_msg

## START
# threads[th_name] = _thread.start_new_thread(th_name, th_func, args [, kwargs])

## Example:
# threads = {"th_func": 1, "log": 2}

def th_func(threads: dict):
    # ------------------------------------------------------------
    # Allow suspending this thread from other threads using
    # _thread.suspend(th_id) / _thread.resume(th_id) functions.
    # If not set, the thread connot be suspended.
    # Still, "soft" suspend handling via notifications can be used
    # ------------------------------------------------------------
    _thread.allowsuspend(True)

    cur_name = _thread.getSelfName()
    cur_id = threads[cur_name]

    print("{}: started with id {}".format(cur_name.upper(), cur_id))

    # ---------------------------------------------
    # Thread function usually runs in infinite loop
    # ---------------------------------------------
    while True:
        # ================================================
        # It is recommended to handle thread notifications
        # ================================================
        ntf = _thread.getnotification()
        if ntf:
            # some notification received
            if ntf == _thread.EXIT:
                # -------------------------------------------------
                # Return from thread function terminates the thread
                # -------------------------------------------------
                print("{}: terminated".format(cur_name.upper()))
                return
            elif ntf == _thread.SUSPEND:
                # -------------------------------------------------------------------
                # The thread can be suspended using _thread.suspend(th_id) function,
                # but sometimes it is more convenient to implement the "soft" suspend
                # -------------------------------------------------------------------
                print("{}: suspended".format(cur_name.upper()))
                # wait for RESUME notification indefinitely, some other thread must
                # send the resume notification: _thread.notify(th_id, _thread.RESUME)
                while _thread.wait() != _thread.RESUME:
                    pass
                print("{}: resumed".format(cur_name.upper()))
            # ---------------------------------------------
            # Handle the application specific notifications
            # ---------------------------------------------
            elif ntf == 1234:
                # Your notification handling code
                pass
            else:
                # -----------------------------
                # Default notification handling
                # -----------------------------
                pass

        # ----------------------------------
        # Put your thread function code here
        # ----------------------------------

        # ---------------------------------------------------------------------------
        # Thread function execution can be suspended until a notification is received
        # Without argument '_thread.wait' will wait for notification indefinitely
        # If the timeout argument is given, the function will return even if
        # no notification is received after the timeout expires with result 'None'
        # ---------------------------------------------------------------------------
        # ntf = _thread.wait(30000)
        # if ntf:
        #     # --------------------------------------------
        #     # Check if terminate notification was received
        #     # --------------------------------------------
        #     if ntf == _thread.EXIT:
        #         return
        #     #print("TH_FUNC: Notification received: ", ntf)
        #
        #     # ---------------------------------------------
        #     # Execute some code based on notification value
        #     # ---------------------------------------------
        #     if ntf == 77:
        #         print("Notification 77 received")
        #     elif ntf == 8888:
        #         myvar += 100
        # else:
        #     # ---------------------------------
        #     # Execute some code on wait timeout
        #     # ---------------------------------
        #     print("TH_FUNC: Wait notification timeout")

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
        typ, sender, msg = _thread.getmsg()
        if msg:
            # -------------------------------------
            # message received from 'sender' thread
            # -------------------------------------

            if typ == 1 and msg == thr_msg.HEARTBEAT:
                # Reply to sender, we can analyze the message first
                _thread.sendmsg(sender, thr_msg.HEARTBEAT)

            else:
                # We can inform the main MicroPython thread (REPL) about received message
                _thread.sendmsg(threads["log"], "[%s] Received message from '%s'\n'%s'" % (_thread.getSelfName(), _thread.getThreadName(sender), msg))
