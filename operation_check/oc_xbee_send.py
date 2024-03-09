import sys
import time

from cansatapi import xbee

MSG = "test"

if __name__ == "__main__":
    while True:
        try:
            xbee.send(MSG)
            print(f"Send message: {MSG}")
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
