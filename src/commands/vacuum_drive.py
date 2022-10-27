from commands1 import Command
from wpilib import IterativeRobotBase

from oi import JoystickAxis, JoystickButtons, UserController


class VacuumDrive(Command):
    _dpad_scaling: float
    _stick_scaling: float

    def __init__(
        self,
        robot: IterativeRobotBase,
        name: str = "VacuumDrive",
        modifier_scaling: float = 1.0,
        dpad_scaling: float = 0.4,
        timeout: int = 15,
    ):
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.vacuum)
        self._dpad_scaling = dpad_scaling
        self._stick_scaling = modifier_scaling

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        vacuum: float = self.robot.oi.get_axis(
            UserController.SCORING, JoystickAxis.RIGHTY
        )
        self.robot.vacuum.move(vacuum * self._stick_scaling)

        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return True

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
