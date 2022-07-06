from datetime import datetime


class Transaction:
    def __init__(self, date, person_from, person_to, narrative, amount):
        self.date = date
        self.person_from = person_from
        self.person_to = person_to
        self.narrative = narrative
        self.amount = amount

    def display(self):
        print("From: " + self.person_from + " | To: " + self.person_to + " | Narrative: " + self.narrative
              + " | Amount: " + str(round(self.amount, 2)))


def read_transactions(file) -> list:
    transactions = []
    file.readline()  # Skip the iterator by one to ignore the heading line
    for line in file:
        data = line.split(",")
        transactions.append(Transaction(
            datetime.strptime(data[0], "%d/%m/%Y"),
            data[1],
            data[2],
            data[3],
            float(data[4])
        ))
    return transactions


def run():
    with open('data/Transactions2014.csv') as file:
        transactions = read_transactions(file)

    while True:
        command = input("Enter command (List All / List [Account]): ")

        if not command.startswith("List "):
            print("Please enter a valid command")
            continue

        command = command[5:]  # Remove the pre-pending "List "

        if command == "All":
            print_all(transactions)
        else:
            print_user(command, transactions)


def print_all(transactions):
    overall_spending = get_all_balances(transactions)
    for key, value in overall_spending.items():
        print(key + ": " + str(round(value, 2)))


def print_user(person, transactions):
    has_printed = False
    for transaction in transactions:
        if transaction.person_from == person or transaction.person_to == person:
            transaction.display()
            has_printed = True

    if not has_printed:
        print("No transactions found for " + person + ".")


def get_all_balances(transactions) -> dict:
    spending = {}
    for transaction in transactions:
        if transaction.person_from in spending:
            spending[transaction.person_from] = spending[transaction.person_from] - transaction.amount
        else:
            spending[transaction.person_from] = -transaction.amount

        if transaction.person_to in spending:
            spending[transaction.person_to] = spending[transaction.person_to] + transaction.amount
        else:
            spending[transaction.person_to] = transaction.amount

    return spending


if __name__ == "__main__":
    run()
