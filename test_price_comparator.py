import unittest

from price_comparator import ProductOffer, compare_prices, format_results


class TestPriceComparator(unittest.TestCase):
    def setUp(self) -> None:
        self.offers = [
            ProductOffer("SiteA", "Test Product 1", 100.0, "https://a.example/item"),
            ProductOffer("SiteB", "Test Product 1", 90.0, "https://b.example/item"),
            ProductOffer("SiteC", "Another Product", 80.0, "https://c.example/item"),
            ProductOffer("SiteD", "  test   product 1 ", 90.0, "https://d.example/item"),
        ]

    def test_compare_prices_returns_sorted_matches_and_lowest(self) -> None:
        matches, lowest = compare_prices("test product 1", self.offers)
        self.assertEqual([o.site for o in matches], ["SiteB", "SiteD", "SiteA"])
        self.assertEqual(lowest.site, "SiteB")
        self.assertEqual(lowest.price, 90.0)

    def test_compare_prices_returns_none_when_no_match(self) -> None:
        matches, lowest = compare_prices("missing product", self.offers)
        self.assertEqual(matches, [])
        self.assertIsNone(lowest)

    def test_format_results_contains_lowest_price_line(self) -> None:
        output = format_results("test product 1", self.offers)
        expected_output = "\n".join(
            [
                "Found 3 offers for 'test product 1':",
                "- SiteB: ₹90.00 (https://b.example/item)",
                "- SiteD: ₹90.00 (https://d.example/item)",
                "- SiteA: ₹100.00 (https://a.example/item)",
                "",
                "Lowest price: SiteB at ₹90.00 (https://b.example/item)",
            ]
        )
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
