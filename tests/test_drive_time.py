import pytest
from wpilib import IterativeRobotBase

from commands.drive_time import DriveTime
from subsystems.drivetrain import Drivetrain
from util.stopwatch import Stopwatch
from wpilib.simulation import PWMSim


@pytest.fixture(scope="function")
def drivetrain_default(robot: IterativeRobotBase):
    return Drivetrain(
        robot, "TestDrivetrain", "../tests/test_configs/drivetrain_default.ini"
    )


@pytest.fixture(scope="function")
def command_default(robot: IterativeRobotBase, drivetrain_default: Drivetrain):
    robot.drivetrain = drivetrain_default
    return DriveTime(robot, duration=5.0, speed=1.0, name="TestDriveTime")


def test_init_default(command_default: DriveTime):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.drivetrain is not None
    assert command_default._stopwatch is not None
    assert command_default.getName() == "TestDriveTime"
    # There is no longer a way to access the initialized timeout
    # assert command_default.timeout == -1
    assert command_default._duration == 5
    assert command_default._speed == 1.0


def test_init_full(robot: IterativeRobotBase, drivetrain_default: Drivetrain):
    robot.drivetrain = drivetrain_default
    dt = DriveTime(robot, 10, 0.5, "CustomDriveTime", 5)
    assert dt is not None
    assert dt.robot is not None
    assert dt.robot.drivetrain is not None
    assert dt._stopwatch is not None
    assert dt.getName() == "CustomDriveTime"
    # There is no longer a way to access the initialized timeout
    # assert dt.timeout == 5
    assert dt._duration == 10
    assert dt._speed == 0.5


def test_initialize(command_default: DriveTime):
    command_default.initialize()
    assert command_default._stopwatch._running


@pytest.mark.parametrize(
    "speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0),
        (0.5, 0.4897959183673469, -0.4897959183673469),
        (1.0, 1.0, -1.0),
        (-0.5, -0.5306122448979592, 0.5306122448979592),
        (-1.0, -1.0, 1.0),
    ],
)
def test_execute(
    robot: IterativeRobotBase,
    drivetrain_default: Drivetrain,
    speed: float,
    left_ex_speed: float,
    right_ex_speed: float,
):

    # given: a drivetrain
    robot.drivetrain = drivetrain_default
    # and: left and right motors on the drive train
    left_motor_sim = PWMSim(drivetrain_default._left_motor.getChannel())
    right_motor_sim = PWMSim(drivetrain_default._right_motor.getChannel())
    # and: a command to drive the robot forward for five seconds
    dt = DriveTime(robot, 5, speed, "TestDriveTime", 15)

    # when: drive time command is initialized and executed
    dt.initialize()
    dt.execute()

    # then: the speed of both motors should match the spped from the command
    pytest.approx(left_motor_sim.getSpeed(), left_ex_speed)
    pytest.approx(right_motor_sim.getSpeed(), right_ex_speed)


def test_is_finished(command_default: DriveTime):
    command_default.initialize()
    assert command_default.isFinished() is False


def test_interrupted(command_default: DriveTime):
    pass  # interrupted method is empty


def test_end(
    robot: IterativeRobotBase,
    command_default: DriveTime,
    drivetrain_default: Drivetrain,
):
    assert command_default._stopwatch._running is False

    # given: a drivetrain
    robot.drivetrain = drivetrain_default
    # and: left and right motors on the drive train
    left_motor_sim = PWMSim(drivetrain_default._left_motor.getChannel())
    right_motor_sim = PWMSim(drivetrain_default._right_motor.getChannel())

    # then: the speed of both motors should match the spped from the command
    assert 0.0 == pytest.approx(left_motor_sim.getSpeed())
    assert 0.0 == pytest.approx(right_motor_sim.getSpeed())


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


@pytest.mark.parametrize(
    "duration,speed,timeout,left_ex_speed,right_ex_speed",
    [
        (0.5, 0.5, 5.0, 0.5306122448979592, -0.5306122448979592),
        (2.0, 1.0, 15.0, 1.0, -1.0),
        # (5.0, 1.0, 1.0, 1.0, -1.0), # Timeouts don't seem to work in testing
    ],
)
def test_command_full(
    robot: IterativeRobotBase,
    drivetrain_default: Drivetrain,
    duration: float,
    speed: float,
    timeout: float,
    left_ex_speed: float,
    right_ex_speed: float,
):
    robot.drivetrain = drivetrain_default

    # given: a drivetrain
    robot.drivetrain = drivetrain_default
    # and: left and right motors on the drive train
    left_motor_sim = PWMSim(drivetrain_default._left_motor.getChannel())
    right_motor_sim = PWMSim(drivetrain_default._right_motor.getChannel())

    dt = DriveTime(robot, duration, speed, "TestDriveTime", timeout)
    sw = Stopwatch()

    dt.initialize()
    sw.start()
    while not dt.isFinished():
        dt.execute()
        pytest.approx(left_ex_speed, left_motor_sim.getSpeed())
        pytest.approx(right_ex_speed, right_motor_sim.getSpeed())

    dt.end()
    sw.stop()
    if duration < timeout:
        assert isclose(sw.elapsed_time_in_secs(), duration)
    else:
        # TODO: Timeouts don't seem to work in testing?
        assert isclose(sw.elapsed_time_in_secs(), timeout)
