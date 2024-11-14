# Test is either a function or a method within a class
# Assert - through means nothing is going to happen, false means it would throw an error
# Also the naming of the function matters, and each function name must start with "test"
# So we use the -v flag to get a more verbose output on our testing and we use the -s flag to get the output of what we printed out in our code.
# We can use the parameterize method in pytest to test with multiple parameters, this method takes 3 parameters as well as an array. The array takes a list of different values based on what you want to test with


# Fixtures - helps you to write tests to minimize the amount of repitive codes. So what fixtures do basically is they help reduce the number of codes for tests, so you can write a test all you'd just need tos to call the name of the fixture as a parameter to the test which would cakk the value and they you can as well assert that
# Also a fixture is a fuction that runs before a specific test case, we can then use this fixture for all of our test
import pytest
from app.calculations import add,subtract,multiply,divide,BankAccount,InsufficientFunds




@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()



@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected", [
    (3,2,5),
    (7,1,8),
    (12,4,16)
])
def test_add(num1,num2,expected):
    print("testing add function")
    assert add(num1,num2)  == expected
    
def test_subract():
    assert subtract(9,4) == 5

def test_multiply():
    assert multiply(3,4) == 12
    
def test_divide():
    assert divide(25,5) == 5

     

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50
    
def test_bank_default_amount(zero_bank_account):
    print("testing my bank account")
    assert zero_bank_account.balance == 0
    
def test_withdrawal(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    
def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80
    
def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55




# Using  fixtures and parameterize for our test cases 

@pytest.mark.parametrize("deposited,withdrew,expectedamount", [
    (200,100,100),
    (50,10,40),
    (1200,200,1000)
    
])
def test_bank_transaction(zero_bank_account,deposited,withdrew,expectedamount):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expectedamount
    
# Now in this case when you're running a test like for example the user trying to withdraw more than they have you'd have to tell python that this is expected and in cases like this it should throw an error or something, so we use the with pytest.raises(Exception) telling it that if this happens do so and so and mind you in our normal python logic we've already caught this case we're just testing it out before we deploy our application.
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds): 
        bank_account.withdraw(200)
    