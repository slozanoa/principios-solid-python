from typing import Optional, Protocol
from commons import CustomerData, PaymentData, PaymentResponse
from processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol
)
from notifiers import NotifierProtocol
from validators import CustomerValidator, PaymentDataValidator
from loggers import TransactionLogger
class PaymentServiceProtocol(Protocol):
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    customer_validator: CustomerValidator
    payment_validator: PaymentDataValidator
    logger: TransactionLogger
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None
    refund_processor: Optional[RefundProcessorProtocol] = None

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def process_refund(self, transaction_id: str): ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ): ...