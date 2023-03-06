# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
from configparser import ConfigParser
from typing import Optional

from commands2 import SubsystemBase
from wpilib import PWMVictorSPX, SmartDashboard, AnalogPotentiometer, DigitalInput


class Arm(SubsystemBase):
    # Config file section name
    GENERAL_SECTION = "ArmGeneral"
    POTENTIOMETER_SECTION = "ArmPotentiometer"
    LOWER_LIMIT_SWITCH_SECTION = "ArmBottomLimitSwitch"
    UPPER_LIMIT_SWITCH_SECTION = "ArmTopLimitSwitch"

    # Config keys
    CHANNEL_KEY = "CHANNEL"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    MAX_SPEED_KEY = "MAX_SPEED"
    MAX_STABLE_SPEED_KEY = "MAX_STABLE_SPEED"
    MODIFIER_SCALING_KEY = "MODIFIER_SCALING"
    POT_RANGE_KEY = "FULL_RANGE"

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
        super().__init__()

    def _init_components(self) -> None:
        self._max_stable_speed = self._config.getfloat(Arm.GENERAL_SECTION, Arm.MAX_STABLE_SPEED_KEY)
        # We have to be able to limit the max speed as some percentage of the max stable speed
        self._max_speed = self._config.getfloat(Arm.GENERAL_SECTION, Arm.MAX_SPEED_KEY)

        # initialize potentiometer for reading rotations on arm motor
        self._arm_pot_range = self._config.getfloat(Arm.POTENTIOMETER_SECTION, Arm.POT_RANGE_KEY)
        arm_pot_channel = self._config.getint(Arm.POTENTIOMETER_SECTION, Arm.CHANNEL_KEY)
        self._arm_pot = AnalogPotentiometer(arm_pot_channel, self._arm_pot_range)

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

        if self._config.getboolean(Arm.LOWER_LIMIT_SWITCH_SECTION, Arm.ENABLED_KEY):
            self._lower_limit_switch = self._init_limit_switch(Arm.LOWER_LIMIT_SWITCH_SECTION)
            self._lower_limit_switch_inverted = self._config.getboolean(
                Arm.LOWER_LIMIT_SWITCH_SECTION, Arm.INVERTED_KEY
            )

        if self._config.getboolean(Arm.UPPER_LIMIT_SWITCH_SECTION, Arm.ENABLED_KEY):
            self._upper_limit_switch = self._init_limit_switch(Arm.UPPER_LIMIT_SWITCH_SECTION)
            self._upper_limit_switch_inverted = self._config.getboolean(
                Arm.UPPER_LIMIT_SWITCH_SECTION, Arm.INVERTED_KEY
            )

        Arm._update_smartdashboard(0.0, self._arm_pot.get())

    def _init_limit_switch(self, config_section: str) -> DigitalInput:
        """
        Initialize a limit switch based on a subsystems configuration section
        """
        channel = self._config.getint(config_section, Arm.CHANNEL_KEY)
        limit_switch = DigitalInput(channel)
        return limit_switch

    def move(self, speed: float) -> None:
        """
        Set the speed of the motor based on the speed passed into the move method
        """
        if not self._enabled:
            pass

        if speed < 0 and not self.is_fully_retracted():
            adjusted_speed = speed * self._max_speed
        elif speed > 0 and not self.is_fully_extended():
            adjusted_speed = speed * self._max_speed
        else:
            adjusted_speed = 0.0

        if self._motor:
            self._motor.set(adjusted_speed)
        Arm._update_smartdashboard(adjusted_speed, self._arm_pot.get())

    # def move_angular(self, angle: float, speed: float) -> None:
    #     if not self._enabled:
    #         pass
    #     speed = speed % 1.0
    #     adjusted_speed = speed * self._max_speed
    #     if self._motor:
    #         self._motor.set(adjusted_speed)

    def is_fully_retracted(self) -> bool:
        """
        Has the Arm lowered to the point that it has engaged the lower limit switch
        """
        return self._lower_limit_switch_inverted ^ self._limit_value(self._lower_limit_switch)

    def is_fully_extended(self) -> bool:
        """
        Has the Arm raised to the point that it has engage the upper limit switch
        """
        return self._lower_limit_switch_inverted ^ self._limit_value(self._upper_limit_switch)

    @staticmethod
    def _limit_value(switch: DigitalInput) -> bool:
        if switch is not None:
            return switch.get()
        else:
            return False

    @staticmethod
    def _update_smartdashboard(speed: float, pot_reading: float) -> None:
        SmartDashboard.putNumber("0_Arm-Potentiometer", pot_reading)
        SmartDashboard.putNumber("0_Arm-Speed", speed)
