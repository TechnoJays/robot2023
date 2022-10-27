import configparser

from wpilib import IterativeRobotBase, PWMMotorController, PWMVictorSPX
from wpilib import SmartDashboard
from commands1 import Subsystem
from commands.do_nothing_vacuum import DoNothingVacuum
from commands.vacuum_drive import VacuumDrive


class Vacuum(Subsystem):
    # Config file section names
    GENERAL_SECTION = "VacuumGeneral"

    # Config keys
    CHANNEL_KEY = "CHANNEL"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    MAX_SPEED_KEY = "MAX_SPEED"

    _robot: IterativeRobotBase = None

    _config = None
    _motor: PWMMotorController = None
    _max_speed: float = 0.0

    def __init__(
        self,
        robot: IterativeRobotBase,
        name: str = "Vacuum",
        configfile: str = "/home/lvuser/py/configs/subsystems.ini",
    ):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        Vacuum._update_smartdashboard(0.0)
        super().__init__(name)

    def _init_components(self):
        self._max_speed = self._config.getfloat(
            Vacuum.GENERAL_SECTION, Vacuum.MAX_SPEED_KEY
        )
        if self._config.getboolean(Vacuum.GENERAL_SECTION, Vacuum.ENABLED_KEY):
            self._motor = PWMVictorSPX(
                self._config.getint(Vacuum.GENERAL_SECTION, Vacuum.CHANNEL_KEY)
            )
            self._motor.setInverted(
                self._config.getboolean(Vacuum.GENERAL_SECTION, Vacuum.INVERTED_KEY)
            )

    def initDefaultCommand(self):
        # self.setDefaultCommand(DoNothingVacuum(self._robot)) #previous
        self.setDefaultCommand(VacuumDrive(self._robot))

    def move(self, speed: float):
        adjusted_speed = 0.0
        if self._motor:
            adjusted_speed = speed * self._max_speed
            self._motor.set(adjusted_speed)
        Vacuum._update_smartdashboard(adjusted_speed)

    @staticmethod
    def _update_smartdashboard(speed: float = 0.0):
        SmartDashboard.putNumber("Vacuum Speed", speed)
