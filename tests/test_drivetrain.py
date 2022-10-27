import pytest
from wpilib import IterativeRobotBase
from subsystems.drivetrain import Drivetrain

from wpilib.simulation import PWMSim


@pytest.fixture(scope="function")
def drivetrain_default(robot: IterativeRobotBase):
    return Drivetrain(
        robot, "TestDriveTrain", "../tests/test_configs/drivetrain_default.ini"
    )


def test_drivetrain_default(drivetrain_default: Drivetrain):
    assert drivetrain_default is not None
    assert drivetrain_default._left_motor is not None
    assert drivetrain_default._right_motor is not None
    assert drivetrain_default._robot_drive is not None
    # No gyro for 2022
    assert drivetrain_default.is_gyro_enabled() is False
    assert drivetrain_default.get_arcade_rotation_modifier() == -1


def test_drivetrain_channels_0_1(robot: IterativeRobotBase):
    # given: a drivetrain
    dt = Drivetrain(
        robot, "TestDriveTrain", "../tests/test_configs/drivetrain_channels_0_1.ini"
    )

    # then: the drivetrain should be valid, and there should motors
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None

    # and: the robot drive motors are real
    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    # then: left motor is initialized and zero latched
    assert left_m.getInitialized() is True
    assert left_m.getRawValue() == 0.0
    # Determine how to check this accurately. Check safety enabled? What is zero latch?
    assert left_m.getZeroLatch() is False

    # and: right motor is initialized and zero latched
    assert right_m.getInitialized() is True
    assert right_m.getRawValue() == 0.0
    # Determine how to check this accurately. Check safety enabled? What is zero latch?
    assert right_m.getZeroLatch() is False


@pytest.mark.parametrize(
    "left_speed,right_speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.5, 0.0, 0.0),
        (1.0, 1.0, 0.0, 0.0),
        (-0.5, -0.5, 0.0, 0.0),
        (-1.0, -1.0, 0.0, 0.0),
    ],
)
def test_drivetrain_zero_speed(
    robot: IterativeRobotBase,
    left_speed: float,
    right_speed: float,
    left_ex_speed: float,
    right_ex_speed: float,
):
    # given: a drivetrain
    dt = Drivetrain(
        robot, "TestDrivetrain", "../tests/test_configs/drivetrain_zero_speed.ini"
    )

    # then: the drivetrain should be valid, and there should motors
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert dt._max_speed == 0.0

    # and: the robot drive motors are real
    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    # and: the drivetrain is "tank drived" at the left and right speed
    dt.tank_drive(left_speed, right_speed)

    # the speed of the left and right motor should be as set
    pytest.approx(left_ex_speed, left_m.getSpeed())
    pytest.approx(right_ex_speed, right_m.getSpeed())


@pytest.mark.parametrize(
    "left_speed,right_speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.5, 0.25, -0.25),
        (1.0, 1.0, 0.5, -0.5),
        (-0.5, -0.5, -0.25, 0.25),
        (-1.0, -1.0, -0.5, 0.5),
    ],
)
def test_drivetrain_half_speed(
    robot: IterativeRobotBase,
    left_speed: float,
    right_speed: float,
    left_ex_speed: float,
    right_ex_speed: float,
):
    # given: a drivetrain
    dt = Drivetrain(
        robot, "TestDrivetrain", "../tests/test_configs/drivetrain_half_speed.ini"
    )

    # then: the drivetrain should have a left and right motor with a max spped of 0.5
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert dt._max_speed == 0.5

    # and: the robot drive motors are real
    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    # and the drivetrain is "tank drived" at the left right
    dt.tank_drive(left_speed, right_speed)

    # the speed of the left and right motor should be less then it was
    assert abs(left_m.getSpeed()) - abs(left_ex_speed) < 0.05
    assert abs(right_m.getSpeed()) - abs(right_ex_speed) < 0.05


