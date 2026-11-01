"""
USN: 25BTRAD102
LAB EXERCISE 14: BANK ACCOUNT SYSTEM USING OOP

QUESTION:
Develop a Python program using classes and objects to manage bank accounts.
Implement deposit, withdrawal, balance enquiry, and transaction validation.

CRITICAL THINKING (CT):
Design appropriate classes and methods, apply encapsulation, analyze
transaction conditions, and test invalid transactions and insufficient
balances.

REAL WORLD EXPOSURE (RWE):
Simulate routine banking transactions and explain how object-oriented
programming supports account management and data protection.
"""


class BankAccount:
    def __init__(self, account_holder, opening_balance=0.0):
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative.")
        self.account_holder = account_holder
        self.__balance = float(opening_balance)
        self.__transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return False
        self.__balance += amount
        self.__transactions.append(("Deposit", amount))
        print(f"Deposit successful. Amount: {amount:.2f}")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return False
        if amount > self.__balance:
            print("Transaction declined: insufficient balance.")
            return False
        self.__balance -= amount
        self.__transactions.append(("Withdrawal", amount))
        print(f"Withdrawal successful. Amount: {amount:.2f}")
        return True

    def check_balance(self):
        print(f"Available balance: {self.__balance:.2f}")
        return self.__balance

    def show_transactions(self):
        if not self.__transactions:
            print("No completed transactions.")
            return
        print("\nTRANSACTION HISTORY")
        for transaction_type, amount in self.__transactions:
            print(f"{transaction_type}: {amount:.2f}")


def main():
    name = input("Enter account holder name: ").strip()
    if not name:
        print("Account holder name cannot be empty.")
        return

    try:
        opening_balance = float(input("Enter opening balance: "))
        account = BankAccount(name, opening_balance)
    except ValueError as error:
        print(f"Invalid account details: {error}")
        return

    while True:
        print("\n--- BANK ACCOUNT SYSTEM ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Balance enquiry")
        print("4. Transaction history")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice in ("1", "2"):
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            if choice == "1":
                account.deposit(amount)
            else:
                account.withdraw(amount)
        elif choice == "3":
            account.check_balance()
        elif choice == "4":
            account.show_transactions()
        elif choice == "5":
            print("Thank you for using the bank account system.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
