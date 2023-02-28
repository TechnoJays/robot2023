# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
import configparser
from configparser import ConfigParser

from commands2.button import JoystickButton
import wpilib
from commands2 import SubsystemBase, CommandBase, TimedCommandRobot
from wpilib import SmartDashboard, SendableChooser

from commands.arm_commands import ArmMove
from commands.autonomous_drive_commands import MoveFromLine
from commands.grabber_commands import Grab, Release
from commands.tank_drive_commands import TankDrive
from oi import OI, JoystickAxis, UserController, JoystickButtons
from subsystems.arm import Arm
from subsystems.drivetrain import Drivetrain
from subsystems.grabber import Grabber


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

    def __init__(self, robot: TimedCommandRobot) -> None:
        self._robot: TimedCommandRobot = robot
        self._init_config()
        self._subsystems = self._init_subsystems()

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

    def _init_subsystems(self) -> list[SubsystemBase]:
        """
        Initialize subsystems managed by the robot controller
        """
        subsystems = []

        self._oi = OI(self._joystick_config)
        subsystems.append(self._oi)

        self._drivetrain = Drivetrain(self._subsystems_config)
        subsystems.append(self._drivetrain)

        self._arm = Arm(self._subsystems_config)
        subsystems.append(self._arm)

        self._grabber = Grabber(self._subsystems_config)
        subsystems.append(self._grabber)

        wpilib.CameraServer.launch()

        return subsystems

    def mappings(self) -> None:
        """
        A method to connect subsystems, the operator interface, and autonomous once
        all the subsystems have been initialized

        This method is called separately from the constructor to prevent circular dependencies
        across Subsystem and Command constructor initialization
        """

        # set up the default drive command to be tank drive
        self.drivetrain.setDefaultCommand(TankDrive(self.oi, self.drivetrain))

        # set up the default arm command
        self.arm.setDefaultCommand(
            ArmMove(
                self.arm,
                lambda: self.oi.get_axis(UserController.SCORING, JoystickAxis.LEFTY),
            )
        )

        # set up the default grabber command to be "Grab"
        self.grabber.setDefaultCommand(Grab(self.grabber))

        # set up the right bumper of the scoring controller to trigger the grabber to release
        self.oi.release_button().whileHeld(Release(self.grabber))

    def get_auto_choice(self) -> CommandBase:
        return self._oi.get_auto_choice()

    def _setup_autonomous_smartdashboard(self,
                                         drivetrain: Drivetrain,
                                         autonomous_config: configparser.ConfigParser) -> SendableChooser:
        self._auto_program_chooser = SendableChooser()
        self._auto_program_chooser.setDefaultOption(
            "Move From Line", MoveFromLine(drivetrain, autonomous_config)
        )
        SmartDashboard.putData("Autonomous", self._auto_program_chooser)
        return self._auto_program_chooser

    @property
    def drivetrain(self) -> Drivetrain:
        """
        Retrieve the drivetrain managed by the robot controller
        """
        return self._drivetrain

    @property
    def arm(self) -> Arm:
        """
        Retrieve the "Arm" managed by the robot controller
        """
        return self._arm

    @property
    def oi(self) -> OI:
        """
        Retrieve the operator interface managed by the robot controller
        """
        return self._oi

    @property
    def grabber(self) -> Grabber:
        return self._grabber

    @property
    def subsystems_config(self) -> ConfigParser:
        return self._subsystems_config

    @property
    def joystick_config(self) -> ConfigParser:
        return self._joystick_config

    @property
    def autonomous_config(self) -> ConfigParser:
        return self._autonomous_config

    @property
    def subsystems(self):
        return self._subsystems
