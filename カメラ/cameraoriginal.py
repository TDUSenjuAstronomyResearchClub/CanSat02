from time import strftime
import cv2
import datetime

cap = cv2.VideoCapture(0)   #カメラチャンネルの指定

now =datetime.datetime.now()    #現在の日付と時間を取得しnowに代入
d = now.strftime('%Y-%m-%d_%H-%M-%S')   
picture = d + '.jpg'   #拡張子の設定

ret, frame = cap.read() #１コマ分のカメラ画像を読み込む
#resize the window
#print(today)
windowsize = (1000, 800)
frame = cv2.resize(frame, windowsize)

cv2.imwrite(picture, frame) #カメラ画像を出力
cap.release()
cv2.destroyAllWindows()
