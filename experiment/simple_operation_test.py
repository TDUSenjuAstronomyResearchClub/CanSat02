"""機体が正常に前進などをする構造になっているかのテストモジュール
"""

from running import geared_motor

# 3秒間前進
geared_motor.StraightLine()

# 3秒間後退
geared_motor.Back()

# 左旋回
geared_motor.TurnLeft()

# 右旋回
geared_motor.TurnRight()
