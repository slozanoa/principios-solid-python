from dataclasses import dataclass
from src.payment_service.notifiers.notifier import NotifierProtocol
from src.payment_service_after.commons.customer import CustomerData


@dataclass
class SMSNotifier(NotifierProtocol):
    sms_gateway: str
    def send_confirmation(self, customer_data: CustomerData):
        phone_number = customer_data.contact_info.phone

        print(
            f"send the sms using {self.sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
        )