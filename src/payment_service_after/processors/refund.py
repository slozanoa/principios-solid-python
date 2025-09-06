from typing import Protocol
from payment_service_after.commons import PaymentResponse


class RefundProcessorProtocol(Protocol):
    def refund_payment(self, transaction_id:str) -> PaymentResponse: ...