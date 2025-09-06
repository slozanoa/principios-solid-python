from src.payment_service.notifiers.notifier import NotifierProtocol
from src.payment_service_after.commons.customer import CustomerData


class EmailNotifier(NotifierProtocol):
    def send_confirmation(self, customer_data: CustomerData):
        from email.mime.text import MIMEText

        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email or ""

        print("Email sent to", customer_data.contact_info.email)