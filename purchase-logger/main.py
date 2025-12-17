import sys
import storage
from datetime import datetime


def print_menu():
    print("\n--- PURCHASE LOGGER ---")
    print("1. Add Purchase")
    print("2. View Summary")
    print("3. Edit Purchase")
    print("4. Export Summary")
    print("5. Exit")


def handle_add():
    print("\nAdd New Purchase")
    try:
        amount_input = input("Amount ($): ")
        amount = float(amount_input)

        if amount < 0:
            print("Error: Amount cannot be negative")
            return

        description = input("Description: ").strip()
        if not description:
            description = "No description"

        category = input("Category: ").strip()
        if not category:
            category = "Uncategorized"

        storage.add_purchase(amount, description, category)
        print("Success: Purchase logged")
    except ValueError:
        print("Error: Please enter a valid number for the amount")


def generate_summary_text():
    purchases = storage.get_all_purchase()
    if not purchases:
        return "No purchases logged yet"

    total_spent = sum(p['amount'] for p in purchases)

    category_totals = {}
    monthly_totals = {}

    for p in purchases:
        cat = p.get('category', 'Uncategorized')
        category_totals[cat] = category_totals.get(cat, 0) + p['amount']

        try:
            month_key = (
                datetime
                .strptime(p['timestamp'], '%Y-%m-%d %H:%M:%S')
                .strftime('%Y-%m')
            )
            monthly_totals[month_key] = monthly_totals.get(
                month_key, 0) + p['amount']
        except ValueError:
            continue

    lines = []
    lines.append("--- SPENDING REPORT ---")
    lines.append(f"Generated on: {
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Total Spent: ${total_spent:,.2f}")

    lines.append("\n[By Category]")
    for cat, amount in category_totals.items():
        lines.append(f"  - {cat}: {amount:,.2f}")

    lines.append("\n[By Month]")
    for month in sorted(monthly_totals.keys(), reverse=True):
        nice_date = datetime.strptime(month, '%Y-%m').strftime('%B %Y')
        lines.append(f"  - {nice_date}: ${monthly_totals[month]:,.2f}")

    return "\n".join(lines)


def handle_summary():
    print(generate_summary_text())


def handle_edit():
    print("\nEdit Purchase")
    purchases = storage.get_all_purchase()

    if not purchases:
        print("No purchases to edit")
        return

    for i, p in enumerate(purchases):
        print(f"{i + 1}. {p['timestamp']} | ${p['amount']:,.2f} | {p['description']} | {p['category']}")

    try:
        selection = int(input("\nSelect number to edit: ")) - 1

        if selection < 0 or selection >= len(purchases):
            print("Error: Invalid selection number")
            return

        current = purchases[selection]

        print(f"Editing: {current['description']} (${current['amount']:,.2f})")
        print("(Press Enter to keep current value)")

        new_amount_str = input(
            f"New Amount [{current['amount']:,.2f}]: ").strip()

        if new_amount_str:
            new_amount = float(new_amount_str)
        else:
            new_amount = current['amount']

        new_desc = input(
            f"New Description [{current['description']}]: ").strip()
        if not new_desc:
            new_desc = current['description']

        new_cat = input(f"New Category [{current['category']}]: ").strip()
        if not new_cat:
            new_cat = current['category']

        storage.update_purchase(selection, new_amount, new_desc, new_cat)
        print("Success: Purchase updated")
    except ValueError:
        print("Error: Invalid input")


def handle_export():
    print("Exporting Report...")
    report = generate_summary_text()

    filename = f"report_{datetime.now().strftime('%Y%m%d')}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
            print(f"Success: Report saved to {filename}")
    except IOError:
        print("Error: Could not write to file")


def main():
    storage.init_csv()

    while True:
        print_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            handle_add()
        elif choice == '2':
            handle_summary()
        elif choice == '3':
            handle_edit()
        elif choice == '4':
            handle_export()
        elif choice == '5':
            sys.exit()
        else:
            print("Invalid command, please try again")


if __name__ == "__main__":
    main()
