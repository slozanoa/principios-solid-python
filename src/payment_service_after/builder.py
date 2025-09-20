from dataclasses import dataclass
from typing import Optional, Self
from processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol
)
from notifiers import NotifierProtocol, EmailNotifier, SMSNotifier
from validators import CustomerValidator, PaymentDataValidator
from loggers import TransactionLogger
from commons import CustomerData,PaymentData
from factory import PaymentProcessorFactory
from service import PaymentService
@dataclass
class PaymentServiceBuilder:
    payment_processor: Optional[PaymentProcessorProtocol] = None
    notifier: Optional[NotifierProtocol] = None
    customer_validator: Optional[CustomerValidator] = None
    payment_validator: Optional[PaymentDataValidator] = None
    logger: Optional[TransactionLogger] = None
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None
    refund_processor: Optional[RefundProcessorProtocol] = None

    def set_logger(self) -> Self:
        self.logger = TransactionLogger()
        return self
    
    def set_payment_validator(self) -> Self:
        self.payment_validator = PaymentDataValidator()
        return self

    def set_customer_validator(self) -> Self:
        self.customer_validator = CustomerValidator()
        return self
    
    def set_payment_processor(self, payment_data: PaymentData) -> Self:
        self.payment_processor = PaymentProcessorFactory.create_payment_processor(payment_data)
        return self
    
    def set_notifier(self, customer_data: CustomerData)-> Self:
        if customer_data.contact_info.email:
            self.notifier = EmailNotifier()
            return self
        if customer_data.contact_info.phone:
            self.notifier = SMSNotifier(sms_gateway="MycustomGateway")
            return self
        raise ValueError("No se puede seleccionar clase de notificación")
    
    def build(self):
        if not all(
            [
                self.payment_processor,
                self.notifier,
                self.customer_validator,
                self.payment_validator,
                self.logger,
            ]
        ):
            missing =[
                name
                for name, value in [
                    ("payment_processor",self.payment_processor),
                    ("notifier",self.notifier),
                    ("customer_validator",self.customer_validator),
                    ("payment_validator",self.payment_validator),
                    ("logger",self.logger),
                ]
                if value is None
            ]
            return ValueError(f"Missing dependencies: {missing}")

        return PaymentService(
            payment_processor=self.payment_processor,
            notifier=self.notifier,
            customer_validator=self.customer_validator,
            payment_validator=self.payment_validator,
            logger=self.logger
        )

