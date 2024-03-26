class OrderProcessorRepository:
    def createProduct(self, product):
        pass

    def createCustomer(self, customer):
        pass

    def deleteProduct(self, productId):
        pass

    def deleteCustomer(self, customerId):
        pass

    def addToCart(self, customer, product, quantity):
        pass

    def removeFromCart(self, customer, product):
        pass

    def getAllFromCart(self, customer):
        pass

    def placeOrder(self, customer, products_quantity_map, shippingAddress):
        pass

    def getOrdersByCustomer(self, customerId):
        pass