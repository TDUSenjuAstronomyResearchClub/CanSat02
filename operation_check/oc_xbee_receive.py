import asyncio

from cansatapi import XBee

if __name__ == "__main__":
    print("start waiting for receive messages...")
    print(asyncio.run(XBee.receive()))
