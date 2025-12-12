import threading

import winsound


def exercises_is_correct(queue:list)->bool:
    #for correct exercises, we must have [S1,S2,S1]
    if len(queue) == 3:
        return True
    else:
        return False



def play_beep_async():
    threading.Thread(target=lambda: winsound.Beep(700, 500), daemon=True).start()



