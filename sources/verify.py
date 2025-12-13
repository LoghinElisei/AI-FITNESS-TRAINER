import threading

import winsound


def exercises_is_correct(queue:list)->bool:
    #for correct exercises, we must have [S1,S2,S1]
    if len(queue) == 3:
        return True
    else:
        return False



def play_beep_async(error = False):
    if not error:
        threading.Thread(target=lambda: winsound.Beep(700, 500), daemon=True).start()
    else:
        threading.Thread(target=lambda: winsound.Beep(2000, 800), daemon=True).start()


