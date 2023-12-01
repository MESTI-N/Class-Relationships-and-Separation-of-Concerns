'''Class Relationships and Separation of Concerns'''
# Define the base class for all types of accounts
class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def get_account_number(self):
        return self.account_number

    def get_current_balance(self):
        return self.balance

    def deposit(self, amount: float):
        self.balance += amount

    def withdraw(self, amount: float):
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative.")
        if self.balance < amount:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount

    def overdraft_allowed(self, overdraft_limit: float):
        if self.balance < 0 and abs(self.balance) > overdraft_limit:
            raise ValueError("Overdraft limit exceeded.")

    def close_account(self):
        if self.balance != 0:
            raise ValueError("Cannot close account with a non-zero balance.")


# Define a subclass for savings accounts
class SavingsAccount(Account):
    def __init__(self, account_number, balance=0, min_balance=0):
        super().__init__(account_number, balance)
        self.min_balance = min_balance

    def withdraw(self, amount: float):
        if amount < 0:
            raise ValueError("Withdrawal amount must be positive.")

        if self.balance - amount < self.min_balance:
            raise ValueError("Withdrawal exceeds allowed minimum balance.")
        else:
            super().withdraw(amount)

# Update the withdraw method in the CheckingAccount class
class CheckingAccount(Account):
    def __init__(self, account_number, balance=0, overdraft_limit=0):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float):
        if amount < 0:
            raise ValueError("Withdrawal amount must be positive.")

        if self.balance - amount < -self.overdraft_limit:
            raise ValueError("Withdrawal exceeds allowed overdraft limit.")
        else:
            self.balance -= amount


# Define the Bank class to manage accounts
class Bank:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: Account):
        self.accounts.append(account)

    def remove_account(self, account_number: str):
        self.accounts = [acc for acc in self.accounts if acc.get_account_number() != account_number]

    def search_account(self, account_number: str):
        return next((acc for acc in self.accounts if acc.get_account_number() == account_number), None)

    def open_account(self, account_number: str, account_type: str = 'savings', **kwargs):
        if account_number not in [acc.get_account_number() for acc in self.accounts]:
            if account_type == 'savings':
                account = SavingsAccount(account_number, **kwargs)
            elif account_type == 'checking':
                account = CheckingAccount(account_number, **kwargs)
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
        self.selected_account = None

    def run(self):
        self.show_main_menu()

    def show_main_menu(self):
        while True:
            print("Banking Main Menu:")
            print("1. Open Account (Bonus)")
            print("2. Select Account")
            print("3. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.open_account()  # Bonus feature
            elif choice == '2':
                self.select_account()
            elif choice == '3':
                print("Exiting the application. Goodbye!")
                return   # This will exit the show_main_menu method
            else:
                print("Invalid choice. Please try again.")

    def show_account_menu(self):
        while True:
            if self.selected_account is None:
                print("You don't have an account selected. Please select an account first.")
                self.show_main_menu()  # Go back to the main menu to select an account
                break

            print("Account Menu:")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Exit Account")

            choice = input("Enter your choice: ").lower()
            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                print("Exiting Account Menu.")
                self.show_main_menu()  # Go back to the main menu
                return
            else:
                print("Invalid choice. Please try again.")

    def select_account(self):
        account_number = input("Enter account number to select: ")
        account = self.bank.search_account(account_number)

        if account:
            print(f"Account {account_number} selected.")
            self.selected_account = account
            self.show_account_menu()
        else:
            print(f"Account {account_number} not found. Please try again.")
            self.show_main_menu()  # Go back to the main menu

    def open_account(self):
        account_number = input("Enter account number: ")
        account_type = input("Enter account type (Savings/Checking): ").lower()

        try:
            if account_type == 'savings':
                min_balance = float(input("Enter minimum balance: "))
                account = self.bank.open_account(account_number, account_type, min_balance=min_balance)
            elif account_type == 'checking':
                overdraft_limit = float(input("Enter overdraft limit: "))
                account = self.bank.open_account(account_number, account_type, overdraft_limit=overdraft_limit)
            else:
                raise ValueError("Invalid account type")

            print(f"Account {account.get_account_number()} opened successfully.")
            self.selected_account = account  # Select the newly opened account
            self.show_account_menu()  # Show the account menu
        except ValueError:
            print("Error")

    def check_balance(self):
        print(f"Account Balance: ${self.selected_account.get_current_balance()}")

    def deposit(self):
        try:
            amount = float(input("Enter amount to deposit: "))
            self.selected_account.deposit(amount)
            print("Deposit successful.")
        except ValueError:
            print("Error")

    def withdraw(self):
        try:
            amount = float(input("Enter amount to withdraw: "))
            if self.selected_account.get_current_balance() >= amount:
                self.selected_account.withdraw(amount)
                print("Withdrawal successful.")
            else:
                print("Insufficient funds. Withdrawal canceled.")
        except ValueError:
            print("Error")


# Example usage
if __name__ == "__main__":
    bank = Bank()
    banking_program = Program(bank)
    banking_program.run()
