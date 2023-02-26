# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
from commands2 import Command
from commands2 import Subsystem

from oi import JoystickAxis, UserController, JoystickButtons, OI
from subsystems.drivetrain import Drivetrain


class TankDrive(Command):

    def __init__(
            self,
            oi: OI,
            drivetrain: Drivetrain,
            modifier_scaling: float = 0.5,
            dpad_scaling: float = 0.4,
    ):
        """
        Constructor

        Sets the scaling factor (`_dpad_scaling`) for "fine" control over the tank drive from the directional pad
        Sets the scaling factor (`_stick_scaling`) for general control of the tank drive from the joysticks

        Set up for "Slew Rate Limiting" based on button modifier input. If the "Slew Rate" button is compressed,
        then the robot tank drive will not use the direct input from the joystick. Instead, it will apply a
        maximum rate of change to the joystick input.

        Caveat: The way the slew rate is applied, it will also affect deceleration of the robot. That means that
        if the slew rate modifier button is depressed, that the robot will not immediately come to a stop when
        the joystick is released, it will slowly decelerate (fast deceleration is one of the primary reasons for
        robot tipping)
        """
        super().__init__()
        self._oi = oi
        self._drivetrain = drivetrain
        self._dpad_scaling = dpad_scaling
        self._stick_scaling = modifier_scaling

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        modifier: bool = self.oi.get_button_state(
            UserController.DRIVER, JoystickButtons.LEFTBUMPER
        )
        dpad_y: float = self.oi.get_axis(
            UserController.DRIVER, JoystickAxis.DPADY
        )
        if dpad_y != 0.0:
            self.drivetrain.arcade_drive(self._dpad_scaling * dpad_y, 0.0)
        else:
            left_track: float = self.oi.get_axis(
                UserController.DRIVER, JoystickAxis.LEFTY
            )
            right_track: float = self.oi.get_axis(
                UserController.DRIVER, JoystickAxis.RIGHTY
            )
            if modifier:
                self.drivetrain.tank_drive(
                    self._stick_scaling * left_track, self._stick_scaling * right_track
                )
            else:
                self.drivetrain.tank_drive(left_track, right_track)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self, **kwargs):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        pass

    def getRequirements(self) -> set[Subsystem]:
        return {self.drivetrain}

    @property
    def drivetrain(self) -> Drivetrain:
        return self._drivetrain

    @property
    def dpad_scaling(self) -> float:
        return self._dpad_scaling

    @property
    def stick_scaling(self):
        return self._stick_scaling

    @property
    def oi(self) -> OI:
        return self._oi