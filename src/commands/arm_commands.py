# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
import typing

from commands2 import CommandBase

from subsystems.arm import Arm


class Raise(CommandBase):
    """
    Command to trigger the Arm subsystem to raise

    There must be a way to limit how far the arm will raise (digital limit switch)
    """

    def __init__(self,
                 arm: Arm,
                 joy_button: typing.Callable[[], bool]
                 ) -> None:
        """
        Set up the raise command with the arm subsystem and joystick button it needs
        """
        super().__init__()
        self._arm = arm
        self._joyInput = joy_button
        self.addRequirements(arm)

    def initialize(self) -> None:
        """
        Initialization of the Arm raise command subsystem

        Should initialize the measurement of the Arms position to "0" or the starting position
        """
        pass

    def execute(self) -> None:
        """
        The steps to execute everytime this command is called
        """
        self._arm.move(1.0)


class Move(CommandBase):
    """
    Command to trigger the Arm subsystem to raise

    There must be a way to limit how far the arm will and lower
    """

    def __init__(self,
                 arm: Arm,
                 joy_stick: typing.Callable[[], float]
                 ) -> None:
        """
        Set up the move command with the joystick "stick" axis and Arm subsystem
        """
        super().__init__()
        self._arm = arm
        # python lambda returning reading of a joystick axis
        self._joyInput = joy_stick
        self.addRequirements(arm)

    def initialize(self) -> None:
        """
        Initialization of the Arm raise command subsystem

        Should initialize the measurement of the Arms position to "0" or the starting position
        """
        pass

    def execute(self) -> None:
        """
        The steps to execute everytime this command is called
        """
        self._arm.move(self._joyInput())


class Lower(CommandBase):
    """
    Command to trigger the Arm subsystem to lower

    There must be a way to limit how far the arm will lower
    """

    def __init__(self,
                 arm: Arm,
                 joy_button: typing.Callable[[], bool]
                 ) -> None:
        """
        Set up the lower command with the Arm subsystem and joystick button that triggers it
        """
        super().__init__()
        self._arm = arm
        self._joyInput = joy_button
        self.addRequirements(arm)

    def initialize(self) -> None:
        """
        Initialization of the Arm raise command subsystem

        Should initialize the measurement of the Arms position to "0" or the starting position
        """
        pass

    def execute(self) -> None:
        """
        The steps to execute everytime this command is called
        """
        self._arm.move(-1.0)
