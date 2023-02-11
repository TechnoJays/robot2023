from commands2 import Command
from wpilib import IterativeRobotBase


class DoNothingShooter(Command):
    def __init__(
        self,
        robot: IterativeRobotBase,
        name: str = "DoNothingShooter",
        timeout: int = 15,
    ):
        super().__init__()
        self.robot = robot
        self.setName(name)
        self.withTimeout(timeout)
        self.requires(robot.shooter)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.shooter.move(0.0)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    def getRequirements(self) -> Set[Subsystem]:
        return { self.robot.shooter }