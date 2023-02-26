from commands2 import Command, Subsystem, CommandBase
from wpilib import IterativeRobotBase

from oi import UserController, JoystickAxis
from subsystems.shooter import Shooter


class Shoot(CommandBase):

    def __init__(
            self,
            shooter: Shooter,
            speed: float,
    ):
        super().__init__()
        self._shooter = shooter
        self._speed = speed
        self.addRequirements(shooter)

    def initialize(self) -> None:
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self) -> None:
        """
        Called repeatedly when this Command is scheduled to run
        """
        self._robot.shooter.move(self._speed)

    def isFinished(self) -> bool:
        """Returns true when the Command no longer needs to be run"""
        if self.isTimedOut():
            return True

        return False


class ShooterDrive(CommandBase):

    def __init__(
            self,
            shooter: Shooter,
            modifier_scaling: float = 1.0,
            dpad_scaling: float = 0.4
    ):
        super().__init__()
        self._shooter = shooter
        self._dpad_scaling = dpad_scaling
        self._stick_scaling = modifier_scaling
        self.addRequirements(shooter)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        shooter: float = self._robot.oi.get_axis(
            UserController.SCORING, JoystickAxis.RIGHTY
        )
        self._robot.shooter.move(shooter * self._stick_scaling)

        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return True


class LowerShooter(CommandBase):
    _robot: IterativeRobotBase = None

    def __init__(
            self, robot: IterativeRobotBase, name: str = "LowerShooter", timeout: int = 15
    ):
        super().__init__()
        self.setName(name)
        self._robot = robot
        self.withTimeout(timeout)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.shooter.upheave(False)
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

    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.shooter}


class DoNothingShooter(CommandBase):

    def __init__(
            self,
            shooter: Shooter
    ):
        super().__init__()
        self._shooter = shooter
        self.addRequirements(shooter)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.shooter.move(0.0)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False


class RaiseShooter(CommandBase):

    def __init__(
            self,
            shooter: Shooter
    ):
        super().__init__()
        self._shooter = shooter
        self.addRequirements(shooter)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.shooter.upheave(True)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False
