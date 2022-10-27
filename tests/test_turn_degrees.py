from commands1 import Command
import pytest
from wpilib import IterativeRobotBase
from commands.turn_degrees import TurnDegrees
from subsystems.drivetrain import Drivetrain

from wpilib.simulation import AnalogGyroSim
from wpilib.simulation import PWMSim


@pytest.fixture(scope="function")
def drivetrain_default(robot: IterativeRobotBase):
    return Drivetrain(
        robot, "TestDrivetrain", "../tests/test_configs/drivetrain_default.ini"
    )


@pytest.fixture(scope="function")
def command_default(robot: IterativeRobotBase, drivetrain_default: Drivetrain):
    robot.drivetrain = drivetrain_default
    return TurnDegrees(robot, 90.0, 1.0, 2.0, "TestTurnDegrees", 15)


@pytest.mark.skip(reason="The Gyro is no longer on the robot")
def update_gyro(drivetrain_default: Drivetrain, command_default: Command):
    gyro_sim = AnalogGyroSim(drivetrain_default._gyro.getChannel())

    current = gyro_sim.getAngle()
    degrees_left = command_default._target_degrees - current
    if degrees_left >= 0:
        gyro_sim.setAngle(gyro_sim.getAngle() + 1.0)
    else:
        gyro_sim.setAngle(gyro_sim.getAngle() - 1.0)


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_init_default(command_default: TurnDegrees):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.drivetrain is not None
    assert command_default.getName() == "TestTurnDegrees"
    # Timeout is no longer accessible
    # assert command_default.timeout == 15
    assert command_default._speed == 1.0
    assert command_default._degrees_change == 90.0
    assert command_default._degree_threshold == 2.0


def test_init_full(robot: IterativeRobotBase, drivetrain_default: Drivetrain):
    robot.drivetrain = drivetrain_default
    td = TurnDegrees(robot, -30.0, 0.5, 5.0, "CustomTurnDegrees", 5)
    assert td is not None
    assert td.robot is not None
    assert td.robot.drivetrain is not None
    assert td.getName() == "CustomTurnDegrees"
    # Timeout is no longer accessible
    # assert td.timeout == 5
    assert td._speed == 0.5
    assert td._degrees_change == -30.0
    assert td._degree_threshold == 5.0


def test_initialize(command_default: TurnDegrees):
    command_default.initialize()
    assert command_default._target_degrees == 90


@pytest.mark.skip("No longer using the gyro")
@pytest.mark.parametrize(
    "initial_angle,target_angle,threshold,speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 1.0, 1.0, -1.0, -1.0),
        (10.0, 30.0, 2.0, 1.0, -1.0, -1.0),
        (20.0, 60.0, 5.0, 0.5, -0.5306122448979592, -0.5306122448979592),
        (20.0, -60.0, 10.0, 1.0, 1.0, 1.0),
        (10.0, -30.0, 2.0, 0.5, 0.5306122448979592, 0.5306122448979592),
    ],
)
def test_execute(
    robot: IterativeRobotBase,
    drivetrain_default: Drivetrain,
    initial_angle: float,
    target_angle: float,
    threshold: float,
    speed: float,
    left_ex_speed: float,
    right_ex_speed: float,
):
    robot.drivetrain = drivetrain_default
    td = TurnDegrees(robot, target_angle, speed, threshold, "CustomTurnDegrees", 15)
    assert td is not None

    # and: the robot drive motors are real
    left_m = PWMSim(drivetrain_default._left_motor.getChannel())
    right_m = PWMSim(drivetrain_default._right_motor.getChannel())

    # hal_data['analog_gyro'][1]['angle'] = initial_angle
    td.initialize()
    td.execute()
    pytest.approx(left_ex_speed, left_m.getSpeed())
    pytest.approx(right_ex_speed, right_m.getSpeed())


@pytest.mark.skip("No longer using the gyro, Figure out how the new ADXRS450_Gyro")
@pytest.mark.parametrize(
    "initial_angle,target_angle,threshold,fake_angle,finished",
    [
        (0.0, 0.0, 1.0, 0.0, True),
        (10.0, 30.0, 2.0, 37.0, False),
        (20.0, 60.0, 5.0, 76.0, True),
        (20.0, -60.0, 10.0, -20.0, False),
        (10.0, -30.0, 2.0, -21.0, True),
    ],
)
def test_is_finished(
    robot,
    drivetrain_default,
    hal_data,
    initial_angle,
    target_angle,
    threshold,
    fake_angle,
    finished,
):
    robot.drivetrain = drivetrain_default
    td = TurnDegrees(robot, target_angle, 1.0, threshold, "CustomTurnDegrees", 15)
    assert td is not None
    hal_data["analog_gyro"][1]["angle"] = initial_angle
    td.initialize()
    hal_data["analog_gyro"][1]["angle"] = fake_angle
    assert td.isFinished() is finished


@pytest.mark.skip("No longer using the gyro, Figure out how the new ADXRS450_Gyro")
@pytest.mark.parametrize(
    "initial_angle,target_angle,threshold,speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 1.0, 1.0, 0.0, 0.0),
        (10.0, 30.0, 2.0, 1.0, -1.0, -1.0),
        (20.0, 60.0, 5.0, 0.5, -0.5, -0.5),
        (20.0, -60.0, 10.0, 1.0, 1.0, 1.0),
        (10.0, -30.0, 2.0, 0.5, 0.5, 0.5),
    ],
)
def test_command_full(
    robot,
    drivetrain_default,
    initial_angle,
    target_angle,
    threshold,
    speed,
    left_ex_speed,
    right_ex_speed,
):
    robot.drivetrain = drivetrain_default
    td = TurnDegrees(robot, target_angle, speed, threshold, "CustomTurnDegrees", 15)
    assert td is not None
    # hal_data['analog_gyro'][1]['angle'] = initial_angle
    td.initialize()
    while not td.isFinished():
        td.execute()
        # update_gyro(hal_data, td)
        # assert hal_data['pwm'][1]['value'] == left_ex_speed
        # assert hal_data['pwm'][2]['value'] == right_ex_speed
    td.end()
    # assert isclose(hal_data['analog_gyro'][1]['angle'], initial_angle + target_angle, threshold)
