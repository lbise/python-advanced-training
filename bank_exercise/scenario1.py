#!/usr/bin/env python3
import logging
from account.external.agios import AgiosBankAccount
from account.external.blocked import BlockedBankAccount
from account.internal import BankAccount
import matplotlib.pyplot as plt

from datetime import date
import datetime

def setup_logger(name, level):
    sim = logging.getLogger(name)
    strm = logging.StreamHandler()
    frmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    strm.setFormatter(frmt)
    sim.addHandler(strm)
    sim.setLevel(level)

if __name__ == '__main__':
    setup_logger('account.internal', logging.DEBUG)
    setup_logger('account.external.agios', logging.DEBUG)
    setup_logger('account.external.blocked', logging.DEBUG)

    bank = BankAccount("LCL", 10000)
    walmart = BankAccount("Walmart", 5000)
    alice = BankAccount("Alice Worz", 500)
    #bob = BankAccount("Bob Müller", 100)
    #bob = BlockedBankAccount("Bob Müller", 100)
    bob = AgiosBankAccount("Bob Müller", 100, bank)
    bob2 = BankAccount("Bob Müller", 1000)

    accounts = []
    accounts.append(bank)
    accounts.append(walmart)
    accounts.append(alice)
    accounts.append(bob)

    # Protected method (Can be accessed by child), it would be unwise to let users directly credit to their accounts
    # !! This is only detected by the linter and not the interpreter !!
    #bob._credit(10, date.today())

    # This is a private method (Should ot be accessed by child class or from instances)
    # !! This is only detected by the linter and not the interpreter !!
    #bob.__check_for_agio()

    logging.info('== BEFORE ============')
    for a in accounts:
        a.print()
    logging.info('======================')

    try:
        alice.transfer_to(walmart, 100, date.today())
        bob.transfer_to(walmart, 100, date.today())
        alice.transfer_to(bob, 100, date.today())
        bob.transfer_to(walmart, 200, date.today())
        alice.transfer_to(bob, 100, date.today() + datetime.timedelta(days=5))
        bob3 = bob + bob2
        bob3.print()
    except Exception as e:
        print('Cannot perform operation: {}'.format(e))

    logging.info('== AFTER ============')
    for a in accounts:
        a.print()
    logging.info('======================')

    fig, ax = plt.subplots()
    for a in accounts:
        a.plot(ax)

    ax.legend()
    plt.show()
