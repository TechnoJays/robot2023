# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
from configparser import ConfigParser
from typing import Optional

from commands2 import SubsystemBase
from wpilib import PWMVictorSPX, SmartDashboard


class Arm(SubsystemBase):
    # Config file section name
    GENERAL_SECTION = "ArmGeneral"

    # Config keys
    CHANNEL_KEY = "CHANNEL"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    MAX_SPEED_KEY = "MAX_SPEED"
    MAX_STABLE_SPEED_KEY = "MAX_STABLE_SPEED"
    MODIFIER_SCALING_KEY = "MODIFIER_SCALING"

    def __init__(
            self,
            config: ConfigParser
    ) -> None:
        self._config = config
        self._enabled = self._config.getboolean(
            Arm.GENERAL_SECTION, Arm.ENABLED_KEY
        )
        self._init_components()
        print("Arm initialized")
        Arm._update_smartdashboard(0.0)
        super().__init__()

    def _init_components(self) -> None:
        self._max_stable_speed = self._config.getfloat(Arm.GENERAL_SECTION, Arm.MAX_STABLE_SPEED_KEY)
        # We have to be able to limit the max speed as some percentage of the max stable speed
        self._max_speed = self._config.getfloat(Arm.GENERAL_SECTION, Arm.MAX_SPEED_KEY) % self._max_stable_speed

        if self._enabled:
            print("*** Arm enabled ****")
            self._motor = PWMVictorSPX(
                self._config.getint(Arm.GENERAL_SECTION, Arm.CHANNEL_KEY)
            )
            self._motor.setInverted(
                self._config.getboolean(Arm.GENERAL_SECTION, Arm.INVERTED_KEY)
            )
            print("*** Arm PWM Configured ****")
        else:
            self._motor = None

        self._modifier_scaling: Optional[float] = None

    def move(self, speed: float) -> None:
        if not self._enabled:
            pass
        speed = speed % 1.0
        adjusted_speed = speed * self._max_speed
        if self._motor:
            self._motor.set(adjusted_speed)
        Arm._update_smartdashboard(adjusted_speed)

    def move_angular(self, angle: float, speed: float) -> None:
        if not self._enabled:
            pass
        speed = speed % 1.0
        adjusted_speed = speed * self._max_speed
        if self._motor:
            self._motor.set(adjusted_speed)

    @staticmethod
    def _update_smartdashboard(speed: float = 0.0):
        SmartDashboard.putNumber("Arm Speed", speed)
