from commands2 import Command
import math

from wpilib import IterativeRobotBase
from commands2 import Subsystem

class TurnDegrees(Command):
    _robot: IterativeRobotBase = None

    _speed: float = None
    _degree_threshold: float = None
    _degrees_change: float = None
    _target_degrees: float = None

    def __init__(
        self,
        robot: IterativeRobotBase,
        degrees_change: float,
        speed: float,
        threshold: float,
        name: str = "TurnDegrees",
        timeout: int = 15,
    ):
        """Constructor"""
        super().__init__()
        self.setName(name)
        self._robot = robot
        self.withTimeout(timeout)
        self._degrees_change = degrees_change
        self._speed = speed
        self._degree_threshold = threshold

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._target_degrees = (
            self._robot.drivetrain.get_gyro_angle() + self._degrees_change
        )
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        degrees_left = self._target_degrees - self._robot.drivetrain.get_gyro_angle()
        turn_speed = self._speed * TurnDegrees._determine_direction(degrees_left)
        self._robot.drivetrain.arcade_drive(0.0, turn_speed, False)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        current = self._robot.drivetrain.get_gyro_angle()
        # If abs(target - current) < threshold then return true
        return (
            math.fabs(self._target_degrees - current) <= self._degree_threshold
            or self.isTimedOut()
        )

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    @staticmethod
    def _determine_direction(degrees_left: float) -> float:
        """Based on the degrees left, determines the direction of the degrees to turn"""
        return 1.0 if degrees_left >= 0 else -1.0
    
    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.drivetrain}
