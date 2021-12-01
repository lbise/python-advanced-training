#!/usr/bin/env python3
import sys
import os
import datetime

#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from account.external.agios import AgiosBankAccount
from account.external.blocked import BlockedBankAccount
from account.internal import BankAccount

DEFAULT_OWNER1 = 'Jeanji'
DEFAULT_OWNER2 = 'Jeanmi'
VAL1 = 100
VAL2 = 200

def test_bank_account_transfer_to():
    value = 50
    account1 = BankAccount(DEFAULT_OWNER1, VAL1)
    account2 = BankAccount(DEFAULT_OWNER2, VAL2)

    account1.transfer_to(account2, value, datetime.date.today())
    assert account1.balance == VAL1 - value
    assert account2.balance == VAL2 + value

def test_blocked_bank_account():
    account1 = BlockedBankAccount(DEFAULT_OWNER1, VAL1)
    account2 = BankAccount(DEFAULT_OWNER2, VAL2)

    exception = False
    try:
        account1.transfer_to(account2, VAL1 + 1, datetime.date.today())
    except Exception as e:
        exception = True

    assert account1.balance == VAL1
    assert account2.balance == VAL2
    assert exception

def test_agios_bank_account():
    value = VAL1 + 1
    bank = BankAccount(DEFAULT_OWNER2, VAL2)
    account1 = AgiosBankAccount(DEFAULT_OWNER1, VAL1, bank)
    account2 = BankAccount(DEFAULT_OWNER2, VAL2)

    account1.transfer_to(account2, value, datetime.date.today())
    assert account1.balance == VAL1 - value
    assert account2.balance == VAL2 + value

    account2.transfer_to(account1, 1, datetime.date.today() + datetime.timedelta(days=1))
    assert account1.balance == VAL1 - value
    assert account2.balance == VAL2 + value - 1
    assert bank.balance == VAL2 + 1
