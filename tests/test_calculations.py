import pytest
from app.calculations import add,subtract,multiply,divide,BankAccount
from decimal import Decimal
import time
# what if we want to do this for more than 2 different sets of numbers , -- decorator pytest parameterized 
@pytest.fixture
def zero_bank_account():
	print("Lame! Creating a zero balance banck account......")
	return BankAccount()

@pytest.fixture
def bank_account():
	print("Creating a minimum(1220) balance bank account......")
	return BankAccount(1220)


@pytest.mark.parametrize("num1,num2,expected",[
	(1,3,4),
	(2,5,7),
	(23,535,558)],)
def test_add(num1,num2,expected):
	print("Testing add function......")
	assert add(num1,num2)==expected

def test_sub():
	print("Testing subtract function......")
	assert subtract(1,5) == -4

def test_multiply():
	print("Testing multiply function......")
	assert multiply(3,5) == 15

def test_divide():
	print("Testing divide function......")
	assert divide(5,5) == 1


# - --------- - - - - - - - - - - - - - - - - - - - - -

def test_account_balance(bank_account):
	assert bank_account.balance == 1220

def test_deposit_amount(bank_account):
	bank_account.deposit(1220)
	assert bank_account.balance  == 2440

def test_defualt_account_balance(zero_bank_account):
	bank_account = BankAccount()
	assert zero_bank_account.balance == 0

def test_withdraw_amount(bank_account):
	bank_account.withdraw(1220)
	assert bank_account.balance  == 0 

def test_interest_amount(bank_account):
	bank_account.interest()
	assert bank_account.balance == 1342.0000000000000000000000

def test_bank_transaction(zero_bank_account):
	zero_bank_account.deposit(1220)
	zero_bank_account.withdraw(20)
	assert zero_bank_account.balance  == 1200 

@pytest.mark.parametrize("deposited,withdrew,remaining_balance",[(12000,2000,10000),(200,100,100),(1299,99,1200)],)
def test_bank_transaction(zero_bank_account,deposited,withdrew,remaining_balance):
	zero_bank_account.deposit(deposited)
	zero_bank_account.withdraw(withdrew)
	assert zero_bank_account.balance == remaining_balance

# bank_account1 = BankAccount(1220)

# bank_account1.deposit(1220)
# bank_account1.withdraw(40)
# bank_account1.interest()
 