@pytest.mark.parametrize(
    "left_speed,right_speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.5, 0.375, -0.375),
        (1.0, 1.0, 0.75, -0.75),
        (-0.5, -0.5, -0.375, 0.375),
        (-1.0, -1.0, -0.75, 0.75),
    ],
)
def test_drivetrain_3_4_speed(
    robot: IterativeRobotBase,
    left_speed: float,
    right_speed: float,
    left_ex_speed: float,
    right_ex_speed: float,
):
    # given: a drivetrain
    dt = Drivetrain(
        robot, "TestDrivetrain", "../tests/test_configs/drivetrain_3_4_speed.ini"
    )

    # then: the drivetrain should have a left and right motor and 3/4 max speed
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert dt._max_speed == 0.75

    # and: the robot drive motors are real
    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    # and the drivetrain is "tank drived" at the left right
    dt.tank_drive(left_speed, right_speed)

    # then: the speed of the left and right motor should be less than 0.5
    assert abs(left_m.getSpeed()) - abs(left_ex_speed) < 0.05
    assert abs(right_m.getSpeed()) - abs(right_ex_speed) < 0.05


@pytest.mark.parametrize(
    "left_speed,right_speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.5, 0.5306122448979592, -0.5306122448979592),
        (1.0, 1.0, 1.0, -1.0),
        (-0.5, -0.5, -0.5306122448979592, 0.5306122448979592),
        (-1.0, -1.0, -1.0, 1.0),
    ],
)
def test_drivetrain_full_speed(
    robot: IterativeRobotBase,
    left_speed: float,
    right_speed: float,
    left_ex_speed: float,
    right_ex_speed: float,
):
    # given: a drivetrain
    dt = Drivetrain(
        robot, "TestDriveTrain", "../tests/test_configs/drivetrain_full_speed.ini"
    )

    # then: the drivetrain should have a left and right motor at full speed
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert dt._max_speed == 1.0

    # and: the robot drive motors are real
    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    # and the drivetrain is "tank drived" at the left right
    dt.tank_drive(left_speed, right_speed)

    # then the speed of the left and the right motor should be the speed
    pytest.approx(left_ex_speed, left_m.getSpeed())
    pytest.approx(right_ex_speed, right_m.getSpeed())


def test_drivetrain_left_inverted(robot: IterativeRobotBase):
    dt = Drivetrain(
        robot, "TestDriveTrain", "../tests/test_configs/drivetrain_left_inverted.ini"
    )
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None

    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    assert left_m.getInitialized() is True
    assert left_m.getSpeed() == 0.0
    assert left_m.getZeroLatch() is False
    assert right_m.getInitialized() is True
    assert right_m.getSpeed() == 0.0
    assert right_m.getZeroLatch() is False
    assert dt._left_motor.getInverted() is True
    assert dt._right_motor.getInverted() is False


def test_drivetrain_right_inverted(robot: IterativeRobotBase):
    dt = Drivetrain(
        robot, "TestDrivetrain", "../tests/test_configs/drivetrain_right_inverted.ini"
    )
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None

    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    assert left_m.getInitialized() is True
    assert left_m.getSpeed() == 0.0
    assert left_m.getZeroLatch() is False
    assert right_m.getInitialized() is True
    assert right_m.getSpeed() == 0.0
    assert right_m.getZeroLatch() is False

    assert dt._left_motor.getInverted() is False
    assert dt._right_motor.getInverted() is True


def test_drivetrain_left_disabled(robot: IterativeRobotBase):
    dt = Drivetrain(
        robot, "TestDrivetrain", "../tests/test_configs/drivetrain_left_disabled.ini"
    )
    assert dt is not None
    assert dt._left_motor is None
    assert dt._right_motor is not None
    assert dt._robot_drive is None


def test_drivetrain_right_disabled(robot: IterativeRobotBase):
    dt = Drivetrain(
        robot, "TestDrivetrain", "../tests/test_configs/drivetrain_right_disabled.ini"
    )
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is None
    assert dt._robot_drive is None
