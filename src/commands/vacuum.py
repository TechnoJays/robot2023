from commands2 import Command
from wpilib import IterativeRobotBase
from commands2 import Subsystem

class Vacuum(Command):
    _speed: float = None
    _robot: IterativeRobotBase = None

    def __init__(
        self,
        robot: IterativeRobotBase,
        speed: float,
        name: str = "Vacuum",
        timeout: int = 15,
    ):
        super().__init__()
        self.setName(name)
        self._robot = robot
        self._speed = speed
        self.withTimeout(timeout)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.vacuum.move(self._speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        if self.isTimedOut():
            return True
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.vacuum.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
    
    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.vacuum}
