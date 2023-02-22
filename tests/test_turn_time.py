from configparser import ConfigParser

import pytest
from wpilib import IterativeRobotBase
from wpilib.simulation import PWMSim

from commands.turn_time import TurnTime
from subsystems.drivetrain import Drivetrain
from util.stopwatch import Stopwatch


@pytest.fixture(scope="function")
def config_default() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_default.ini")
    return config


@pytest.fixture(scope="function")
def drivetrain_default(config_default: ConfigParser):
    return Drivetrain(config_default)


@pytest.fixture(scope="function")
def command_default(robot: IterativeRobotBase, drivetrain_default: Drivetrain):
    robot.drivetrain = drivetrain_default
    return TurnTime(drivetrain_default, 5, 1.0)


def test_init_default(command_default: TurnTime):
    assert command_default is not None
    assert command_default.drivetrain is not None
    assert command_default.stopwatch is not None
    assert command_default.duration == 5
    assert command_default.speed == 1.0


def test_init_full(drivetrain_default: Drivetrain):
    dt = TurnTime(drivetrain_default, 10, 0.5)
    assert dt is not None
    assert dt.drivetrain is not None
    assert dt.stopwatch is not None
    assert dt.duration == 10
    assert dt.speed == 0.5


def test_initialize(command_default: TurnTime):
    command_default.initialize()
    assert command_default.stopwatch._running


@pytest.mark.parametrize(
    "speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0),
        (0.5, -0.5306122448979592, -0.5306122448979592),
        (1.0, -1.0, -1.0),
        (-0.5, 0.5306122448979592, 0.5306122448979592),
        (-1.0, 1.0, 1.0),
    ],
)
def test_execute(
        drivetrain_default: Drivetrain,
        speed: float,
        left_ex_speed: float,
        right_ex_speed: float,
):
    dt = TurnTime(drivetrain_default, 5, speed)
    assert dt is not None

    left_m = PWMSim(drivetrain_default._left_motor.getChannel())
    right_m = PWMSim(drivetrain_default._right_motor.getChannel())

    dt.initialize()
    dt.execute()
    pytest.approx(left_ex_speed, left_m.getSpeed())
    pytest.approx(right_ex_speed, right_m.getSpeed())


def test_is_finished(command_default):
    command_default.initialize()
    assert command_default.isFinished() is False


def test_interrupted(command_default):
    pass  # interrupted method is empty


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


@pytest.mark.parametrize(
    "duration,timeout, speed,left_ex_speed,right_ex_speed",
    [
        (0.5, 5.0, 0.5, -0.5306122448979592, -0.5306122448979592),
        (0.5, 5.0, -0.5, 0.5306122448979592, 0.5306122448979592),
        (2.0, 15.0, 1.0, -1.0, -1.0),
        # (5.0, 1.0, 1.0, 1.0, -1.0), # Timeouts don't seem to work in testing
    ],
)
def test_command_full(
        drivetrain_default: Drivetrain,
        duration: float,
        timeout: float,
        speed: float,
        left_ex_speed: float,
        right_ex_speed: float,
):
    dt = TurnTime(drivetrain_default, duration, speed)
    sw = Stopwatch()
    assert dt is not None

    left_m = PWMSim(drivetrain_default._left_motor.getChannel())
    right_m = PWMSim(drivetrain_default._right_motor.getChannel())

    dt.initialize()
    sw.start()
    while not dt.isFinished():
        dt.execute()
        pytest.approx(left_ex_speed, left_m.getSpeed())
        pytest.approx(right_ex_speed, right_m.getSpeed())
    dt.end()
    sw.stop()
    if duration < timeout:
        assert isclose(sw.elapsed_time_in_secs(), duration)
    else:
        # TODO: Timeouts don't seem to work in testing?
        assert isclose(sw.elapsed_time_in_secs(), timeout)
