from dao.OrderProcessor import OrderProcessor
from entity.Customer import Customer
from entity.Product import Product
from exception.OrderNotFound import OrderNotFound
from exception.ProductNotFound import ProductNotFound
from exception.UserNotFound import UserNotFound


class EcomApp:
    @staticmethod
    def register_customer(order_processor, customer):
        order_processor.createCustomer(customer)

    @staticmethod
    def create_product(order_processor, product):
        order_processor.createProduct(product)

    @staticmethod
    def delete_product(order_processor, product_id):
        if not order_processor.deleteProduct(product_id):
            print("Error: Failed to delete product. Make sure it is not associated with any carts.")
        else:
            print("Product deleted successfully.")


    @staticmethod
    def add_to_cart(order_processor, cart_id, customer, product, quantity):
        order_processor.addToCart(cart_id, customer, product, quantity)

    @staticmethod
    def view_cart(order_processor, customer):
        cart_items = order_processor.getAllFromCart(customer)
        if cart_items:
            print("Cart items:")
            for item in cart_items:
                print(item)
        else:
            print("Cart is empty")

    @staticmethod
    def place_order(order_processor, order_id, customer_id, shipping_address, cart_id):
        products_quantity_map = {}
        while True:
            product_id = input("Enter product ID (or press Enter to finish): ")
            if not product_id:
                break
            quantity = int(input("Enter quantity: "))
            products_quantity_map[product_id] = quantity

        try:
            success = order_processor.placeOrder(order_id, customer_id, products_quantity_map, shipping_address, cart_id)
            if success:
                print("Order placed successfully.")
            else:
                print("Failed to place order.")
        except UserNotFound as e:
            print(f"Error: {e}")
        except ProductNotFound as e:
            print(f"Error: {e}")

    @staticmethod
    def view_customer_order(order_processor, customer_id):
        orders = order_processor.getOrdersByCustomer(customer_id)
        if orders:
            print("Customer orders:")
            for order in orders:
                print(order)
        else:
            print("No orders found for the customer")

    @staticmethod
    def main():
        order_processor = OrderProcessor()
        
        while True:
            print("\nMenu:")
            print("1. Register Customer")
            print("2. Create Product")
            print("3. Delete Product")
            print("4. Add to Cart")
            print("5. View Cart")
            print("6. Place Order")
            print("7. View Customer Order")
            print("0. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                customer_id = input("Enter customer ID: ")
                name = input("Enter customer name: ")
                email = input("Enter customer email: ")
                password = input("Enter customer password: ")
                customer = Customer(customer_id, name, email, password)
                EcomApp.register_customer(order_processor, customer)
            elif choice == "2":
                product_id = input("Enter product ID: ")
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                description = input("Enter product description: ")
                stock_quantity = int(input("Enter product stock quantity: "))
                product = Product(product_id, name, price, description, stock_quantity)
                EcomApp.create_product(order_processor, product)
            elif choice == "3":
                product_id = input("Enter product ID to delete: ")
                EcomApp.delete_product(order_processor, product_id)
            elif choice == "4":
                cart_id = input("Enter cart ID: ")
                customer_id = input("Enter customer ID: ")
                product_id = input("Enter product ID to add to cart: ")
                quantity = int(input("Enter quantity: "))
                customer = Customer(customer_id, "", "", "") 
                product = Product(product_id, "", 0, "", 0)
                EcomApp.add_to_cart(order_processor, cart_id, customer, product, quantity)
            elif choice == "5":
                # View Cart
                customer_id = input("Enter customer ID to view cart: ")
                customer = Customer(customer_id, "", "", "") 
                EcomApp.view_cart(order_processor, customer)
            elif choice == "6":
                # Place Order
                order_id = input("Enter order ID: ")
                customer_id = input("Enter customer ID: ")
                shipping_address = input("Enter shipping address: ")
                cartId = input("Enter Cart Id: ")
                products_quantity_map = {} 
                customer = Customer(customer_id, "", "", "") 
                EcomApp.place_order(order_processor, order_id, customer, products_quantity_map, shipping_address, cartId)
            elif choice == "7":
                # View Customer Order
                customer_id = input("Enter customer ID to view orders: ")
                EcomApp.view_customer_order(order_processor, customer_id)
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    EcomApp.main()
