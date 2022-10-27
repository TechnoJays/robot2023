from configparser import ConfigParser

from commands1 import CommandGroup
from commands1 import WaitCommand
from wpilib import IterativeRobotBase

from commands.drive_time import DriveTime
from commands.raise_shooter import RaiseShooter
from commands.shoot import Shoot
from commands.vacuum import Vacuum


def use_drive_gyro(robot) -> bool:
    return robot.drivetrain.is_gyro_enabled()


class MoveFromLine(CommandGroup):
    _SECTION = "MoveFromLine"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"

    _robot = None

    _drive_speed: float = None
    _drive_time: float = None

    def __init__(
        self,
        robot: IterativeRobotBase,
        config_path: str = "/home/lvuser/py/configs/autonomous.ini",
    ):
        """Constructor"""
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config)
        self._initialize_commands()

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)

    def _initialize_commands(self):
        command = DriveTime(self._robot, self._drive_time, self._drive_speed)
        self.addSequential(command)


class DriveToWall(CommandGroup):
    _SECTION = "DriveToWall"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"

    _robot = None

    _drive_speed: float = None
    _drive_time: float = None

    def __init__(
        self, robot, config_path: str = "/home/lvuser/py/configs/autonomous.ini"
    ):
        """Constructor"""
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config)
        self._initialize_commands()

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)

    def _initialize_commands(self):
        command = DriveTime(self._robot, self._drive_time, self._drive_speed)
        self.addSequential(command)


class DeadReckoningScore(CommandGroup):
    _SECTION = "DeadReckoningScore"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"
    _WAIT_TIME = "WAIT_TIME"

    _robot = None

    _drive_speed: float = None
    _drive_time: float = None
    _wait_time: float = None

    def __init__(
        self, robot, config_path: str = "/home/lvuser/py/configs/autonomous.ini"
    ):
        """Constructor"""
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config)
        self._initialize_commands()

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)
        self._wait_time = parser.getfloat(self._SECTION, self._WAIT_TIME)

    def _initialize_commands(self):
        command = DriveTime(self._robot, self._drive_time, self._drive_speed)
        self.addSequential(command)
        command = WaitCommand(self._wait_time)
        self.addSequential(command)
        command = RaiseShooter(self._robot)
        self.addSequential(command)


class ShootScore(CommandGroup):
    _SECTION = "ShootScore"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"
    _WAIT_TIME = "WAIT_TIME"
    _SHOOT_TIME_KEY = "SHOOT_TIME"
    _VACUUM_TIME_KEY = "VACUUM_TIME"

    _robot = None

    _drive_speed: float = None
    _drive_time: float = None
    _wait_time: float = None
    _shoot_time: float = None
    _vacuum_time: float = None

    def __init__(
        self, 
        robot, 
        config_path: str = "/home/lvuser/py/configs/autonomous.ini"
    ):
        """Constructor"""
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config)
        self._initialize_commands()

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)
        self._wait_time = parser.getfloat(self._SECTION, self._WAIT_TIME)
        self._shoot_time = parser.getfloat(self._SECTION, self._SHOOT_TIME_KEY)
        self._vacuum_time = parser.getfloat(self._SECTION, self._VACUUM_TIME_KEY)

    def _initialize_commands(self):
        command = DriveTime(self._robot, self._drive_time, self._drive_speed)
        self.addSequential(command)
        command = WaitCommand(self._wait_time)
        self.addSequential(command)
        command = Shoot(self._robot, 1.0, "AutoShoot", self._shoot_time)
        self.addSequential(command)
        command = WaitCommand(self._wait_time)
        self.addSequential(command)
        command = Vacuum(self._robot, -1.0, "AutoVacuum", self._vacuum_time)
        self.addSequential(command)
