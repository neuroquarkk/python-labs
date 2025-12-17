from datetime import datetime
import os
import csv

DB_FILE = "expenses.csv"


def init_csv():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "amount", "description", "category"])


def add_purchase(amount, description, category):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(DB_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, amount, description, category])


def get_all_purchase():
    purchases = []

    if not os.path.exists(DB_FILE):
        return purchases

    with open(DB_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['amount'] = float(row['amount'])
                purchases.append(row)
            except ValueError:
                continue

    return purchases


def update_purchase(index, new_amount, new_description, new_category):
    rows = []

    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    if 0 <= index < len(rows):
        rows[index]['amount'] = new_amount
        rows[index]['description'] = new_description
        rows[index]['category'] = new_category

        with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['timestamp', 'amount', 'description', 'category']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            return True

    return False
