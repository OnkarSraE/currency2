
import time
from exchange_rates import EXCHANGE_RATES, CURRENCY_SYMBOLS

def get_valid_amount() -> float:
    #To get a valid amount from user input
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount < 0:
                print("Please enter a positive amount.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number.")

def get_valid_currency(prompt: str) -> str:
    #To get a valid currency code from user input
    while True:
        currency = input(prompt).upper()
        if currency in EXCHANGE_RATES:
            return currency
        print(f"\nInvalid currency. Available currencies: {', '.join(sorted(EXCHANGE_RATES.keys()))}")
        print("Please try again.\n")

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    #To convert amount from one currency to another
    usd_amount = amount / EXCHANGE_RATES[from_currency]           # Convert to USD first (base currency)
    return usd_amount * EXCHANGE_RATES[to_currency]               # Convert from USD to target currency

def format_currency(amount: float, currency: str) -> str:
    # To format amount with currency symbol
    symbol = CURRENCY_SYMBOLS.get(currency, '')
    return f"{symbol}{amount:.2f} {currency}"

def simulate_processing(message: str = "Processing", duration: int = 3) -> None:
    #To simulate processing time with a loading animation
    print(f"\n{message}", end="")
    for _ in range(duration):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()