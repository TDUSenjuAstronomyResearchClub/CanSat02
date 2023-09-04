"""機体が正常に前進などをする構造になっているかのテストモジュール
"""
from running.geared_motor import *

# 3秒間前進
StraightLine()

# 3秒間後退
Back()

# 左旋回
TurnLeft()

# 右旋回
TurnRight()
