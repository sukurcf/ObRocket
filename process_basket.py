from typing import List, Dict, Tuple
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS, cross_origin

FILE_NAME = 'products_list.txt'
APPLE_DISCOUNTED_PRICE = 4.5


class Product:
    """Class to hold info related to product"""

    def __init__(self, code: str, name: str, price: float):
        self.type = 'product'
        self.code = code
        self.name = name
        self.price = price

    def __str__(self):
        return f'Product: {self.code}, {self.price}'


class Coupon:
    """Class to hold discount info"""

    def __init__(self, code: str, price: float):
        self.type = 'coupon'
        self.code = code
        self.price = price

    def __str__(self):
        return f'Coupon: {self.code}, {self.price}'


class Basket:
    """
    Class to hold list of products in a basket.
    """

    def __init__(self, list_of_products: List):
        self.products = list_of_products

    def calculate_total(self) -> int:
        return sum(i.price for i in self.products)

    def get_coupons_applied(self):
        return [i.code for i in self.products if i.type == 'coupon']


def get_products_info(filename: str) -> Dict[str, Tuple[str, float]]:
    """
    :param filename: file containing list of product - code, name, prices
    :return: dictionary containing product code as keys, (name, price) tuple as values
    """
    with open(filename) as f:
        lines = f.readlines()[1:]
    products = {}
    for line in lines:
        code, name, price = line.split(',')
        products[code] = (name, float(price))
    return products


def process(list_of_products):
    products: Dict[str, Tuple[str, float]] = get_products_info(FILE_NAME)
    coffee_count: int = 0
    apples_count: int = 0
    chai_count: int = 0
    milk_count: int = 0
    oatmeal_count: int = 0
    try:
        print("Products: ", list_of_products)
        basket = Basket([Product(i, products[i][0], products[i][1]) for i in list_of_products])
    except KeyError as ke:
        message = f'{ke} is not present in list of products.'
        print(message)
        return {"error": message, "total": 0}, 500
    for i, product in enumerate(basket.products):
        if product.type == 'product':
            if product.code == 'CF1':
                coffee_count += 1
                if coffee_count % 2 == 0:
                    basket.products.insert(i + 1, Coupon('BOGO', -products['CF1'][1]))
            elif product.code == 'AP1':
                apples_count += 1
                if apples_count == 3:
                    apple_indexes = [idx for idx, item in enumerate(basket.products[:i]) if
                                     type(item) == Product and item.code == 'AP1']
                    for count, idx in enumerate(apple_indexes, start=1):
                        basket.products.insert(idx + count, Coupon('APPL', -1.5))
                elif apples_count > 3:
                    basket.products.insert(i + 1, Coupon('APPL', -1.5))
            elif product.code in ('CH1', 'MK1'):
                if product.code == 'CH1':
                    chai_count += 1
                elif product.code == 'MK1':
                    milk_count += 1
                if chai_count == 1 and milk_count == 1:
                    for idx, item in enumerate(basket.products[:i + 1]):
                        if type(item) == Product and item.code == 'MK1':
                            basket.products.insert(idx + 1, Coupon('CHMK', -products['MK1'][1]))
            elif product.code == 'OM1':
                oatmeal_count += 1
    total = float("{:.2f}".format(basket.calculate_total()))
    print("Total price expected: $", total)
    basket_products = [i.__dict__ for i in basket.products]
    for i in basket_products:
        if i['type'] == 'product':
            i['product'] = i['code']
        else:
            i['coupon'] = i['code']
    return {"total": total, "basket_products": basket_products}, 200


if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)


    @app.route('/process_basket', methods=['POST', 'OPTIONS', 'GET'])
    @cross_origin()
    def process_basket() -> (int, List[str]):
        """
        :return: total value and list of items in basket including coupons applied
        """
        list_of_items = request.json.get('list_of_items')
        response, status = process(list_of_items)
        return jsonify({"total": response['total'], "basket_products": response['basket_products']}), status


    app.run(host='0.0.0.0')
