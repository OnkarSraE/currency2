from typing import Dict
from utils import get_valid_amount, get_valid_currency, convert_currency, format_currency, simulate_processing
from exchange_rates import EXCHANGE_RATES, TRANSACTION_FEES, HISTORICAL_VARIATIONS, CURRENCY_SYMBOLS


def simple_conversion() -> None:
    #To perform a simple currency conversion
    amount = get_valid_amount()
    print(f"\nAvailable currencies: {', '.join(sorted(EXCHANGE_RATES.keys()))}")
    from_currency = get_valid_currency("Enter source currency: ")
    to_currency = get_valid_currency("Enter target currency: ")

    simulate_processing("Converting")
    result = convert_currency(amount, from_currency, to_currency)
    print(f"\nResult: {format_currency(amount, from_currency)} = {format_currency(result, to_currency)}")


def multi_currency_conversion() -> None:
   # To convert one currency to multiple currencies
    amount = get_valid_amount()
    print(f"\nAvailable currencies: {', '.join(sorted(EXCHANGE_RATES.keys()))}")
    from_currency = get_valid_currency("Enter source currency: ")

    simulate_processing("Calculating multiple conversions")
    print("\nConversion Results:")
    print("=" * 40)
    for currency in sorted(EXCHANGE_RATES.keys()):
        if currency != from_currency:
            result = convert_currency(amount, from_currency, currency)
            print(f"{format_currency(amount, from_currency)} = {format_currency(result, currency)}")


def margin_calculator() -> None:
    #Calculate exchange with buy/sell margins
    amount = get_valid_amount()
    print(f"\nAvailable currencies: {', '.join(sorted(EXCHANGE_RATES.keys()))}")
    from_currency = get_valid_currency("Enter source currency: ")
    to_currency = get_valid_currency("Enter target currency: ")

    buy_margin = float(input("Enter buy margin percentage (0-5): "))
    while buy_margin < 0 or buy_margin > 5:
        print("Margin must be between 0 and 5%")
        buy_margin = float(input("Enter buy margin percentage (0-5): "))

    sell_margin = float(input("Enter sell margin percentage (0-5): "))
    while sell_margin < 0 or sell_margin > 5:
        print("Margin must be between 0 and 5%")
        sell_margin = float(input("Enter sell margin percentage (0-5): "))

    simulate_processing("Calculating exchange with margins")
    base_rate = convert_currency(1, from_currency, to_currency)
    buy_rate = base_rate * (1 + buy_margin / 100)
    sell_rate = base_rate * (1 - sell_margin / 100)

    print("\nExchange Rate Details:")
    print("=" * 40)
    print(f"Base Rate: 1 {from_currency} = {format_currency(base_rate, to_currency)}")
    print(f"Buy Rate: 1 {from_currency} = {format_currency(buy_rate, to_currency)}")
    print(f"Sell Rate: 1 {from_currency} = {format_currency(sell_rate, to_currency)}")

    print("\nTransaction Details:")
    print("=" * 40)
    buy_amount = amount * buy_rate
    sell_amount = amount * sell_rate
    print(f"Amount to buy {amount} {from_currency}: {format_currency(buy_amount, to_currency)}")
    print(f"Amount to sell {amount} {from_currency}: {format_currency(sell_amount, to_currency)}")


def find_best_rate() -> None:
   # To find the best exchange rate for a given currency
    print(f"\nAvailable currencies: {', '.join(sorted(EXCHANGE_RATES.keys()))}")
    base_currency = get_valid_currency("Enter base currency: ")

    simulate_processing("Finding best rates")
    print(f"\nBest exchange rates for {base_currency}:")
    print("=" * 40)

    rates = [(curr, convert_currency(1, base_currency, curr))
             for curr in EXCHANGE_RATES if curr != base_currency]
    rates.sort(key=lambda x: x[1], reverse=True)

    for currency, rate in rates:
        print(f"1 {base_currency} = {format_currency(rate, currency)}")


