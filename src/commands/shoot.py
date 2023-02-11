from commands2 import Command
from wpilib import IterativeRobotBase


class Shoot(Command):
    _speed: float = None

    def __init__(
        self,
        robot: IterativeRobotBase,
        speed: float,
        name: str = "Shoot",
        timeout: int = 15,
    ):
        super().__init__()
        self.setName(name)
        self.withTimeout(timeout)
        self.robot = robot
        self._speed = speed
        self.requires(robot.shooter)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """
        Called repeatedly when this Command is scheduled to run
        """
        self.robot.shooter.move(self._speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        if self.isTimedOut():
            return True
               
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.shooter.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
    
    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self.robot.shooter}
