import unittest
from process_basket import process


class TestProcessBasket(unittest.TestCase):
    def setUp(self) -> None:
        self.baskets_totals = [
            (["CH1", "AP1", "AP1", "AP1", "MK1"], 16.61, 200),
            (["CH1", "AP1", "CF1", "MK1"], 20.34, 200),
            (["MK1", "AP1"], 10.75, 200),
            (["CF1", "CF1"], 11.23, 200),
            (["AP1", "AP1", "CH1", "AP1"], 16.61, 200),
            (["AA1", "AP1", "CH1", "AK1"], 0, 500),
            (["AP1", "AP1", "AP1", "AP1", "AP1", "AP1"], 27, 200),
            (["AP1", "CH1", "AP1"], 15.11, 200),
            (["CH1", "CH1", "CF1", "CF1", "CF1", "MK1", "AP1", "AP1", "AP1", "OM1"], 45.87, 200),
            (["CH1", "CF1", "CF1", "MK1", "AP1", "OM1", "AP1", "AP1"], 31.53, 200)
        ]

    def test_baskets_totals(self) -> None:
        for basket, expected_total, expected_status_code in self.baskets_totals:
            response, status_code = process(basket)
            self.assertEqual(expected_total, response["total"])
            self.assertEqual(expected_status_code, status_code)
            print("-" * 50)

    def tearDown(self) -> None:
        self.baskets_totals = None


if __name__ == "__main__":
    unittest.main()