def historical_conversion() -> None:
    # To simulate historical conversion with time travel
    amount = get_valid_amount()
    print(f"\nAvailable currencies: {', '.join(sorted(EXCHANGE_RATES.keys()))}")
    from_currency = get_valid_currency("Enter source currency: ")
    to_currency = get_valid_currency("Enter target currency: ")

    simulate_processing("Time traveling to fetch historical rates", 5)
    print("\nHistorical Conversion Results:")
    print("=" * 40)

    for i, var in enumerate(HISTORICAL_VARIATIONS):
        result = convert_currency(amount, from_currency, to_currency) * var
        period = 'Past' if i == 0 else 'Present' if i == 1 else 'Future'
        print(f"{period}: {format_currency(amount, from_currency)} = {format_currency(result, to_currency)}")


def volume_discount_calculator() -> None:
    #To calculate exchange fees with volume-based discounts
    amount = get_valid_amount()
    print(f"\nAvailable currencies: {', '.join(sorted(EXCHANGE_RATES.keys()))}")
    from_currency = get_valid_currency("Enter source currency: ")
    to_currency = get_valid_currency("Enter target currency: ")

    simulate_processing("Calculating volume discounts")
    base_conversion = convert_currency(amount, from_currency, to_currency)

    # Volume-based discount tiers
    volume_discounts = {
        1000: 0.1,  # 0.1% discount for amounts over 1000
        5000: 0.25,  # 0.25% discount for amounts over 5000
        10000: 0.5,  # 0.5% discount for amounts over 10000
        50000: 1.0  # 1.0% discount for amounts over 50000
    }

    # Calculate applicable discount
    discount_rate = 0
    for threshold, rate in sorted(volume_discounts.items()):
        if amount >= threshold:
            discount_rate = rate

    print("\nFee Breakdown:")
    print("=" * 40)
    print(f"Base conversion: {format_currency(base_conversion, to_currency)}")

    total_fees = 0
    for fee_name, fee_percent in TRANSACTION_FEES.items():
        adjusted_fee = fee_percent - discount_rate
        if adjusted_fee < 0:
            adjusted_fee = 0
        fee_amount = base_conversion * (adjusted_fee / 100)
        total_fees += fee_amount
        print(f"{fee_name} ({adjusted_fee:.2f}%): {format_currency(fee_amount, to_currency)}")

    if discount_rate > 0:
        print(f"\nVolume Discount Applied: {discount_rate}%")

    print("\nSummary:")
    print("=" * 40)
    print(f"Total Fees: {format_currency(total_fees, to_currency)}")
    print(f"Final Amount: {format_currency(base_conversion - total_fees, to_currency)}")


def portfolio_analysis() -> None:
    #To analyze a currency portfolio
    portfolio: Dict[str, float] = {}
    print(f"\nAvailable currencies: {', '.join(sorted(EXCHANGE_RATES.keys()))}")

    num_currencies = int(input("How many currencies in your portfolio? "))
    for _ in range(num_currencies):
        currency = get_valid_currency("Enter currency: ")
        amount = get_valid_amount()
        portfolio[currency] = amount

    simulate_processing("Analyzing portfolio")
    print("\nPortfolio Analysis:")
    print("=" * 40)

    total_usd = 0
    for currency, amount in portfolio.items():
        usd_value = convert_currency(amount, currency, 'USD')
        total_usd += usd_value
        print(f"{format_currency(amount, currency)} = {format_currency(usd_value, 'USD')}")

    print(f"\nTotal Portfolio Value: {format_currency(total_usd, 'USD')}")
    print("\nPercentage Breakdown:")
    print("=" * 40)
    for currency, amount in portfolio.items():
        usd_value = convert_currency(amount, currency, 'USD')
        percentage = (usd_value / total_usd) * 100
        print(f"{currency}: {percentage:.2f}%")


def compare_rates() -> None:
    # To compare exchange rates between multiple currencies
    currencies = sorted(EXCHANGE_RATES.keys())

    simulate_processing("Generating comparison matrix")
    print("\nExchange Rate Comparison Matrix:")
    print("=" * 80)

    # Print header
    print("\n     ", end="")
    for curr in currencies:
        print(f"{curr:>10}", end="")
    print("\n" + "-" * 80)

    # Print rates
    for curr1 in currencies:
        print(f"{curr1:5}", end="")
        for curr2 in currencies:
            rate = convert_currency(1, curr1, curr2)
            print(f"{rate:10.2f}", end="")
        print()