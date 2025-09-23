from listener import Listener


class AccountabilityListner[T](Listener):
    def notify(self, event: T):
        print(f"Notificando evento {event}")