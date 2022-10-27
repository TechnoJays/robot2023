import wpilib
from wpilib import SmartDashboard

from commands1 import Command
from commands1 import Scheduler
from oi import OI
from subsystems.climbing import Climbing
from subsystems.drivetrain import Drivetrain
from subsystems.shooter import Shooter
from subsystems.vacuum import Vacuum


class MyRobot(wpilib.TimedRobot):

    oi: OI = None
    drivetrain: Drivetrain = None
    climbing: Climbing = None
    shooter: Shooter = None
    vacuum: Vacuum = None
    autonomous_command: Command = None

    def autonomousInit(self):
        # Schedule the autonomous command
        self.autonomous_command = self.oi.get_auto_choice()
        self.autonomous_command.start()

    def testInit(self):
        pass

    def teleopInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def disabledInit(self):
        pass

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.oi = OI(self)
        self.drivetrain = Drivetrain(self)
        self.climbing = Climbing(self)
        self.shooter = Shooter(self)
        self.vacuum = Vacuum(self)
        self.oi.setup_button_bindings()
        # wpilib.CameraServer.launch('subsystems/vision.py:main')
        wpilib.CameraServer.launch()

    def autonomousPeriodic(self):
        """
        This function is called periodically during autonomous.
        The scheduler is what runs the periodioc processes for managing
        commands during autonomous
        """
        Scheduler.getInstance().run()
        pass

    def teleopPeriodic(self):
        """
        This function is called periodically during operator control.
        The scheduler is what runs the periodic processes for managing
        commands during autonomous
        """
        SmartDashboard.putString("Color Target", str(self.oi.get_game_message()))
        Scheduler.getInstance().run()

    def testPeriodic(self):
        """
        This function is called periodically during test mode.
        """
        pass


if __name__ == "__main__":
    wpilib.run(MyRobot)
