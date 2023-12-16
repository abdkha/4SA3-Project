# notification_service.py
from subject import Subject

class NotificationService(Subject):
    def send_notification(self, data):
        # Send notifications to all registered users (observers)
        self.notify(data)
