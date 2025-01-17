from Product import Product
def main():
    # Create instances of the Product class
    product1 = Product(name="Laptop", price=1500.00)
    product2 = Product(name="Phone", price=800.00)


    print("Product Details:")
    print(product1)
    print(product2)


    product1.set_name = "Gaming Laptop"
    product1.set_price = 2000.00

    # Compute selling price for the updated product
    selling_price = product1.computeSellingPrice()
    print(f"\nUpdated Product 1 Details: {product1}")
    print(f"Selling Price: {selling_price:.2f}")



if __name__ == "__main__":
    main()
