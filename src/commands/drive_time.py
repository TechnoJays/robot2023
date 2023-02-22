from commands2 import Command
from commands2 import Subsystem

from subsystems.drivetrain import Drivetrain
from util.stopwatch import Stopwatch


class DriveTime(Command):

    def __init__(
            self,
            drivetrain: Drivetrain,
            duration: float,
            speed: float,
    ):
        """Constructor"""
        super().__init__()
        self._drivetrain = drivetrain
        self._stopwatch = Stopwatch()
        self._duration = duration
        self._speed = speed

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._stopwatch.start()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.drivetrain.arcade_drive(self._speed, 0.0, False)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._stopwatch.elapsed_time_in_secs() >= self._duration

    def end(self, **kwargs):
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        self._drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    def getRequirements(self) -> set[Subsystem]:
        return {self._drivetrain}

    @property
    def drivetrain(self) -> Drivetrain:
        return self._drivetrain

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def stopwatch(self) -> Stopwatch:
        return self._stopwatch

    @property
    def speed(self) -> float:
        return self._speed
