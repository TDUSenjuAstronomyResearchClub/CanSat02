import sys
import time

from cansatapi import XBee
if __name__ == "__main__":
    while True:
        try:
            XBee.send("test")
            print("Send message")
            time.sleep(1000)
        except KeyboardInterrupt:
            sys.exit(0)
