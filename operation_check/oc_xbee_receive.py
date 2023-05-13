import sys

from cansatapi import XBee

if __name__ == "__main__":
    print("start waiting for receive messages...")
    while True:
        try:
            print(XBee.receive())
        except KeyboardInterrupt:
            sys.exit(0)
