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
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self.transactions.append(f"-${amount:.2f}")

    def __str__(self) -> str:
        return f"BankAccount(owner ={self.owner}, balance = ${self._balance:.2f})"
    
    def __repr__(self) -> str:
        return f"BankAccount(owner ={self.owner!r}, balance = ${self._balance!r})"
    

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
            raise ValueError("Savings accounts must maintain a $50 minimum")
        super().withdraw(amount)  # reuse parent logic

    def __str__(self) -> str:
        return (
            f"SavingsAccount(owner={self.owner}, "
            f"balance=${self._balance:.2f}, "
            f"interest_earned=${self.interest_earned:.2f})"
        )
    
    
acc = BankAccount.open_with_bonus("Vipul")
print(acc)          # balance starts at $100

try:
    acc.balance = -50   # raises ValueError — the setter catches it
except ValueError as e:
    print(f"Error: {e}")

print(acc.balance)  # still $100, because the setter prevented the change

sav = SavingsAccount("Vipul", 1000)
sav.apply_interest()
print(sav)              # shows balance + interest earned

try:
    sav.withdraw(981)       # raises ValueError — minimum balance rule (1030 - 981 = 49 < 50)
except ValueError as e:
    print(f"Error: {e}")

sav.withdraw(500)       # works fine (1030 - 500 = 530 > 50)
print(sav.transactions)

