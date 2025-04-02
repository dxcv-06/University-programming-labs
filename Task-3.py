def calculate_revenue(sales_list):
    """
    Function calculates the total revenue for each product
    """
    revenue_by_product = {}
    
    for sale in sales_list:
        product = sale["product"]
        revenue = sale["quantity"] * sale["price"]
        
        if product in revenue_by_product:
            revenue_by_product[product] += revenue
        else:
            revenue_by_product[product] = revenue
    
    return revenue_by_product

def get_high_revenue_products(revenue_dict, threshold=1000):
    """
    Function returns a list of products with revenue greater than the threshold
    """
    return [product for product, revenue in revenue_dict.items() if revenue > threshold]

def calculate_product_metrics(sales_list, product_name):
    """
    Function calculates detailed metrics for a specific product
    """
    product_sales = [sale for sale in sales_list if sale["product"] == product_name]
    
    if not product_sales:
        return None
    
    total_quantity = sum(sale["quantity"] for sale in product_sales)
    total_revenue = sum(sale["quantity"] * sale["price"] for sale in product_sales)
    avg_price = total_revenue / total_quantity if total_quantity > 0 else 0
    sale_count = len(product_sales)
    
    return {
        "total_quantity": total_quantity,
        "total_revenue": total_revenue,
        "average_price": avg_price,
        "sale_count": sale_count
    }

def display_product_details(sales, product):
    """
    Displays detailed information about a product's sales
    """
    metrics = calculate_product_metrics(sales, product)
    
    if not metrics:
        print(f"\nNo sales data found for '{product}'.")
        return
    
    print("\n" + "=" * 40)
    print(f"Sales Report for: {product}")
    print("=" * 40)
    print(f"Total Units Sold: {metrics['total_quantity']}")
    print(f"Total Revenue: ${metrics['total_revenue']:.2f}")
    print(f"Average Price: ${metrics['average_price']:.2f}")
    print(f"Number of Sales: {metrics['sale_count']}")
    print("=" * 40)
    
    print("\nIndividual Sales:")
    print("-" * 40)
    print(f"{'Quantity':<10} | {'Price':<10} | {'Revenue':<10}")
    print("-" * 40)
    
    for sale in [s for s in sales if s["product"] == product]:
        revenue = sale["quantity"] * sale["price"]
        print(f"{sale['quantity']:<10} | ${sale['price']:<9.2f} | ${revenue:<9.2f}")
    print("-" * 40)

def display_sales_summary(sales):
    """
    Displays a summary of all sales
    """
    revenue_by_product = calculate_revenue(sales)
    total_revenue = sum(revenue_by_product.values())
    
    print("\n" + "=" * 40)
    print("Sales Summary")
    print("=" * 40)
    print(f"Total Products: {len(revenue_by_product)}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print("=" * 40)
    
    print("\nRevenue by Product:")
    print("-" * 40)
    print(f"{'Product':<15} | {'Revenue':<15} | {'% of Total':<15}")
    print("-" * 40)
    
    # Sort products by revenue (highest first)
    sorted_products = sorted(revenue_by_product.items(), key=lambda x: x[1], reverse=True)
    
    for product, revenue in sorted_products:
        percentage = (revenue / total_revenue) * 100 if total_revenue > 0 else 0
        print(f"{product:<15} | ${revenue:<14.2f} | {percentage:<14.2f}%")
    
    print("-" * 40)
    
    # Show high revenue products
    high_revenue = get_high_revenue_products(revenue_by_product)
    if high_revenue:
        print("\nHigh Revenue Products (>$1000):")
        for product in high_revenue:
            print(f"- {product}: ${revenue_by_product[product]:.2f}")
    else:
        print("\nNo products with revenue greater than $1000.")

def interactive_sales_analysis():
    """
    Interactive UI for sales data analysis
    """
    # Create test sales data
    sales = [
        {"product": "apples", "quantity": 50, "price": 15},
        {"product": "bananas", "quantity": 30, "price": 25},
        {"product": "milk", "quantity": 20, "price": 30},
        {"product": "bread", "quantity": 100, "price": 10},
        {"product": "cheese", "quantity": 10, "price": 150},
        {"product": "apples", "quantity": 20, "price": 15}
    ]
    
    # Calculate revenue once for all products
    revenue_by_product = calculate_revenue(sales)
    
    # Get unique product names for menu
    products = list(set(sale["product"] for sale in sales))
    
    while True:
        print("\nSales Analysis System")
        print("1. View Overall Sales Summary")
        print("2. View Product Details")
        print("3. Add New Sale")
        print("4. View High Revenue Products (>$1000)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            # Display overall sales summary
            display_sales_summary(sales)
            
        elif choice == "2":
            # Show product list
            print("\nAvailable Products:")
            for idx, product in enumerate(products, 1):
                print(f"{idx}. {product} (Revenue: ${revenue_by_product[product]:.2f})")
            
            # Get product selection
            try:
                product_idx = int(input("\nEnter product number (or 0 to go back): "))
                if product_idx == 0:
                    continue
                
                if 1 <= product_idx <= len(products):
                    product = products[product_idx - 1]
                    display_product_details(sales, product)
                else:
                    print("Invalid product number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "3":
            # Add new sale
            print("\nAdd New Sale")
            
            # Get product (either existing or new)
            print("\nExisting products:", ", ".join(products))
            product = input("Enter product name: ")
            
            # Get quantity and price with validation
            try:
                quantity = int(input("Enter quantity sold: "))
                if quantity <= 0:
                    print("Quantity must be positive.")
                    continue
                    
                price = float(input("Enter unit price: $"))
                if price <= 0:
                    print("Price must be positive.")
                    continue
                
                # Add the new sale
                sales.append({"product": product, "quantity": quantity, "price": price})
                
                # Update revenue calculation and product list
                revenue_by_product = calculate_revenue(sales)
                products = list(set(sale["product"] for sale in sales))
                
                print(f"\nAdded sale: {quantity} {product}(s) at ${price:.2f} each")
                
            except ValueError:
                print("Please enter valid numbers for quantity and price.")
                
        elif choice == "4":
            # Display high revenue products
            high_revenue = get_high_revenue_products(revenue_by_product)
            
            if high_revenue:
                print("\nHigh Revenue Products (>$1000):")
                print("-" * 40)
                print(f"{'Product':<15} | {'Revenue':<15}")
                print("-" * 40)
                for product in high_revenue:
                    print(f"{product:<15} | ${revenue_by_product[product]:<14.2f}")
                print("-" * 40)
            else:
                print("\nNo products with revenue greater than $1000.")
                
        elif choice == "5":
            print("Exiting Sales Analysis System. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    # Run the interactive sales analysis system
    interactive_sales_analysis()
