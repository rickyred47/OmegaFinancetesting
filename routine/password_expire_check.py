from threading import Thread
from obj import email_manager
from time import sleep
from datetime import datetime

email_string = '''Your password is expiring soon.

Please log into Omega Finance sometime in the next 3 days to change your password, or you will be locked out.

Thanks,
The Omega Finance Team'''

class PasswordThread(Thread):

    def run(self):
        # Run indefinitely
        while True:
            # Check if current hour is 0.
            current_time = datetime.now()
            if not current_time.hour:
                # Go through all users and detect if password is 3 days from expiring
                userlist = self.db.get_user_accounts()
                for user in userlist:
                    days_away = (user.password_expire_date.replace(tzinfo=None) - current_time).days
                    if days_away == 3:
                        # Send email
                        email_manager.send_email(user.email, 'Upcoming Password Expiration', email_string)

            # Sleep for an hour
            sleep(3600)


def begin(database_handler):
    thread = PasswordThread()
    thread.db = database_handler
    thread.run()
