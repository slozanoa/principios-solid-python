
from dataclasses import dataclass
from typing import Optional, Self

from factory import PaymentProcessorFactory
from commons import CustomerData, PaymentData, PaymentResponse
from processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol
)
from notifiers import NotifierProtocol
from validators import CustomerValidator, PaymentDataValidator
from loggers import TransactionLogger
from service_protocol import PaymentServiceProtocol
from listeners import ListenersManager
@dataclass
class PaymentService(PaymentServiceProtocol):
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    customer_validator: CustomerValidator
    payment_validator: PaymentDataValidator
    logger: TransactionLogger
    listener: ListenersManager
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None
    refund_processor: Optional[RefundProcessorProtocol] = None

    @classmethod
    def create_with_payment_processor(
        cls, payment_data: PaymentData, **kwargs
    ) -> Self:
        try:
            processor = PaymentProcessorFactory.create_payment_processor(
                payment_data
            )
            return cls(payment_processor=processor, **kwargs)
            
        except ValueError as e:
            print("Error creando la clase")
            raise e

    def set_notifier(self, notifier: NotifierProtocol):
        print("Changing the notifier implementación")
        self.notifier = notifier


    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        self.customer_validator.validate(customer_data)
        self.payment_validator.validate(payment_data)
        payment_response = self.payment_processor.process_transaction(
            customer_data, payment_data
        )
        self.listener.notifyAll(f"pago exitoso al evento: {payment_response.transaction_id}")
        self.notifier.send_confirmation(customer_data)
        self.logger.log_transaction(
            customer_data, payment_data, payment_response
        )
        return payment_response

    def process_refund(self, transaction_id: str):
        if not self.refund_processor:
            raise Exception("this processor does not support refunds")
        refund_response = self.refund_processor.refund_payment(transaction_id)
        self.logger.log_refund(transaction_id, refund_response)
        return refund_response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ):
        if not self.recurring_processor:
            raise Exception("this processor does not support recurring")
        recurring_response = self.recurring_processor.setup_recurring_payment(
            customer_data, payment_data
        )
        self.logger.log_transaction(
            customer_data, payment_data, recurring_response
        )
        return recurring_response
