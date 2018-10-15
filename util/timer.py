import threading


def fun_timer():
    print('Hello Timer!')
    global timer
    timer = threading.Timer(5.5, fun_timer)
    timer.start()

timer = threading.Timer(1, fun_timer)
timer.start()