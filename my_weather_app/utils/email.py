# In utils/email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotification:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())
            print(f"Email sent to {recipient_email} successfully.")
        except Exception as e:
            print(f"Email sending failed: {e}")

# Example usage in main.py
if __name__ == "__main__":
    smtp_server = "smtp.office365.com"  # Replace with your SMTP server
    smtp_port = 587  # Replace with your SMTP server's port
    sender_email = "abdul.khan@hotmail.ca"  # Replace with your email
    sender_password = "#h#E67AP1234"  # Replace with your email password

    email_notifier = EmailNotification(smtp_server, smtp_port, sender_email, sender_password)

    recipient_email = "recipient@example.com"  # Replace with the recipient's email
    subject = "Weather Alert"
    message = "There is a weather alert for your location."

    email_notifier.send_email(recipient_email, subject, message)
