from threading import Thread
from obj import admin_processes
from time import sleep
from datetime import date


class ActivationThread(Thread):
    def run(self):
        database = None
        while True:
            suspended_users = database.get_suspended_users()
            for suspended_user in suspended_users:
                if suspended_user.suspension_start == date.today():
                    admin_processes.deactivated_user(suspended_user, database)
                if suspended_user.suspension_end < date.today():
                    suspended_user.activated = True
                    suspended_user.is_suspended = False
                    database.commit_info()
            sleep(300)


def begin(database_handler):
    thread = ActivationThread()
    thread.database = database_handler
    thread.run()

