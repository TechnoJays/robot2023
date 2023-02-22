import math

from commands2 import Command
from commands2 import Subsystem

from subsystems.drivetrain import Drivetrain


class TurnDegreesAbsolute(Command):

    def __init__(
            self,
            drivetrain: Drivetrain,
            degrees_target: float,
            speed: float,
            threshold: float,
    ):
        """Constructor"""
        super().__init__()
        self._drivetrain = drivetrain
        self._target_degrees = degrees_target
        self._speed = speed
        self._degree_threshold = threshold

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        degrees_left = self._target_degrees - self._drivetrain.get_gyro_angle()
        turn_speed = self._speed * TurnDegreesAbsolute._determine_direction(
            degrees_left
        )
        self._drivetrain.arcade_drive(0.0, turn_speed, False)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        current = self._drivetrain.get_gyro_angle()
        # If abs(target - current) < threshold then return true
        return (
                math.fabs(self._target_degrees - current) <= self._degree_threshold
        )

    def end(self, **kwargs):
        """Called once after isFinished returns true"""
        self._drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    @staticmethod
    def _determine_direction(degrees_left: float) -> float:
        """Based on the degrees left, returns -1 for turn right, returns 1 for turn left"""
        return 1.0 if degrees_left >= 0 else -1.0

    def getRequirements(self) -> set[Subsystem]:
        return {self._drivetrain}

    @property
    def drivetrain(self) -> Drivetrain:
        return self._drivetrain

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def target_degrees(self) -> float:
        return self._target_degrees

    @property
    def degree_threshold(self) -> float:
        return self._degree_threshold
