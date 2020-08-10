import time
from timeloop import Timeloop
from datetime import timedelta
import mysocket
import os

tl = Timeloop()

# os.environ['TZ'] = 'US/Pacific'
# time.tzset()


@tl.job(interval=timedelta(seconds=600))
def ping_colab_every_10mins():
    print("ping_colab current time : {}".format(time.ctime()))
    mysocket.main.pingColabServer()


# if __name__ == "__main__":
#     tl.start(block=True)
