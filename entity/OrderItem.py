class OrderItem:
    def __init__(self, order_item_id, order_id, product_id, quantity):
        self.__order_item_id = order_item_id
        self.__order_id = order_id
        self.__product_id = product_id
        self.__quantity = quantity
    
    # Getters
    def get_order_item_id(self):
        return self.__order_item_id
    
    def get_order_id(self):
        return self.__order_id
    
    def get_product_id(self):
        return self.__product_id
    
    def get_quantity(self):
        return self.__quantity
    
    # Setters
    def set_order_item_id(self, order_item_id):
        self.__order_item_id = order_item_id
    
    def set_order_id(self, order_id):
        self.__order_id = order_id
    
    def set_product_id(self, product_id):
        self.__product_id = product_id
    
    def set_quantity(self, quantity):
        self.__quantity = quantity