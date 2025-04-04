import streamlit as st
import pandas as pd
from utils import convert_currency, format_currency
from exchange_rates import EXCHANGE_RATES, TRANSACTION_FEES, HISTORICAL_VARIATIONS

st.title("Currency Converter Pro (Web Version)")

# Sidebar menu for selecting functionality
menu = st.sidebar.radio("Select Functionality", [
    "Simple Currency Conversion",
    "Multi-Currency Conversion",
    "Margin Calculator",
    "Best Exchange Rate Finder",
    "Historical Conversion",
    "Volume Discount Calculator",
    "Currency Portfolio Analysis",
    "Exchange Rate Comparison"
])

if menu == "Simple Currency Conversion":
    st.header("Simple Currency Conversion")
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
    from_currency = st.selectbox("From Currency", sorted(EXCHANGE_RATES.keys()))
    to_currency = st.selectbox("To Currency", sorted(EXCHANGE_RATES.keys()))
    if st.button("Convert"):
        result = convert_currency(amount, from_currency, to_currency)
        st.success(f"{format_currency(amount, from_currency)} = {format_currency(result, to_currency)}")

elif menu == "Multi-Currency Conversion":
    st.header("Multi-Currency Conversion")
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
    from_currency = st.selectbox("Source Currency", sorted(EXCHANGE_RATES.keys()))
    if st.button("Convert to All Currencies"):
        results = {}
        for currency in sorted(EXCHANGE_RATES.keys()):
            if currency != from_currency:
                conv = convert_currency(amount, from_currency, currency)
                results[currency] = format_currency(conv, currency)
        st.write(f"Conversion Results for {format_currency(amount, from_currency)}:")
        st.table(pd.DataFrame(list(results.items()), columns=["Currency", "Converted Amount"]))

elif menu == "Margin Calculator":
    st.header("Margin Calculator")
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
    from_currency = st.selectbox("From Currency", sorted(EXCHANGE_RATES.keys()))
    to_currency = st.selectbox("To Currency", sorted(EXCHANGE_RATES.keys()))
    buy_margin = st.number_input("Enter buy margin percentage (0-5)", min_value=0.0, max_value=5.0, step=0.1)
    sell_margin = st.number_input("Enter sell margin percentage (0-5)", min_value=0.0, max_value=5.0, step=0.1)
    if st.button("Calculate Margin"):
        base_rate = convert_currency(1, from_currency, to_currency)
        buy_rate = base_rate * (1 + buy_margin / 100)
        sell_rate = base_rate * (1 - sell_margin / 100)
        buy_amount = amount * buy_rate
        sell_amount = amount * sell_rate

        st.subheader("Exchange Rate Details")
        st.write(f"Base Rate: 1 {from_currency} = {format_currency(base_rate, to_currency)}")
        st.write(f"Buy Rate: 1 {from_currency} = {format_currency(buy_rate, to_currency)}")
        st.write(f"Sell Rate: 1 {from_currency} = {format_currency(sell_rate, to_currency)}")

        st.subheader("Transaction Details")
        st.write(f"Amount to buy {format_currency(amount, from_currency)}: {format_currency(buy_amount, to_currency)}")
        st.write(
            f"Amount to sell {format_currency(amount, from_currency)}: {format_currency(sell_amount, to_currency)}")

