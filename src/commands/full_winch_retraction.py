from commands2 import Command
from wpilib import IterativeRobotBase


class FullWinchRetraction(Command):
    def __init__(
        self,
        robot: IterativeRobotBase,
        name: str = None,
        speed: float = 0.0,
        timeout: int = 15,
    ):
        """Constructor"""
        super().__init__()
        self.setName(name)
        self.withTimeout(timeout)
        self.robot = robot
        self._climb_speed: float = speed
        self.requires(robot.climbing)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.climbing.move_winch(self._climb_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self.robot.climbing.is_retracted()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.climbing.move_winch(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    def getRequirements(self) -> Set[Subsystem]:
        return {self.robot.climbing}
