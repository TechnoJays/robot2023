import glob
import logging

import wpilib
from commands2 import CommandScheduler, CommandBase, CommandGroupBase
from commands2 import TimedCommandRobot

from commands.autonomous_drive_commands import MoveFromLine
from robot_controller import RobotController

logging.basicConfig(level=logging.INFO)


def discover_config(file_pattern: str) -> list[str]:
    return glob.glob(file_pattern)


class RetrojaysRobot(TimedCommandRobot):
    SIM_SUBSYSTEMS_CONFIG_PATH = "../src/configs/subsystems.ini"
    SIM_JOYSTICK_CONFIG_PATH = "../src/configs/joysticks.ini"
    SIM_AUTONOMOUS_CONFIG_PATH = "../src/configs/autonomous.ini"

    TEST_SUBSYSTEMS_CONFIG_PATH = "../tests/test_configs/subsystems_default.ini"
    TEST_JOYSTICK_CONFIG_PATH = "../tests/test_configs/joysticks_default.ini"
    TEST_AUTONOMOUS_CONFIG_PATH = "../tests/test_configs/autonomous_default.ini"

    robot_controller: RobotController = None
    autonomous_command: CommandGroupBase = None

    def autonomousInit(self):
        # Schedule the autonomous command
        # autonomous_command = MoveFromLine(
        # self.robot_controller.drivetrain,
        # self.robot_controller.autonomous_config
        # )
        # TODO move into robot controller for better mgmt?
        autonomous_command = self.robot_controller.get_auto_choice()
        if autonomous_command == "MOVEFROMLINE":
            self.autonomous_command = MoveFromLine(self.controller.drivetrain, self.controller.autonomous_config)
            self.autonomous_command.schedule()
        else:
            pass

    def autonomousPeriodic(self):
        """
        This function is called periodically during autonomous.
        The scheduler is what runs the periodic processes for managing
        commands during autonomous
        """
        pass

    def autonomousExit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()


    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def disabledExit(self):
        pass

    def robotInit(self):
        """
        This function is called upon robot startup and creates the main "Robot Controller" which contains
        the majority of the robot code

        This function also checks if the robot is currently running as a simulation
        """
        if self.isTest():
            print("#### Running TEST MODE ####")
            self.robot_controller = RobotController(self,
                                                    self.TEST_SUBSYSTEMS_CONFIG_PATH,
                                                    self.TEST_JOYSTICK_CONFIG_PATH,
                                                    self.TEST_AUTONOMOUS_CONFIG_PATH)
        elif self.isSimulation():
            print("#### Running SIM MODE ####")
            self.robot_controller = RobotController(self,
                                                    self.SIM_SUBSYSTEMS_CONFIG_PATH,
                                                    self.SIM_JOYSTICK_CONFIG_PATH,
                                                    self.SIM_AUTONOMOUS_CONFIG_PATH)
        else:
            print("#### Running REAL MODE ####")
            self.robot_controller = RobotController(self)

        self.robot_controller.mappings()

    def robotPeriodic(self) -> None:
        """
        Ensures commands are run
        """
        self.robot_controller.update_sensors()
        CommandScheduler.getInstance().run()

    def teleopInit(self):
        if self.autonomous_command and self.autonomous_command.isScheduled():
            self.autonomous_command.cancel()

    def teleopPeriodic(self):
        """
        This function is called periodically during operator control.
        The scheduler is what runs the periodic processes for managing
        commands during autonomous
        """
        pass

    def testInit(self):
        pass

    def testPeriodic(self):
        """
        This function is called periodically during test mode.
        """
        pass

    @property
    def controller(self):
        return self.robot_controller


if __name__ == "__main__":
    wpilib.run(RetrojaysRobot)
