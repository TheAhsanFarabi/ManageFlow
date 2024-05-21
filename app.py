import csv
import os
from datetime import datetime

def read_csv(file_path):
    products = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row)
    return products

def write_csv(file_path, products):
    with open(file_path, mode='w', newline='') as file:
        fieldnames = products[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def update_product(products, product_id, field, value):
    for product in products:
        if product['Product Id'] == product_id:
            product[field] = value
            product['updated_at'] = datetime.now().strftime('%Y-%m-%d')
            break

def display_products(products):
    print("\nCurrent Products List:")
    for product in products:
        print(f"ID: {product['Product Id']}, Name: {product['Product Name']}, Brand: {product['Brand']}, "
              f"Quantity: {product['Quantity']}, Updated At: {product['updated_at']}, Created At: {product['created_at']}")

def adjust_quantity(products, product_id, adjustment):
    for product in products:
        if product['Product Id'] == product_id:
            new_quantity = int(product['Quantity']) + adjustment
            if new_quantity < 0:
                print("Quantity cannot be negative.")
                return
            product['Quantity'] = new_quantity
            product['updated_at'] = datetime.now().strftime('%Y-%m-%d')
            break

def main():
    file_path = 'products.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return

    products = read_csv(file_path)
    display_products(products)
    
    while True:
        print("\nOptions:")
        print("1. Update Product Information")
        print("2. Adjust Quantity")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            product_id = input("Enter Product ID to update: ")
            field = input("Enter field to update (Product Name, Brand, Quantity): ")
            value = input(f"Enter new value for {field}: ")
            update_product(products, product_id, field, value)
            write_csv(file_path, products)
            display_products(products)

        elif choice == '2':
            product_id = input("Enter Product ID to adjust quantity: ")
            adjustment = input("Enter '+' to increase or '-' to decrease quantity: ")
            if adjustment == '+':
                adjust_quantity(products, product_id, 1)
            elif adjustment == '-':
                adjust_quantity(products, product_id, -1)
            else:
                print("Invalid adjustment input.")
            write_csv(file_path, products)
            display_products(products)

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
