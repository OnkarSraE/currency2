
from currency_operations import (
    simple_conversion, multi_currency_conversion, margin_calculator,
    find_best_rate, historical_conversion, volume_discount_calculator,
    portfolio_analysis, compare_rates
)

def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Currency Converter Pro ===")
    print("=" * 28)
    print("1. Simple Currency Conversion")
    print("2. Multi-Currency Conversion")
    print("3. Margin Calculator")
    print("4. Best Exchange Rate Finder")
    print("5. Historical Conversion")
    print("6. Volume Discount Calculator")
    print("7. Currency Portfolio Analysis")
    print("8. Exchange Rate Comparison")
    print("9. Exit")
    print("=" * 28)

def main() -> None:
    """Main program loop."""
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-9): ")

        try:
            if choice == '1':
                simple_conversion()
            elif choice == '2':
                multi_currency_conversion()
            elif choice == '3':
                margin_calculator()
            elif choice == '4':
                find_best_rate()
            elif choice == '5':
                historical_conversion()
            elif choice == '6':
                volume_discount_calculator()
            elif choice == '7':
                portfolio_analysis()
            elif choice == '8':
                compare_rates()
            elif choice == '9':
                print("\nThank you for using Currency Converter Pro!")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()