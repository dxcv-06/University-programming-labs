def update_inventory(product_name, quantity, inventory_dict):
    """
    Function updates the quantity of products in the dictionary.
    Positive quantity adds products, negative - removes them
    """
    if product_name in inventory_dict:
        inventory_dict[product_name] += quantity
        # Ensure the quantity is not negative
        if inventory_dict[product_name] < 0:
            inventory_dict[product_name] = 0
    else:
        # If the product does not exist, add it (only with positive quantity)
        if quantity > 0:
            inventory_dict[product_name] = quantity
    
    return inventory_dict

def get_low_stock_products(inventory_dict, threshold=5):
    """
    Function returns a list of products with quantity less than the threshold
    """
    return [product for product, quantity in inventory_dict.items() if quantity < threshold]

def display_inventory(inventory_dict):
    """
    Displays current inventory in a formatted way
    """
    print("\nCurrent Inventory:")
    print("-" * 30)
    print(f"{'Product':<15} | {'Quantity':<10}")
    print("-" * 30)
    for product, quantity in inventory_dict.items():
        print(f"{product:<15} | {quantity:<10}")
    print("-" * 30)

def interactive_inventory_management():
    """
    Function for interactive inventory management with a menu
    """
    # Create initial inventory
    inventory = {
        "apples": 10,
        "bananas": 15,
        "milk": 5,
        "bread": 3,
        "butter": 2,
        "cheese": 7
    }
    
    while True:
        # Display menu
        print("\nInventory Management System")
        print("1. Display current inventory")
        print("2. Add product")
        print("3. Remove product")
        print("4. Show low stock products (less than 5)")
        print("5. Exit")
        
        # Get user choice
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            # Display inventory
            display_inventory(inventory)
            
        elif choice == "2":
            # Add product
            product_name = input("Enter product name: ")
            while True:
                try:
                    quantity = int(input("Enter quantity to add: "))
                    if quantity <= 0:
                        print("Please enter a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            update_inventory(product_name, quantity, inventory)
            print(f"Added {quantity} {product_name} to inventory.")
            
        elif choice == "3":
            # Remove product
            if not inventory:
                print("Inventory is empty.")
                continue
                
            # Show current products for reference
            print("\nAvailable products:")
            for idx, product in enumerate(inventory.keys(), 1):
                print(f"{idx}. {product} ({inventory[product]} in stock)")
            
            product_name = input("\nEnter product name to remove: ")
            
            if product_name not in inventory:
                print(f"Error: {product_name} not found in inventory.")
                continue
                
            while True:
                try:
                    quantity = int(input(f"Enter quantity to remove (max {inventory[product_name]}): "))
                    if quantity <= 0:
                        print("Please enter a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            update_inventory(product_name, -quantity, inventory)
            print(f"Removed {quantity} {product_name} from inventory.")
            
        elif choice == "4":
            # Show low stock products
            low_stock = get_low_stock_products(inventory)
            if low_stock:
                print("\nLow stock products (less than 5 units):")
                for product in low_stock:
                    print(f"- {product}: {inventory[product]} units")
            else:
                print("\nThere are no low stock products.")
                
        elif choice == "5":
            # Exit
            print("Exiting Inventory Management System. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    # Run the interactive inventory management system
    interactive_inventory_management()
