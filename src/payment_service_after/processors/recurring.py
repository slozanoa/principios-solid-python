from typing import Protocol
from payment_service_after.commons import CustomerData, PaymentData, PaymentResponse

class RecurringPaymentProcessorProtocol(Protocol):
    def setup_recurring_payment(self, customer_data: CustomerData, payment_data:PaymentData) -> PaymentResponse: ...