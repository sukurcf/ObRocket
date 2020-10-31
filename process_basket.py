from typing import List, Dict, Tuple, TypedDict
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS, cross_origin

FILE_NAME = 'products_list.txt'
APPLE_DISCOUNTED_PRICE = 4.5


class Product:
    """Class to hold product related info"""

    def __init__(self, code: str, name: str, price: float) -> None:
        self.type = 'product'
        self.code = code
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f'Product: {self.code}, {self.price}'


class Coupon:
    """Class to hold coupon and discount info"""

    def __init__(self, code: str, price: float) -> None:
        self.type = 'coupon'
        self.code = code
        self.price = price

    def __str__(self) -> str:
        return f'Coupon: {self.code}, {self.price}'


class BasketItems(TypedDict):
    total: int
    basket_products: List


class Basket:
    """
    Class to hold list of items and coupons applied in a basket.
    """

    def __init__(self, list_of_products: List) -> None:
        self.products = list_of_products

    def calculate_total(self) -> int:
        return sum(i.price for i in self.products)

    def get_coupons_applied(self) -> List[str]:
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


def process(list_of_products: List[str]) -> Tuple[Dict, int]:
    """
    :param list_of_products: list of item codes that need to be part of basket
    :return dictionary containing list of items and coupon codes applied on those items,
    and the total price and status code.
    """

    # Initialising variables
    products: Dict[str, Tuple[str, float]] = get_products_info(FILE_NAME)
    coffee_count: int = 0
    apples_count: int = 0
    chai_count: int = 0
    milk_count: int = 0
    oatmeal_count: int = 0
    CHMK_applied: bool = False

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
                    # Applying BOGO coupon.
                    basket.products.insert(i + 1, Coupon('BOGO', -products['CF1'][1]))

            elif product.code == 'AP1':
                apples_count += 1
                if apples_count == 3:
                    apple_indexes = [idx for idx, item in enumerate(basket.products[:i]) if
                                     type(item) == Product and item.code == 'AP1']
                    for count, idx in enumerate(apple_indexes, start=1):
                        # Applying APPL coupon on already added apples.
                        basket.products.insert(idx + count, Coupon('APPL', -1.5))
                elif apples_count > 3:
                    # Applying APPL coupon.
                    basket.products.insert(i + 1, Coupon('APPL', -1.5))

            elif product.code in ('CH1', 'MK1'):
                if product.code == 'CH1':
                    chai_count += 1
                elif product.code == 'MK1':
                    milk_count += 1
                if chai_count >= 1 and milk_count >= 1 and not CHMK_applied:
                    for idx, item in enumerate(basket.products[:i + 1]):
                        if type(item) == Product and item.code == 'MK1':
                            # Applying CHMK coupon.
                            basket.products.insert(idx + 1, Coupon('CHMK', -products['MK1'][1]))
                            break
                    CHMK_applied = True

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
    def process_basket() -> (BasketItems, int):
        """
        :return: total value and list of items in basket including coupons applied
        """
        list_of_items = request.json.get('list_of_items')
        response, status = process(list_of_items)
        return jsonify(
            {
                "total": response['total'],
                "basket_products": response['basket_products']
            }
        ), status

    app.run(host='0.0.0.0')
