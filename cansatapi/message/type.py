"""JSONの型を定義するモジュール

https://json2pyi.pages.dev/ を使用して生成したのち微修正しました。
"""
# Generated with https://json2pyi.pages.dev/
# and some fix by me.

from __future__ import annotations
from typing import TypedDict


class SensorJson(TypedDict):
    time: str | None
    gps: Gps | None
    nine_axis: NineAxis | None
    bme280: Bme280 | None
    lps25hb: Lps25Hb | None
    battery: float | None
    distance: float | None
    camera: str | None
    soil_moisture: float | None
    message: str | None


class Gps(TypedDict):
    latitude: float
    longitude: float
    altitude: float
    distance: Distance
    azimuth: Azimuth


class Distance(TypedDict):
    sample: float
    goal: float


class Azimuth(TypedDict):
    sample: float
    goal: float


class NineAxis(TypedDict):
    acceleration: Acceleration
    angular_velocity: AngularVelocity
    azimuth: float


class Acceleration(TypedDict):
    x: float
    y: float
    z: float


class AngularVelocity(TypedDict):
    x: float
    y: float
    z: float


class Bme280(TypedDict):
    temperature: float
    humidity: float
    pressure: float


class Lps25Hb(TypedDict):
    temperature: float
    pressure: float
    altitude: float
