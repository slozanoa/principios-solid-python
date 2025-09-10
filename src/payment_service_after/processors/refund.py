from typing import Protocol
from commons import PaymentResponse


class RefundProcessorProtocol(Protocol):
    def refund_payment(self, transaction_id:str) -> PaymentResponse: ...