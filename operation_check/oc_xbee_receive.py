import asyncio

from cansatapi import xbee

if __name__ == "__main__":
    print("start waiting for receive messages...")
    print(asyncio.run(XBee.receive()))
