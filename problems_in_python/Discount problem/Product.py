class Product:
    DISCOUNT_RATE = 10
    productID = 0

    def __init__(self, name, price):
        Product.productID += 1
        self.product_name = name
        self.product_price = price

    @property
    def get_name(self):
        return self.product_name

    @get_name.setter
    def set_name(self, product_name):
        self.product_name = product_name

    @property
    def get_price(self):
        return self.product_price

    @get_price.setter
    def set_price(self, product_price):
        self.product_price = product_price

    def computeDiscount(self):
        discountValue = self.DISCOUNT_RATE / 100
        return discountValue

    def computeSellingPrice(self):
        computedDiscountPrice = self.get_price * self.computeDiscount()
        sellingPrice = self.get_price - computedDiscountPrice
        return sellingPrice

    def __str__(self):
        return f"Product ID: {self.productID}, Name: {self.product_name}, Price: {self.product_price}"