elif menu == "Best Exchange Rate Finder":
    st.header("Best Exchange Rate Finder")
    base_currency = st.selectbox("Select Base Currency", sorted(EXCHANGE_RATES.keys()))
    if st.button("Find Best Rates"):
        rates = [(curr, convert_currency(1, base_currency, curr))
                 for curr in EXCHANGE_RATES if curr != base_currency]
        rates.sort(key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(rates, columns=["Currency", "Rate"])
        df["Formatted Rate"] = df["Rate"].apply(lambda r: format_currency(r, base_currency))
        st.table(df[["Currency", "Rate"]])
        st.write("Exchange Rates:")
        for currency, rate in rates:
            st.write(f"1 {base_currency} = {format_currency(rate, currency)}")

elif menu == "Historical Conversion":
    st.header("Historical Conversion")
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
    from_currency = st.selectbox("From Currency", sorted(EXCHANGE_RATES.keys()))
    to_currency = st.selectbox("To Currency", sorted(EXCHANGE_RATES.keys()))
    if st.button("Get Historical Conversions"):
        labels = ["Past", "Present", "Future"]
        base_conversion = convert_currency(amount, from_currency, to_currency)
        results = {}
        for i, variation in enumerate(HISTORICAL_VARIATIONS):
            adjusted = base_conversion * variation
            results[labels[i]] = format_currency(adjusted, to_currency)
        st.write(f"Historical Conversion Results for {format_currency(amount, from_currency)}:")
        st.table(pd.DataFrame(list(results.items()), columns=["Period", "Converted Amount"]))

elif menu == "Volume Discount Calculator":
    st.header("Volume Discount Calculator")
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
    from_currency = st.selectbox("From Currency", sorted(EXCHANGE_RATES.keys()))
    to_currency = st.selectbox("To Currency", sorted(EXCHANGE_RATES.keys()))
    if st.button("Calculate Volume Discount"):
        base_conversion = convert_currency(amount, from_currency, to_currency)
        # Volume-based discount tiers
        volume_discounts = {
            1000: 0.1,  # 0.1% discount for amounts over 1000
            5000: 0.25,  # 0.25% discount for amounts over 5000
            10000: 0.5,  # 0.5% discount for amounts over 10000
            50000: 1.0  # 1.0% discount for amounts over 50000
        }
        discount_rate = 0
        for threshold, rate in sorted(volume_discounts.items()):
            if amount >= threshold:
                discount_rate = rate

        fee_details = []
        total_fees = 0
        for fee_name, fee_percent in TRANSACTION_FEES.items():
            adjusted_fee = fee_percent - discount_rate
            if adjusted_fee < 0:
                adjusted_fee = 0
            fee_amount = base_conversion * (adjusted_fee / 100)
            total_fees += fee_amount
            fee_details.append((fee_name, f"{adjusted_fee:.2f}%", format_currency(fee_amount, to_currency)))

        st.subheader("Fee Breakdown")
        df_fees = pd.DataFrame(fee_details, columns=["Fee Name", "Adjusted Fee", "Fee Amount"])
        st.table(df_fees)
        st.write(f"Volume Discount Applied: {discount_rate}%")
        st.subheader("Summary")
        st.write(f"Total Fees: {format_currency(total_fees, to_currency)}")
        st.write(f"Final Amount: {format_currency(base_conversion - total_fees, to_currency)}")

elif menu == "Currency Portfolio Analysis":
    st.header("Currency Portfolio Analysis")
    st.write(
        "Enter your portfolio below. "
        "Use one line per entry in the format: **CURRENCY,AMOUNT**. For example:\n\n"
        "```\nUSD,1000\nEUR,500\nJPY,2000\n```"
    )
    portfolio_input = st.text_area("Portfolio Input", height=150)
    if st.button("Analyze Portfolio"):
        portfolio = {}
        for line in portfolio_input.splitlines():
            if line.strip():
                try:
                    currency, amt_str = line.split(",")
                    currency = currency.strip().upper()
                    amt = float(amt_str.strip())
                    if currency in EXCHANGE_RATES:
                        portfolio[currency] = portfolio.get(currency, 0) + amt
                    else:
                        st.warning(f"Currency {currency} is not supported.")
                except ValueError:
                    st.warning(f"Invalid line: {line}")
        if portfolio:
            total_usd = 0
            analysis = []
            for currency, amt in portfolio.items():
                usd_value = convert_currency(amt, currency, 'USD')
                total_usd += usd_value
                analysis.append((currency, format_currency(amt, currency), format_currency(usd_value, 'USD')))
            st.subheader("Portfolio Analysis")
            st.table(pd.DataFrame(analysis, columns=["Currency", "Amount", "USD Value"]))
            st.write(f"**Total Portfolio Value in USD:** {format_currency(total_usd, 'USD')}")
            st.subheader("Percentage Breakdown")
            breakdown = []
            for currency, amt in portfolio.items():
                usd_value = convert_currency(amt, currency, 'USD')
                percentage = (usd_value / total_usd) * 100 if total_usd != 0 else 0
                breakdown.append((currency, f"{percentage:.2f}%"))
            st.table(pd.DataFrame(breakdown, columns=["Currency", "Percentage"]))

elif menu == "Exchange Rate Comparison":
    st.header("Exchange Rate Comparison")
    currencies = sorted(EXCHANGE_RATES.keys())
    matrix = []
    for from_cur in currencies:
        row = []
        for to_cur in currencies:
            rate = convert_currency(1, from_cur, to_cur)
            row.append(rate)
        matrix.append(row)
    df_matrix = pd.DataFrame(matrix, index=currencies, columns=currencies)
    st.dataframe(df_matrix.style.format("{:.2f}"))
