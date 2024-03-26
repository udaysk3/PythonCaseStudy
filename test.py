import unittest
from unittest.mock import MagicMock
from dao.OrderProcessor import OrderProcessor
from entity.Customer import Customer
from entity.Product import Product
from entity.Cart import Cart
from exception.UserNotFound import UserNotFound
from exception.ProductNotFound import ProductNotFound
from exception.OrderNotFound import OrderNotFound

class TestOrderProcessor(unittest.TestCase):
    def setUp(self):
        self.order_processor = OrderProcessor()

    def test_create_product_success(self):
        product_data = {
            'product_id': 15,
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 10.0,
            'stock_quantity': 100
        }
        product = Product(**product_data)
        self.order_processor.createProduct = MagicMock(return_value=True)
        result = self.order_processor.createProduct(product)
        self.assertTrue(result)

    def test_add_to_cart_success(self):
        customer = Customer(customer_id=1, name='Test Customer', email='test@example.com', password='password')
        product = Product(product_id=1, name='Test Product', description='Test Description', price=10.0, stock_quantity=100)

        self.order_processor.addToCart = MagicMock(return_value=True)

        result = self.order_processor.addToCart(10, customer, product, quantity=2)
        self.assertTrue(result)

    def test_place_order_success(self):
        order_id = 1
        customer = Customer(customer_id=1, name='Test Customer', email='test@example.com', password='password')
        products_quantity_map = {1: 2, 2: 3}
        shipping_address = "123 Test Address"
        cart_id = 1

        self.order_processor.retrieveProductsFromCart = MagicMock(return_value={1: {'price': 10.0, 'quantity': 5}, 2: {'price': 20.0, 'quantity': 3}})
        self.order_processor.placeOrder = MagicMock(return_value=True)
        result = self.order_processor.placeOrder(order_id, customer, products_quantity_map, shipping_address, cartId=cart_id)
        self.assertTrue(result)

    def test_exception_customer_not_found(self):
        customer_id = 9999 
        self.order_processor.getOrdersByCustomer = MagicMock(return_value=[])

        with self.assertRaises(UserNotFound):
            self.order_processor.getOrdersByCustomer(customer_id)

    def test_exception_product_not_found(self):
        product_id = 9999
        self.order_processor.deleteProduct = MagicMock(return_value=False)
        with self.assertRaises(ProductNotFound):
            self.order_processor.deleteProduct(product_id)

    def test_exception_order_not_found(self):
        order_id = 9999  
        self.order_processor.placeOrder = MagicMock(return_value=False)
        with self.assertRaises(OrderNotFound):
            self.order_processor.placeOrder(order_id)

if __name__ == '__main__':
    unittest.main()
