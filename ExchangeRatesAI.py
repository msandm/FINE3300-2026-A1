
import csv
from pathlib import Path


class ExchangeRates:
    def __init__(self, exchange_rate_file):
        # Locate the exchange rate file in the same folder as this program
        self.file_path = Path(exchange_rate_file)

        if not self.file_path.is_absolute():
            self.file_path = Path(__file__).resolve().parent / self.file_path

        self.exchange_rate, self.rate_date = self.read_exchange_rate()

    def read_exchange_rate(self):
        # Read the latest USD/CAD exchange rate from the CSV file
        with open(self.file_path, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None or "FXAUSDCAD" not in reader.fieldnames:
                raise ValueError("The CSV file does not contain FXAUSDCAD.")

            latest_rate = None
            latest_date = None

            for row in reader:
                rate = row.get("FXAUSDCAD", "").strip()

                if rate:
                    latest_rate = float(rate)
                    latest_date = row.get("Date", "").strip()

        if latest_rate is None or latest_rate <= 0:
            raise ValueError("No valid USD/CAD exchange rate was found.")

        return latest_rate, latest_date

    def convert(self, amount, from_currency, to_currency):
        # Standardize currency inputs
        from_currency = from_currency.strip().upper()
        to_currency = to_currency.strip().upper()

        # Validate the currencies
        if from_currency not in ("USD", "CAD"):
            raise ValueError("The 'from' currency must be USD or CAD.")

        if to_currency not in ("USD", "CAD"):
            raise ValueError("The 'to' currency must be USD or CAD.")

        if amount < 0:
            raise ValueError("The amount cannot be negative.")

        # Convert between the two currencies
        if from_currency == to_currency:
            return amount

        elif from_currency == "USD" and to_currency == "CAD":
            return amount * self.exchange_rate

        elif from_currency == "CAD" and to_currency == "USD":
            return amount / self.exchange_rate


def main():
    try:
        # Create an ExchangeRates object using the CSV file
        rates = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")

        # Prompt the user for the required information
        amount = float(input("Enter the amount to convert: "))
        from_currency = input("Enter the 'from' currency (USD or CAD): ").strip().upper()
        to_currency = input("Enter the 'to' currency (USD or CAD): ").strip().upper()

        # Convert the amount
        converted_amount = rates.convert(amount, from_currency, to_currency)

        # Display the result
        print(f"\nExchange rate date: {rates.rate_date}")
        print(
            f"{from_currency} ${amount:,.2f} = "
            f"{to_currency} ${converted_amount:,.2f}"
        )

    except (ValueError, FileNotFoundError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()