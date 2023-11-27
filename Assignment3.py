'''Class Relationships and Separation of Concerns'''
# Define the base class for all types of accounts
class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def get_account_number(self) -> str:
        return self.account_number

    def get_current_balance(self) -> float:
        return self.balance

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        # TODO: Implement withdrawal logic
        pass

    def overdraft_allowed(self) -> bool:
        # TODO: Implement overdraft logic
        pass

    def close_account(self) -> None:
        # TODO: Implement close account logic
        pass

# Define a subclass for savings accounts
class SavingsAccount(Account):
    def __init__(self, account_number, balance=0):
        super().__init__(account_number, balance)

    def minimum_balance(self) -> float:
        # TODO: Implement minimum balance logic for savings account
        pass

    def withdraw(self, amount: float) -> None:
        # TODO: Implement withdrawal logic specific to SavingsAccount
        pass

# Define a subclass for checking accounts
class CheckingAccount(Account):
    def __init__(self, account_number, balance=0):
        super().__init__(account_number, balance)

    def overdraft_allowed(self) -> bool:
        # TODO: Implement overdraft logic for checking account
        pass

    def placeholder_method(self) -> None:
        # Placeholder method in CheckingAccount
        pass

# Define the Bank class to manage accounts
class Bank:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account: Account) -> None:
        self.accounts[account.get_account_number()] = account

    def remove_account(self, account_number: str) -> None:
        if account_number in self.accounts:
            del self.accounts[account_number]

    def search_account(self, account_number: str) -> Account:
        return self.accounts.get(account_number, None)

    def open_account(self, account_number: str, account_type: str = 'Savings') -> Account:
        if account_number not in self.accounts:
            if account_type == 'Savings':
                account = SavingsAccount(account_number)
            elif account_type == 'Checking':
                account = CheckingAccount(account_number)
            else:
                raise ValueError("Invalid account type")
            
            self.add_account(account)
            return account
        else:
            raise ValueError("Account already exists")

# Define the main program class
class Program:
    def __init__(self, bank: Bank):
        self.bank = bank

    def run(self) -> None:
        while True:
            print("Banking Menu:")
            print("1. Open Account")
            print("2. Show All Accounts")
            print("3. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.open_account()
            elif choice == '2':
                self.show_all_accounts()
            elif choice == '3':
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def open_account(self) -> None:
        account_number = input("Enter account number: ")
        account_type = input("Enter account type (Savings/Checking): ")

        try:
            account = self.bank.open_account(account_number, account_type)
            print(f"Account {account.get_account_number()} opened successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def show_all_accounts(self) -> None:
        print("All Accounts:")
        for account_number, account in self.bank.accounts.items():
            print(f"Account {account_number}: Balance ${account.get_current_balance()}")

# Example usage
if __name__ == "__main__":
    bank = Bank()
    banking_program = Program(bank)
    banking_program.run()
