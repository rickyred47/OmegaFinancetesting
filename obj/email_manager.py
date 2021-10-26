import smtplib

gmail_user = 'omega.finance.corp@gmail.com'
gmail_password = 'yf4vJA39qHh8QHd'
gmail_smtp_server = ('smtp.gmail.com', 465)


def send_email(recipient_list, subject, body):
    """
    Sends an email to everyone on the recipient list.

    Arguments:
        recipient_list (list) : The list of recipients.
        subject (str) : The subject of the message.
        body (str) : The body of the message.
    """
    # Create the email text
    email_text = f'From: {gmail_user}\n'
    email_text += f'To: {", ".join(recipient_list)}\n'
    email_text += f'Subject: {subject}\n\n'
    email_text += body

    # Attempt to send the email
    smtp_server = smtplib.SMTP_SSL(gmail_smtp_server[0], gmail_smtp_server[1])
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(gmail_user, recipient_list, email_text)
    smtp_server.close()
