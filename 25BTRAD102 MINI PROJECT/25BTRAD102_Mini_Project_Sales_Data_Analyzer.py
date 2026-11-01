"""
USN: 25BTRAD102
MINI PROJECT (UNIT 3): SALES DATA ANALYZER

PROBLEM STATEMENT:
Develop a Python-based sales data analyzer using lists and dictionaries to
manage product names, quantities sold, and prices. Calculate total sales,
identify the highest-selling product, and summarize product-wise performance.

EXPECTED FUNCTIONALITIES:
- Store product details and sales information using lists and dictionaries.
- Add or update product sales records.
- Calculate total sales and product-wise revenue.
- Identify the highest-selling product and compare product performance.
- Test the program using different sales datasets and interpret the results.
"""

products = {}


def add_or_update_product():
    name = input("Enter product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    try:
        quantity = int(input("Enter quantity sold: "))
        price = float(input("Enter unit price: "))
    except ValueError:
        print("Quantity must be a whole number and price must be numeric.")
        return

    if quantity < 0 or price < 0:
        print("Quantity and price cannot be negative.")
        return

    products[name] = {"quantity": quantity, "price": price}
    print("Product sales record saved.")


def display_sales_summary():
    if not products:
        print("No product records available.")
        return

    print("\nPRODUCT-WISE SALES")
    print(f'{"Product":<25} {"Quantity":>10} {"Unit Price":>12} {"Revenue":>12}')
    print("-" * 63)

    total_revenue = 0.0
    highest_quantity_product = None

    for name, details in products.items():
        quantity = details["quantity"]
        price = details["price"]
        revenue = quantity * price
        total_revenue += revenue

        print(f"{name:<25} {quantity:>10} {price:>12.2f} {revenue:>12.2f}")

        if (
            highest_quantity_product is None
            or quantity > products[highest_quantity_product]["quantity"]
        ):
            highest_quantity_product = name

    print("-" * 63)
    print(f"Total sales revenue: {total_revenue:.2f}")

    if highest_quantity_product is not None:
        highest_quantity = products[highest_quantity_product]["quantity"]
        print(
            f"Highest-selling product by quantity: "
            f"{highest_quantity_product} ({highest_quantity} units)"
        )


def main():
    while True:
        print("\n--- SALES DATA ANALYZER ---")
        print("1. Add or update product sales")
        print("2. Display sales summary")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_or_update_product()
        elif choice == "2":
            display_sales_summary()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 3.")


if __name__ == "__main__":
    main()
