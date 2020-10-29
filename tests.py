import unittest

from flask import jsonify

from process_basket import process_basket


class TestProcessBasket(unittest.TestCase):
    def setUp(self) -> None:
        self.baskets_totals = [
            (['CH1', 'AP1', 'AP1', 'AP1', 'MK1'], 16.61, jsonify({'total': 16.61, 'basket_products': [
                {'type': 'product', 'code': 'CH1', 'name': 'Chai', 'price': 3.11, 'product': 'CH1'},
                {'type': 'product', 'code': 'AP1', 'name': 'Apples', 'price': 6.0, 'product': 'AP1'},
                {'type': 'coupon', 'code': 'APPL', 'price': -1.5, 'coupon': 'APPL'},
                {'type': 'product', 'code': 'AP1', 'name': 'Apples', 'price': 6.0, 'product': 'AP1'},
                {'type': 'coupon', 'code': 'APPL', 'price': -1.5, 'coupon': 'APPL'},
                {'type': 'product', 'code': 'AP1', 'name': 'Apples', 'price': 6.0, 'product': 'AP1'},
                {'type': 'coupon', 'code': 'APPL', 'price': -1.5, 'coupon': 'APPL'},
                {'type': 'product', 'code': 'MK1', 'name': 'Milk', 'price': 4.75, 'product': 'MK1'},
                {'type': 'coupon', 'code': 'CHMK', 'price': -4.75, 'coupon': 'CHMK'}]}, 200)),
            (['CH1', 'AP1', 'CF1', 'MK1'], 20.34, ['CHMK']),
            (['MK1', 'AP1'], 10.75, []),
            (['CF1', 'CF1'], 11.23, ['BOGO']),
            (['AP1', 'AP1', 'CH1', 'AP1'], 16.61, ['APPL', 'APPL', 'APPL'])
        ]

    def test_baskets_totals(self) -> None:
        for basket, expected_total, expected_coupons_applied in self.baskets_totals:
            actual_total, actual_coupons_applied = process_basket(basket)
            self.assertEqual(expected_total, actual_total)
            print('-' * 50)


if __name__ == '__main__':
    unittest.main()
