import threading
import time


mylock = threading.RLock()
num = 0
"""

class WorkThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.t_name = name

    def run(self):
        global num
        while True:
            mylock.acquire()
            print(f"{self.t_name} locked, number: {num}")
            if num >= 3:
                mylock.release()
                print(f"{self.t_name} released, number: {num}")
                break
            num += 1
            print(f"{self.t_name} released, number: {num}")
            mylock.release()


def test():
    thread1 = WorkThread("A-Worker")
    thread2 = WorkThread("B-Worker")
    thread1.start()
    thread2.start()

"""


def print1(a):
    mylock.acquire()
    for i in range(3):
        print("one: "+ str(a))
        time.sleep(1)
    mylock.release()


def print2(a):
    mylock.acquire()
    for i in range(3):
        print("two: "+ str(a))
        time.sleep(1)
    mylock.release()


def test1():
    thread1 = threading.Thread(target=print1, args=(1,))
    thread2 = threading.Thread(target=print2, args=(2,))
    thread1.start()
    thread2.start()


if __name__ == "__main__":
    test1()
