from commands2 import Command
from wpilib import IterativeRobotBase
from commands2 import Subsystem


class DoNothing(Command):
    def __init__(
        self, robot: IterativeRobotBase, name: str = "DoNothing", timeout: int = 15
    ):
        """Constructor"""
        super().__init__()
        self.setName(name)
        self.withTimeout(timeout)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        pass

    def getRequirements(self) -> set[Subsystem]:
        return {}
