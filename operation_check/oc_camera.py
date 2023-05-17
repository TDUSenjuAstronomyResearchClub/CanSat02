from datetime import datetime
from cansatapi import camera

if __name__ == "__main__":
    print("Start at:" + datetime.now().time().isoformat())
    camera.photograph()
    print("Done at:" + datetime.now().time().isoformat())
