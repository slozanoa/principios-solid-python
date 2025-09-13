from dataclasses import dataclass
from decorator_protocol import PaymentServiceDecoratorProtocol
from service_protocol import PaymentServiceProtocol
from commons import CustomerData, PaymentData, PaymentResponse

@dataclass
class PaymentServiceLogging(PaymentServiceDecoratorProtocol):
    wrappend: PaymentServiceProtocol

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: 
        print("start process transaction")
        response = self.wrappend.process_transaction(customer_data, payment_data)
        print("fininsh process transaction")
        return response

    def process_refund(self, transaction_id: str): 
        print(f"start process refund using: {transaction_id}")

        response = self.wrappend.process_refund(transaction_id)
        print("Fininsh process refund")
        return response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ):
        print("start process recurring")
        print("Fininsh process recurring")