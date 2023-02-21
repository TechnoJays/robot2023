# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
import configparser, traceback
from configparser import ConfigParser

import wpilib
from commands2 import SubsystemBase, CommandBase, TimedCommandRobot

from oi import OI
from subsystems.arm import Arm
from subsystems.climbing import Climbing
from subsystems.drivetrain import Drivetrain
from subsystems.shooter import Shooter
from subsystems.vacuum import Vacuum


class RobotController:
    """
    This class is where the bulk of robot logic is declared. This is aligned to the
    `robotpy`/wpilib Command-based declarative paradigm. The majority of the structure
    of the robot outside of subsystems, and operator interface (oi) mappings are
    declared here
    """
    SUBSYSTEMS_CONFIG_PATH = "/home/lvuser/py/configs/subsystems.ini"
    JOYSTICK_CONFIG_PATH = "/home/lvuser/py/configs/joysticks.ini"
    AUTONOMOUS_CONFIG_PATH = "/home/lvuser/py/configs/autonomous.ini"

    _robot: TimedCommandRobot = None

    _oi: OI = None
    _drivetrain: Drivetrain = None
    _arm: Arm = None
    _climbing: Climbing = None
    _shooter: Shooter = None
    _vacuum: Vacuum = None
    _autonomous_command: CommandBase = None

    _subsystems_config: ConfigParser = None
    _joystick_config: ConfigParser = None
    _autonomous_config: ConfigParser = None

    def __init__(self, robot: TimedCommandRobot) -> None:
        self._robot = robot
        self._init_config()
        self._init_subsystems(robot)

    def _init_config(self) -> None:
        """
        Initialize config parsers for subsystems, operator interface, and autonomous
        """
        self._subsystems_config = configparser.ConfigParser()
        self._subsystems_config.read(self.SUBSYSTEMS_CONFIG_PATH)

        self._joystick_config = configparser.ConfigParser()
        self._joystick_config.read(self.JOYSTICK_CONFIG_PATH)

        self._autonomous_config = configparser.ConfigParser()
        self._autonomous_config.read(self.AUTONOMOUS_CONFIG_PATH)

    def _init_subsystems(self, robot: TimedCommandRobot) -> list[SubsystemBase]:
        """
        Initialize subsystems managed by the robot controller
        """
        subsystems = []

        self._oi = OI(robot, self._joystick_config)
        subsystems.append(self._oi)

        self._drivetrain = Drivetrain(robot, self._subsystems_config)
        subsystems.append(self._drivetrain)

        wpilib.CameraServer.launch()

        return subsystems

    def mappings(self) -> None:
        """
        A method to connect subsystems, the operator interface, and autonomous once
        all the subsystems have been initialized
        """
        self.oi().init_button_bindings()
        self.oi().map_commands(self.drivetrain(), self.arm())

    def get_auto_choice(self) -> CommandBase:
        return self.oi().get_auto_choice()

    def drivetrain(self) -> Drivetrain:
        """
        Retrieve the drivetrain managed by the robot controller
        """
        return self._drivetrain

    def arm(self) -> Arm:
        """
        Retrieve the "Arm" managed by the robot controller
        """
        return self._arm

    def oi(self) -> OI:
        """
        Retrieve the operator interface managed by the robot controller
        """
        return self._oi

    def vacuum(self) -> Vacuum:
        print("**** invalid vacuum accessed here:")
        traceback.print_stack()
        return Vacuum()


