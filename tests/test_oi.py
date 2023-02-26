from configparser import ConfigParser

import pytest
from commands2._impl.button import JoystickButton

from commands.autonomous_commands import MoveFromLine
from oi import JoystickAxis, JoystickButtons, OI


@pytest.fixture(scope="function")
def config_default() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/joysticks_default.ini")
    return config


@pytest.fixture(scope="function")
def config_joy_ports_01() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/joysticks_ports_0_1.ini")
    return config


@pytest.fixture(scope="function")
def config_auto() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/autonomous_default.ini")
    return config


@pytest.fixture(scope="function")
def oi_default(config_default: ConfigParser) -> OI:
    return OI(config_default)


@pytest.fixture(scope="function")
def oi_joy_ports(config_joy_ports_01: ConfigParser) -> OI:
    return OI(config_joy_ports_01)


def test__init_joystick(oi_joy_ports: OI, config_joy_ports_01: ConfigParser):
    assert oi_joy_ports is not None
    assert oi_joy_ports.config() == config_joy_ports_01
    assert len(oi_joy_ports.controllers()) == 2
    assert oi_joy_ports.controllers()[0] is not None
    assert oi_joy_ports.controllers()[1] is not None


def test__init_dead_zone(oi_joy_ports: OI, config_joy_ports_01: ConfigParser):
    assert oi_joy_ports is not None
    assert oi_joy_ports.config() == config_joy_ports_01
    assert len(oi_joy_ports.controllers()) == 2
    assert oi_joy_ports.controllers()[0] is not None
    assert oi_joy_ports.controllers()[1] is not None


def test__init_joystick_binding(oi_default: OI, config_default: ConfigParser):
    assert oi_default is not None
    assert oi_default.config() == config_default

    assert JoystickAxis.LEFTX == config_default.getint(OI.AXIS_BINDING_SECTION, OI.LEFT_X_KEY)
    assert JoystickAxis.LEFTY == config_default.getint(OI.AXIS_BINDING_SECTION, OI.LEFT_Y_KEY)
    assert JoystickAxis.RIGHTX == config_default.getint(OI.AXIS_BINDING_SECTION, OI.RIGHT_X_KEY)
    assert JoystickAxis.RIGHTY == config_default.getint(OI.AXIS_BINDING_SECTION, OI.RIGHT_Y_KEY)

    assert JoystickAxis.DPADX == config_default.getint(OI.AXIS_BINDING_SECTION, OI.DPAD_X_KEY)
    assert JoystickAxis.DPADY == config_default.getint(OI.AXIS_BINDING_SECTION, OI.DPAD_Y_KEY)

    assert JoystickButtons.X == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.X_KEY)
    assert JoystickButtons.A == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.A_KEY)
    assert JoystickButtons.B == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.B_KEY)
    assert JoystickButtons.Y == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.Y_KEY)

    assert JoystickButtons.LEFTBUMPER == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.LEFT_BUMPER_KEY)
    assert JoystickButtons.RIGHTBUMPER == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.RIGHT_BUMPER_KEY)
    assert JoystickButtons.LEFTTRIGGER == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.LEFT_TRIGGER_KEY)
    assert JoystickButtons.RIGHTTRIGGER == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.RIGHT_TRIGGER_KEY)

    assert JoystickButtons.BACK == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.BACK_KEY)
    assert JoystickButtons.START == config_default.getint(OI.BUTTON_BINDING_SECTION, OI.START_KEY)


@pytest.mark.skip(reason="don't know why robot is None for this test")
def test__setup_autonomous_smartdashboard(oi_default: OI, config_auto: ConfigParser):
    assert oi_default is not None
    auto_chooser = oi_default._setup_autonomous_smartdashboard(config_auto)
    assert auto_chooser is not None
    assert type(auto_chooser.getSelected()) is MoveFromLine


def test__init_button_bindings(oi_default):
    assert oi_default is not None
    assert oi_default.grab_button() is not None
    assert type(oi_default.grab_button()) is JoystickButton
    assert oi_default.release_button() is not None
    assert type(oi_default.release_button()) is JoystickButton


@pytest.mark.skip(reason="requires setup_autonomous_dashboard")
def test_get_auto_choice():
    assert False


@pytest.mark.skip(reason="unimplemented for lack of time")
def test_get_position():
    assert False


@pytest.mark.skip(reason="no important game message (panel color) for 2023 game")
def test_get_game_message():
    assert False


@pytest.mark.skip(reason="reserved for later sophisticated pyfrc/robotpy testing")
def test_get_axis():
    assert False


@pytest.mark.skip(reason="reserved for later sophisticated pyfrc/robotpy testing")
def test_get_button_state():
    assert False
