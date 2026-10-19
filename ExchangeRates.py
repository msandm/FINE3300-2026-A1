class ExchangeRates:
    def __init__(self, boc_exchangerate="BankOfCanadaExchangeRate.2026.csv"):
        self.__boc_exchangerate = boc_exchangerate
        self.__usd_cad = 0.0
        self.__read_file()
#loads the Bank of Canada exchange rate file and loads the latest USD/CAD exchange rate as well from it.


    def __read_file(self):
        file = open(self.__boc_exchangerate, "r")
        text = file.read()
        file.close()
#Opens the Bank of Canada exchange rate file and reads whole file into one string. Then it pulls out the latest USD/CAD exchange rate.

#Goes through the text one character at a time to split it into rows and columns so the USD/CAD rate can be found:
#a comma starts a new column, a new line starts a new row
        rows = []
        row = []
        cell = ""
        for char in text:
            if char == ",":
                row.append(cell)
                cell = ""
            elif char == "\n":
                row.append(cell)
                rows.append(row)
                row = []
                cell = ""
            else:
                cell += char


        if cell != "" or len(row) > 0:
            row.append(cell)
            rows.append(row)
# Save the last row too, since the file doesn't end with a new line and the loop above would otherwise leave it out


        header = rows[0]
        column = 0
        count = 0
        for name in header:
            if name == "FXAUSDCAD":
                column = count
                break
            count += 1
# This is to find which column holds the USD/CAD rate

        latest = rows[-1]
        self.__usd_cad = float(latest[column])
# The last row of data has the latest exchange rate for USD/CAD, so we will take that row.


# This converts the amount from one currency to the other using the rate from the file
    def convert(self, amount, from_currency, to_currency):
        currencies = ["USD", "CAD"]
        valid = (amount >= 0 and
                 from_currency in currencies and
                 to_currency in currencies)
        result = 0.0
# Check that the amount isn't negative and both currencies are USD or CAD.

        if valid:
            # If the user selects US dollars to Canadian dollars. We will then multiply by the exchange rate
            if from_currency == "USD" and to_currency == "CAD":
                result = amount * self.__usd_cad
            # If the user selects Canadian dollars to US dollars. We will then divide by the exchange rate
            elif from_currency == "CAD" and to_currency == "USD":
                result = amount / self.__usd_cad
            else:
                result = amount

        return (valid, result)
# This is to confirm and send back whether the inputs were valid and the converted amount

# This is now the part that runs when the user starts the program:

if __name__ == "__main__":
    # This code creates the calculator, which loads the latest exchange rate from the file
    rates = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")
    # These are the currency answers the user is allowed to type
    currencies = ["USD", "CAD", "cad", "usd"]

    # First question is how much money to convert. If the number is negative, ask again
    amount = float(input("Enter the amount to convert: "))
    while amount < 0:
        print("The amount cannot be negative.")
        amount = float(input("Enter the amount to convert: "))

    #The second part is to ask the user which currency they want to convert from. If the user types something other than USD, usd, CAD, or cad, ask again.
    from_currency = input("Convert from (USD or CAD): ")
    while from_currency not in currencies:
        print("Please enter USD or CAD.")
        from_currency = input("Convert from (USD or CAD): ")
    if from_currency == "usd":
        from_currency = "USD"
    elif from_currency == "cad":
        from_currency = "CAD"

    #The third part is to ask the user which currency they want to convert to. If the user types something other than USD, usd, CAD, or cad, ask again.
    to_currency = input("Convert to (USD or CAD): ")
    while to_currency not in currencies:
        print("Please enter USD or CAD.")
        to_currency = input("Convert to (USD or CAD): ")
    if to_currency == "usd":
        to_currency = "USD"
    elif to_currency == "cad":
        to_currency = "CAD"

    # This code will then do the conversion and show the final result with the currency, dollar signs, rounded to the penny. If the inputs were invalid, it will show an invalid message.
    valid, result = rates.convert(amount, from_currency, to_currency)
    if valid:
        print("${:.2f} {} = ${:.2f} {}".format(amount, from_currency, result, to_currency))
    else:
        print("Conversion inputs are invalid!!")