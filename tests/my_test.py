import pytest
from app.calculations import add, BankAccount, InsufficiantFunds


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (-1, 5, 4)
])
def test_add(num1, num2, expected):
    print("test passed")
    sum = add(num1, num2)

    assert sum == expected


@pytest.fixture
def bank_account_init():
    return BankAccount(100)


@pytest.fixture
def zero_bank_account_init():
    return BankAccount()


def test_bank_set_initial_amount():
    bank_account = BankAccount(50)

    assert bank_account.balance == 50


def test_bank_default_amount():
    bank_account = BankAccount()

    assert bank_account.balance == 0


def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)

    assert bank_account.balance == 30


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_banl_transaction(zero_bank_account_init, deposited, withdrew, expected):
    zero_bank_account_init.deposit(deposited)
    zero_bank_account_init.withdraw(withdrew)

    assert zero_bank_account_init.balance == expected


def test_insufficient_funds(bank_account_init):
    with pytest.raises(InsufficiantFunds):
        bank_account_init.withdraw(200)

 