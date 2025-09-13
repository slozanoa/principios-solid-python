from typing import Protocol

from commons import CustomerData, PaymentData, PaymentResponse
from service_protocol import PaymentServiceProtocol


class PaymentServiceDecoratorProtocol(Protocol):
    wrappend: PaymentServiceProtocol

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def process_refund(self, transaction_id: str): ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ): ...