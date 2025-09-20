from service import PaymentService

from processors import StripePaymentProcessor

from notifiers import EmailNotifier, NotifierProtocol, SMSNotifier

from builder import PaymentServiceBuilder
from commons import CustomerData, ContactInfo,PaymentData
def get_email_notifier()-> EmailNotifier:
    return EmailNotifier()

def get_sms_notifier()-> SMSNotifier:
    return SMSNotifier(sms_gateway="smsgatewayExample")

def get_notifier_implementation(customer_data: CustomerData) -> NotifierProtocol:
    if customer_data.contact_info.phone:
        return get_sms_notifier()
    if customer_data.contact_info.email:
        return get_email_notifier()
    
    raise ValueError("No se puede elegir la estategia correcta")

def get_customer_data() -> CustomerData:
    contact_info = ContactInfo(email="jhon@gmail.com")
    customer_data = CustomerData(name="jhon doe", contact_info=contact_info)
    return customer_data

if __name__ == "__main__":
    customer_data = get_customer_data()

    payment_data = PaymentData(amount=100, source="tok_visa", currency="USD")
    builder = PaymentServiceBuilder()
    service = (
        builder.set_logger()
        .set_customer_validator()
        .set_payment_validator()
        .set_payment_processor(payment_data)
        .set_notifier(customer_data)
        .build()
        )
