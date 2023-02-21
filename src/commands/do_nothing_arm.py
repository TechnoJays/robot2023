from commands2 import Command
from commands2 import Subsystem

from subsystems.arm import Arm


class DoNothingArm(Command):
    _arm: Arm = None

    def __init__(
            self,
            arm: Arm,
            timeout: int = 15,
    ):
        super().__init__()
        self._arm = arm
        self.withTimeout(timeout)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.arm().move(0.0)
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

    def arm(self) -> Arm:
        return self._arm

    def getRequirements(self) -> set[Subsystem]:
        return {self.arm()}
