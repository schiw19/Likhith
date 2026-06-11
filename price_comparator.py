from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class ProductOffer:
    site: str
    product_name: str
    price: float
    url: str


SAMPLE_OFFERS: List[ProductOffer] = [
    ProductOffer("Amazon", "iPhone 15 (128GB)", 68999.0, "https://amazon.example/iphone-15"),
    ProductOffer("Flipkart", "Apple iPhone 15 128 GB", 67999.0, "https://flipkart.example/iphone-15"),
    ProductOffer("eBay", "Apple iPhone 15 - 128GB", 69500.0, "https://ebay.example/iphone-15"),
    ProductOffer("Walmart", "Apple iPhone 15 128GB", 68450.0, "https://walmart.example/iphone-15"),
]


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())


def compare_prices(
    product_query: str, offers: Iterable[ProductOffer]
) -> Tuple[List[ProductOffer], Optional[ProductOffer]]:
    normalized_query = _normalize(product_query)
    matching_offers = [
        offer for offer in offers if normalized_query in _normalize(offer.product_name)
    ]
    matching_offers.sort(key=lambda offer: (offer.price, offer.site.casefold()))
    if not matching_offers:
        return [], None
    return matching_offers, matching_offers[0]


def format_results(
    product_query: str, offers: Iterable[ProductOffer]
) -> str:
    matching_offers, lowest = compare_prices(product_query, offers)
    if not matching_offers:
        return f"No offers found for '{product_query}'."

    lines = [f"Found {len(matching_offers)} offers for '{product_query}':"]
    for offer in matching_offers:
        lines.append(f"- {offer.site}: ₹{offer.price:.2f} ({offer.url})")
    lines.append(
        f"\nLowest price: {lowest.site} at ₹{lowest.price:.2f} ({lowest.url})"
    )
    return "\n".join(lines)


if __name__ == "__main__":
    query = input("Enter product to compare: ").strip()
    print(format_results(query, SAMPLE_OFFERS))
