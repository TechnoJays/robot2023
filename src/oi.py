import configparser
from enum import Enum

from commands2 import CommandGroupBase
from commands2.button import JoystickButton
from wpilib import DriverStation
from wpilib import Joystick
from wpilib import SendableChooser


class JoystickAxis:
    """Enumerates joystick axis."""

    LEFTX = 0
    LEFTY = 1
    RIGHTX = 4
    RIGHTY = 5
    DPADX = 11
    DPADY = 12


class JoystickButtons:
    """Enumerates joystick buttons."""

    X = 1
    A = 2
    B = 3
    Y = 4
    LEFTBUMPER = 5
    RIGHTBUMPER = 6
    LEFTTRIGGER = 7
    RIGHTTRIGGER = 8
    BACK = 9
    START = 10


class UserController(Enum):
    """Enumerates the controllers."""

    DRIVER = 0
    SCORING = 1


class OI:
    """
    This class is the glue that binds the controls on the physical operator
    interface to the commands and command groups that allow control of the robot.
    """

    AXIS_BINDING_SECTION = "AxisBindings"
    BUTTON_BINDING_SECTION = "ButtonBindings"
    JOY_CONFIG_SECTION = "JoyConfig"
    DEAD_ZONE_KEY = "DEAD_ZONE"
    PORT_KEY = "PORT"
    LEFT_X_KEY = "LEFTX"
    LEFT_Y_KEY = "LEFTY"
    RIGHT_X_KEY = "RIGHTX"
    RIGHT_Y_KEY = "RIGHTY"
    DPAD_X_KEY = "DPADX"
    DPAD_Y_KEY = "DPADY"
    X_KEY = "X"
    A_KEY = "A"
    B_KEY = "B"
    Y_KEY = "Y"
    LEFT_BUMPER_KEY = "LEFTBUMPER"
    RIGHT_BUMPER_KEY = "RIGHTBUMPER"
    LEFT_TRIGGER_KEY = "LEFTTRIGGER"
    RIGHT_TRIGGER_KEY = "RIGHTTRIGGER"
    BACK_KEY = "BACK"
    START_KEY = "START"

    def __init__(
            self,
            config: configparser.ConfigParser,
    ):
        self._config = config

        self._controllers: list[Joystick] = []
        self._dead_zones: list[float] = []
        for i in range(2):
            self._controllers.append(self._init_joystick(i))
            self._dead_zones.append(self._init_dead_zone(i))

        self._init_joystick_binding()
        self._init_button_binding()
        self._auto_program_chooser: SendableChooser = SendableChooser()
        self._starting_chooser: SendableChooser = SendableChooser()

    def _init_joystick(self, driver: int) -> Joystick:
        config_section = OI.JOY_CONFIG_SECTION + str(driver)
        return Joystick(self._config.getint(config_section, OI.PORT_KEY))

    def _init_dead_zone(self, driver: int) -> float:
        config_section = OI.JOY_CONFIG_SECTION + str(driver)
        return self._config.getfloat(config_section, OI.DEAD_ZONE_KEY)

    def _init_joystick_binding(self):
        JoystickAxis.LEFTX = self._config.getint(OI.AXIS_BINDING_SECTION, OI.LEFT_X_KEY)
        JoystickAxis.LEFTY = self._config.getint(OI.AXIS_BINDING_SECTION, OI.LEFT_Y_KEY)
        JoystickAxis.RIGHTX = self._config.getint(OI.AXIS_BINDING_SECTION, OI.RIGHT_X_KEY)
        JoystickAxis.RIGHTY = self._config.getint(OI.AXIS_BINDING_SECTION, OI.RIGHT_Y_KEY)

        JoystickAxis.DPADX = self._config.getint(OI.AXIS_BINDING_SECTION, OI.DPAD_X_KEY)
        JoystickAxis.DPADY = self._config.getint(OI.AXIS_BINDING_SECTION, OI.DPAD_Y_KEY)

        JoystickButtons.X = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.X_KEY)
        JoystickButtons.A = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.A_KEY)
        JoystickButtons.B = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.B_KEY)
        JoystickButtons.Y = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.Y_KEY)

        JoystickButtons.LEFTBUMPER = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.LEFT_BUMPER_KEY)
        JoystickButtons.RIGHTBUMPER = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.RIGHT_BUMPER_KEY)
        JoystickButtons.LEFTTRIGGER = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.LEFT_TRIGGER_KEY)
        JoystickButtons.RIGHTTRIGGER = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.RIGHT_TRIGGER_KEY)

        JoystickButtons.BACK = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.BACK_KEY)
        JoystickButtons.START = self._config.getint(OI.BUTTON_BINDING_SECTION, OI.START_KEY)

    def _init_button_binding(self) -> None:
        self._grab_button = JoystickButton(
            self._controllers[UserController.SCORING.value], JoystickButtons.RIGHTBUMPER
        )
        self._release_button = JoystickButton(
            self._controllers[UserController.SCORING.value], JoystickButtons.LEFTBUMPER
        )

    def get_auto_choice(self) -> CommandGroupBase:
        """
        Return the autonomous mode choice selected on the smart dashboard

        TODO Challenges with _robot reference being `None` in `RobotController`
        """
        return self.auto_chooser().getSelected()

    def get_position(self) -> int:
        """
        Return the drive teams selected starting position for the robot on the field

        TODO unimplemented in smart dashboard
        """
        return self._starting_chooser.getSelected()

    @staticmethod
    def get_game_message() -> str:
        return DriverStation.getGameSpecificMessage()

    def get_axis(self, user: UserController, axis: int) -> float:
        """Read axis value for specified controller/axis.

        Args:
            user: Controller ID to read from
            axis: Axis ID to read from.

        Return:
            Current position for the specified axis. (Range [-1.0, 1.0])
        """
        controller = self._controllers[user.value]
        value: float
        if axis == JoystickAxis.DPADX:
            value = controller.getPOV()
            if value == 90:
                value = 1.0
            elif value == 270:
                value = -1.0
            else:
                value = 0.0
        elif axis == JoystickAxis.DPADY:
            value = controller.getPOV()
            if value == 0:
                value = -1.0
            elif value == 180:
                value = 1.0
            else:
                value = 0.0
        else:
            value = controller.getRawAxis(axis)
            if abs(value) < self._dead_zones[user.value]:
                value = 0.0
        return value

    def get_button_state(self, user: UserController, button: int) -> bool:
        return self._controllers[user.value].getRawButton(button)

    def config(self) -> configparser.ConfigParser:
        return self._config

    def controllers(self) -> list[UserController]:
        return self._controllers

    def auto_chooser(self) -> SendableChooser:
        return self._auto_program_chooser

    def grab_button(self) -> JoystickButton:
        return self._grab_button

    def release_button(self) -> JoystickButton:
        return self._release_button
