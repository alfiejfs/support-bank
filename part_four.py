import json, os, logging, datetime
import xml.etree.ElementTree as et


class Transaction:
    def __init__(self, date, person_from, person_to, narrative, amount):
        self.date = date
        self.person_from = person_from
        self.person_to = person_to
        self.narrative = narrative
        self.amount = amount

    def display(self):
        print("Date: " + self.date.strftime("%m/%d/%Y") + " | From: " + self.person_from + " | To: "
              + self.person_to + " | Narrative: " + self.narrative + " | Amount: " + str(round(self.amount, 2)))


def read_transactions_csv(file) -> list:
    transactions = []
    file.readline()  # Skip the iterator by one to ignore the heading line
    line_number = 2
    for line in file:
        data = line.split(",")
        try:
            formatted_date = datetime.datetime.strptime(data[0], "%d/%m/%Y")
        except ValueError:
            logging.warning(("Line", line_number, "has an invalid date. :("))
            continue

        try:
            amount = float(data[4])
        except ValueError:
            logging.warning(("Line", line_number, "has an amount that is not a number. :("))
            continue

        transactions.append(Transaction(
            formatted_date,
            data[1],
            data[2],
            data[3],
            amount
        ))

        line_number += 1

    return transactions


def read_transactions_json(file) -> list:
    transactions = []
    data = json.loads(file.read())
    for transaction in data:
        transactions.append(Transaction(
            datetime.datetime.fromisoformat(transaction['Date']),
            transaction['FromAccount'],
            transaction['ToAccount'],
            transaction['Narrative'],
            float(transaction['Amount'])
        ))
    return transactions


def read_transactions_xml(file) -> list:
    transactions = []

    tree = et.parse(os.path.abspath(file.name))
    for child in tree.getroot():
        date = child.attrib['Date']
        narrative = child[0].text
        amount = float(child[1].text)
        from_person = child[2][0].text
        to_person = child[2][1].text

        transactions.append(Transaction(
            excel_date_to_datetime(date),
            from_person,
            to_person,
            narrative,
            amount
        ))

    return transactions

def load_transactions(file_name):
    if not os.path.exists("data/" + file_name):
        print("File " + file_name + "could not be found.")
    else:
        with open("data/" + file_name, 'r') as file:
            if file_name.endswith(".csv"):
                transactions = read_transactions_csv(file)
                print("File imported")
            elif file_name.endswith(".json"):
                transactions = read_transactions_json(file)
                print("File imported")
            elif file_name.endswith(".xml"):
                transactions = read_transactions_xml(file)
                print("File imported")
            else:
                transactions = None
                print("File extension not supported")

    return transactions

def run():
    logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

    transactions = None
    while True:
        command = input("Enter command (List All / List [Account] / Import File [File] / Export File [File]): ")

        if command.startswith("Import File "):
            file_name = command[12:]
            load_transactions(file_name)

        elif command.startswith("Export "):
            file_name = command[12:]
            transactions = load_transactions(file_name)
            new_file_name = input("What will the file be called? ")
            format = input("What is the file format? ")
            convert_to_csv(transactions, new_file_name, format)

        elif command.startswith("List "):
            specifier = command[5:]  # Remove the pre-pending "List "
            if specifier == "All":
                print_all(transactions)
            else:
                print_user(specifier, transactions)

        else:
            print("Please enter a valid command")

def convert_to_csv(transactions, file, file_name):
    with open("data/" + file_name, 'w+') as new_file:
        new_file.writelines("Date,From,To,Narrative,Amount")
        for t in



def convert_to_json(file, file_name):
    pass

def convert_to_xml(file, file_name):
    pass

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


def excel_date_to_datetime(excel_date):
    temp = datetime.datetime(1900, 1, 1)
    delta = datetime.timedelta(days=int(excel_date))
    return temp + delta


if __name__ == "__main__":
    run()
