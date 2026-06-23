class BankError(Exception):
    """Custom exception for bank account errors."""
    pass

class InsufficientFundsError(BankError):
    def __init__(self, amount:float, balance:float):
        self.amount= amount
        self.balance =  balance
        super().__init__(f"Cannot withdraw ${amount:.2f} from account with balance ${balance:.2f}")

class MinimumBalanceError(BankError):
    def __init__(self, minimum:float):
        self.minimum = minimum
        super().__init__(f"Account must maintain a minimum balance of ${minimum:.2f}")

class BankAccount:
    interest_rate = 0.03

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance =  balance
        self.transactions: list[str] = []

    @staticmethod
    def validate_amount(amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")

    @property
    def balance(self) -> float:
        return self._balance
    
    @balance.setter
    def balance(self, value: float) -> None:
        if value <0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    @classmethod
    def open_with_bonus(cls, owner: str) -> "BankAccount":
        return cls(owner, balance=100.0)  # Open account with a bonus of $100
    
    def deposit(self, amount: float) -> None:
        BankAccount.validate_amount(amount)  # validation before anything
        self._balance += amount
        self.transactions.append(f"+${amount:.2f}")
        
    def withdraw(self, amount: float) -> None:
        BankAccount.validate_amount(amount)  # validation before anything
        if amount > self._balance:
            raise InsufficientFundsError(amount, self._balance)
        self._balance -= amount
        self.transactions.append(f"-${amount:.2f}")

    def __str__(self) -> str:
        return f"BankAccount(owner ={self.owner}, balance = ${self._balance:.2f})"
    
    def __repr__(self) -> str:
        return f"BankAccount(owner ={self.owner!r}, balance = ${self._balance!r})"

    def __len__(self) -> int:
        return len(self.transactions)
    
    def __contains__(self, transaction: str) -> bool:
        return transaction in self.transactions
    
    def __iter__(self):
        return iter(self.transactions)
    
    def __getitem__(self, index:int) -> str:
        return self.transactions[index]

    def safe_withdraw(self, amount:float) -> bool:
        try:
            self.withdraw(amount)
            print(f"Withdrew ${amount:.2f} successfully.")
            return True
        except InsufficientFundsError as e:
            print(f"Failed to withdraw: {e}")
            return False
        except ValueError as e:
            print(f"Invalid amount: {e}")
            return False
        finally:
            print(f"Balance after attempt: ${self._balance:.2f}")

class SavingsAccount(BankAccount):
    def __init__(self, owner: str, balance: float = 0.0):
        super().__init__(owner, balance)  # call parent __init__
        self.interest_earned: float = 0.0

    def apply_interest(self) -> None:
        interest = self._balance * self.interest_rate
        self._balance += interest
        self.interest_earned += interest
        self.transactions.append(f"+${interest:.2f} (interest)")

    def withdraw(self, amount: float) -> None:
        if self._balance - amount < 50:
            raise MinimumBalanceError(50)
        super().withdraw(amount)  # reuse parent logic

    def __str__(self) -> str:
        return (
            f"SavingsAccount(owner={self.owner}, "
            f"balance=${self._balance:.2f}, "
            f"interest_earned=${self.interest_earned:.2f})"
        )
    
if __name__ == "__main__":
    # Setup
    acc = BankAccount.open_with_bonus("Vipul")
    sav = SavingsAccount("Vipul Savings", 500)

    # Deposits
    acc.deposit(300)
    sav.deposit(200)
    sav.apply_interest()

    # Iteration
    print("--- Account transactions ---")
    for t in acc:
        print(t)

    print(f"\nTotal transactions: {len(acc)}")
    print(f"Last transaction: {acc[-1]}")

    # Error handling
    acc.safe_withdraw(10000)  # should fail gracefully

    print(f"\n{acc}")
    print(f"{sav}")

