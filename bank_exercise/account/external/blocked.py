import logging
from ..internal import BankAccount
import datetime

L = logging.getLogger(__name__)

class BlockedBankAccount(BankAccount):
    def __init__(self, owner : str, initial_balance : int):
        super().__init__(owner, initial_balance)

    def transfer_to(self, recipient, value, transaction_date : datetime):
        if self.balance < value:
            L.error('Cannot overdraw')
            raise Exception('Cannot overdraw')

        super().transfer_to(recipient, value, transaction_date)
