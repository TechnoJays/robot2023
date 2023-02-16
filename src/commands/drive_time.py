from commands2 import Command
from wpilib import IterativeRobotBase
from util.stopwatch import Stopwatch
from commands2 import Subsystem


class DriveTime(Command):
    _stopwatch: Stopwatch = None
    _duration: float = None
    _speed: float = None
    _robot: IterativeRobotBase = None

    def __init__(
        self,
        robot: IterativeRobotBase,
        duration: float,
        speed: float,
        name: str = "DriveTime",
        timeout: int = 15,
    ):
        """Constructor"""
        super().__init__()
        self.setName(name)
        self._robot = robot
        self.withTimeout(timeout)
        self._stopwatch = Stopwatch()
        self._duration = duration
        self._speed = speed

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._stopwatch.start()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.drivetrain.arcade_drive(self._speed, 0.0, False)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._stopwatch.elapsed_time_in_secs() >= self._duration

    def end(self):
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        self._robot.drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
    
    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.drivetrain}
