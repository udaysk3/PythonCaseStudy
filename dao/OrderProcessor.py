from .OrderProcessorRepository import OrderProcessorRepository
from util.DBConnUtil import DBConnection
import pyodbc
from exception.ProductNotFound import ProductNotFound
from exception.UserNotFound import UserNotFound 
from exception.OrderNotFound import OrderNotFound


class OrderProcessor(OrderProcessorRepository):
    def __init__(self):
        self.conn = DBConnection.getConnection()

    def retrieveProductsFromCart(self, customer_id, cart_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT p.product_id, p.price, c.quantity FROM cart c JOIN products p ON c.product_id = p.product_id WHERE c.customer_id = ? AND c.cart_id = ?",
                (customer_id, cart_id))
            rows = cursor.fetchall()
            products_quantity_map = {}
            for row in rows:
                product_id = row.product_id
                price = row.price
                quantity = row.quantity
                print(f"Raw quantity for product {product_id}: {quantity}")
                try:
                    quantity = int(quantity)
                except ValueError:
                    print(f"Error converting quantity to integer for product {product_id}. Quantity value: {quantity}")
                    quantity = 0
                print(f"Processed quantity for product {product_id}: {quantity}")
                products_quantity_map[product_id] = {'price': price, 'quantity': quantity}
            return products_quantity_map
        except pyodbc.Error as ex:
            print(f"Error retrieving products from cart: {ex}")
            return None

    def createProduct(self, product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO products (product_id,name, description, price, stock_quantity) VALUES (?,?, ?, ?, ?)",
                           (product.get_product_id(),product.get_name(), product.get_description(), product.get_price(), product.stock_quantity))
            self.conn.commit()
            print("Product created successfully")
            return True
        except pyodbc.Error as ex:
            print(f"Error creating product: {ex}")
            return False

    def createCustomer(self, customer):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO customers (customer_id,name, email, password) VALUES (?,?, ?, ?)",
                           (customer.get_customer_id(),customer.get_name(), customer.get_email(), customer.get_password()))
            self.conn.commit()
            print("Customer created successfully")
            return True
        except pyodbc.Error as ex:
            print(f"Error creating customer: {ex}")
            return False

    def deleteProduct(self, productId):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM products WHERE product_id = ?", (productId,))
            self.conn.commit()
            print("Product deleted successfully")
            return True
        except Exception as ex:
            print("something")
            raise ProductNotFound(f"Product with ID {productId} not found")
        # except pyodbc.Error as ex:
        #     print(f"Error deleting product: {ex}")
        #     return False

    def deleteCustomer(self, customerId):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customerId,))
            self.conn.commit()
            print("Customer deleted successfully")
            return True
        except pyodbc.Error as ex:
            print(f"Error deleting customer: {ex}")
            return False
        except Exception as ex:
            raise UserNotFound(f"Customer with ID {customerId} not found")

    def addToCart(self, cart_id, customer, product, quantity):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO cart (cart_id, customer_id, product_id, quantity) VALUES (?, ?, ?, ?)",
                           (cart_id, customer.get_customer_id(), product.get_product_id(), quantity))
            self.conn.commit()
            print("Product added to cart successfully")
            return True
        except pyodbc.Error as ex:
            print(f"Error adding product to cart: {ex}")
            return False
        except Exception as ex:
            raise OrderNotFound("Error removing product from cart: customer or product not found")

    def removeFromCart(self, customer, product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM cart WHERE customer_id = ? AND product_id = ?",
                           (customer.get_customer_id(), product.get_product_id()))
            self.conn.commit()
            print("Product removed from cart successfully")
            return True
        except pyodbc.Error as ex:
            print(f"Error removing product from cart: {ex}")
            return False
        except Exception as ex:
            raise OrderNotFound("Error removing product from cart: Order or product not found")

    def getAllFromCart(self, customer):
        try:
            cursor = self.conn.cursor()
            rows = cursor.execute("SELECT products.* FROM products JOIN cart ON products.product_id = cart.product_id WHERE cart.customer_id = ?",
                                  (customer.get_customer_id(),))
            products = []
            for row in rows:
                products.append({'product_id': row.product_id, 'name': row.name, 'description': row.description,
                                 'price': row.price, 'stock_quantity': row.stock_quantity})
            return products
        except pyodbc.Error as ex:
            print(f"Error getting products from cart: {ex}")
            return []
        
    def placeOrder(self, order_id, customer, products_quantity_map, shippingAddress, cartId):
        try:
            cursor = self.conn.cursor()
            product_prices = {}
            for product_id in products_quantity_map.keys():
                cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
                row = cursor.fetchone()
                if row:
                    product_prices[product_id] = row.price
                else:
                    raise ProductNotFound(f"Product with ID {product_id} not found")
            total_price = sum(
                products_quantity_map[product_id] * product_prices[product_id] for product_id in products_quantity_map.keys()
            )
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer.get_customer_id(),))
            if not cursor.fetchone():
                raise UserNotFound(f"Customer with ID {customer.get_customer_id()} not found")
            cursor.execute(
                "INSERT INTO orders (order_id, customer_id, order_date, total_price) VALUES (?, ?, GETDATE(), ?)",
                (order_id, customer.get_customer_id(), total_price)
            )

            order_item_id = cursor.execute("SELECT MAX(order_item_id) FROM order_items").fetchone()[0] or 0
            for product_id, quantity in products_quantity_map.items():
                order_item_id += 1
                cursor.execute("INSERT INTO order_items (order_item_id, order_id, product_id, quantity) VALUES (?, ?, ?, ?)",
                            (order_item_id, order_id, product_id, quantity))
            self.conn.commit()

            print("Order placed successfully")
            return True

        except pyodbc.Error as ex:
            print(f"Error placing order: {ex}")
            return False


    def getOrdersByCustomer(self, customerId):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT products.*, order_items.quantity FROM products JOIN order_items ON products.product_id = order_items.product_id JOIN orders ON orders.order_id = order_items.order_id WHERE orders.customer_id = ?",
                           (customerId,))
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                orders.append({'product_id': row.product_id, 'name': row.name, 'description': row.description, 'price': row.price, 'stock_quantity': row.stock_quantity, 'quantity': row.quantity})
            return orders
        except pyodbc.Error as ex:
            print(f"Error getting orders by customer: {ex}")
            return []
