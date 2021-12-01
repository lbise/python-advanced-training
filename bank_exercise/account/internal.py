import logging
import sys
import datetime
import numpy

L = logging.getLogger(__name__)

class BankAccount(object):
    def __init__(self, owner : str, initial_balance : int):
        self.owner = owner
        self.balance = initial_balance
        self.max_value = None
        self.balance_history = [initial_balance]

    def __add__(self, other):
        if self.owner != other.owner:
            return None
        return BankAccount(self.owner, self.balance + other.balance)

    def monitor(func):
        def wrapper(self, recipient, value, transaction_date : datetime):
            if self.max_value is None or self.max_value < value:
                L.warning(f'{self.owner} New highest value transferred: {value}')
            func(self, recipient, value, transaction_date)
            self.max_value = value

        return wrapper

    def print(self):
        L.info('{} balance={}'.format(self.owner, self.balance))

    def add_balance(self, value):
        self.balance += value
        self.balance_history.append(self.balance)

    def _credit(self, value, transaction_date : datetime):
        L.debug(f'{self.owner} credit={value}')
        self.add_balance(value)

    @monitor
    def transfer_to(self, recipient, value, transaction_date : datetime):
        self.add_balance(-value)
        recipient._credit(value, transaction_date)

    def plot(self, ax):
        ax.plot(self.balance_history, label=self.owner)
