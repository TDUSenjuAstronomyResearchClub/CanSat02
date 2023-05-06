import json
from cansatapi import camera

if __name__ == "__main__":

    #カメラのデータを取得
    img_data = camera.photograph()

    #16進数の文字列に変換
    camera_data = img_data.hex()

    #jsonデータを生成し、格納  
    json_data = json.dumps({"camera": camera_data}) 

    #jsonデータを出力 
    print(json_data)