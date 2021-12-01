from ..internal import BankAccount
import logging
import datetime
from datetime import date

L = logging.getLogger(__name__)

class AgiosBankAccount(BankAccount):
    def __init__(self, owner : str, initial_balance : int, bank_account : "BankAccount"):
        super().__init__(owner, initial_balance)
        self.bank_account = bank_account
        self.neg_date = None

    def __check_for_agios(self, value, transaction_date : datetime):
        if not self.neg_date is None:
            bank_amount = (transaction_date - self.neg_date).days
            L.info(f'Credit to bank: amt={bank_amount}')
            self.transfer_to(self.bank_account, bank_amount, transaction_date)
            self.neg_date = None

    def _credit(self, value, transaction_date : datetime):
        self.__check_for_agios(value, transaction_date)
        super()._credit(value, transaction_date)

    def transfer_to(self, recipient, value, transaction_date : datetime):
        super().transfer_to(recipient, value, transaction_date)
        if self.neg_date is None and self.balance < 0:
            L.warning(f'Balance turns negative on {transaction_date}')
            self.neg_date = transaction_date
