import time, threading, os, sys
from enums import Player
class Timer(threading.Thread):

    def __init__(self, time_limit, time_record, game):
        self.time_event = threading.Event()
        self.controller_event = threading.Event()
        self.controller_event.set()
        self.thread = threading.Thread(target=self._run_timer,
                                       args=[self.time_event,
                                             self.controller_event,
                                             time_limit,
                                             game,
                                             time_record], daemon=True)

    def start_timer(self):
        self.thread.start()
        self.controller_event = threading.Thread(daemon=True)
        self.controller_event.start()
        self.time_event.set()
        # c1 = threading.Thread(daemon=True)
        # c1.start()
        # time_event1.set()

        # c2 = threading.Thread(daemon=True)
        # c2.start()
        # time_event2.clear()  # pause the timer for player 2 when player 1 playing

    def restart_timer(self):
        self.time_event.set()

    def pause_timer(self):
        self.time_event.clear()

    def _run_timer(self, time_event, controller_event, max_time, game, time_record_obj):

        global time_message
        countDown = max_time

        while controller_event.is_set():
            # countdown every second
            time_event.wait()  # control pause or resume
            if time_record_obj['reset']:
                countDown = max_time
                time_record_obj['reset'] = False
            if game.turn == Player.BLACK:
                time_record_obj["cur_spend_p1"] += 1
                time_record_obj["time_spend_p1"] += 1
            else:
                time_record_obj["time_spend_p2"] += 1
                time_record_obj["cur_spend_p2"] += 1
            time_record_obj["agg_time_spend"] += 1

            sys.stdout.write(
                f"\r[Time left for {str(game.turn).split('.')[1]}: {int(countDown / 60)}:{countDown % 60:02d}]")
            time_message = f"{int(countDown / 60)}:{countDown % 60:02d}"  # for logging of time

            if countDown > 0:
                # print(f"{game.turn} is flushing")
                sys.stdout.flush()
                countDown -= 1
            else:
                # time-up and just on hold, resume in next round
                print(f"time for {str(game.turn).split('.')[1]} is up. Game is pause. "
                      f"Possible penalty. You can still make one move.")
                countDown = max_time
                time_event.clear()

            time.sleep(1)




