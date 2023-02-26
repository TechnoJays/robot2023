import wpilib
from commands2 import CommandScheduler
from commands2 import TimedCommandRobot

from robot_controller import RobotController


class RetrojaysRobot(TimedCommandRobot):

    def __init__(self, period: 0.02):
        super().__init__(period)
        self._robot_controller = None

    def autonomousInit(self):
        # Schedule the autonomous command
        # TODO move into robot controller for better mgmt?
        autonomous_command = self._robot_controller.get_auto_choice()
        autonomous_command.start()

    def testInit(self):
        pass

    def teleopInit(self):
        pass

    def disabledInit(self):
        pass

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self._robot_controller = RobotController(self)
        self._robot_controller.mappings()

    def autonomousPeriodic(self):
        """
        This function is called periodically during autonomous.
        The scheduler is what runs the periodioc processes for managing
        commands during autonomous
        """
        pass

    def teleopPeriodic(self):
        """
        This function is called periodically during operator control.
        The scheduler is what runs the periodic processes for managing
        commands during autonomous
        """
        CommandScheduler.getInstance().run()

    def testPeriodic(self):
        """
        This function is called periodically during test mode.
        """
        pass

    def controller(self) -> RobotController:
        """ Returns the robot controller managing all robot subsystems and operator interface"""
        return self._robot_controller


if __name__ == "__main__":
    wpilib.run(RetrojaysRobot)
