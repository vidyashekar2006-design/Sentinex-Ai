from datetime import datetime, timezone


def normalize_record(record, source):
    """
    Convert one scraper record into our common Supply WebShield schema.
    """

    # -----------------------------
    # SOURCE
    # -----------------------------
    source_name = str(source).strip()

    # -----------------------------
    # PRICE
    # -----------------------------
    raw_price = record.get("price")

    price = None
    currency = None

    if isinstance(raw_price, dict):
        price = raw_price.get("value")
        currency = raw_price.get("currency")

    elif isinstance(raw_price, (int, float)):
        price = raw_price

    elif isinstance(raw_price, str):
        # Keep raw string for now.
        # We will improve price parsing later.
        price = raw_price

    # -----------------------------
    # RATING
    # -----------------------------
    rating = record.get("rating")

    # -----------------------------
    # REVIEW
    # -----------------------------
    review = record.get("review")

    # -----------------------------
    # AVAILABILITY
    # -----------------------------
    availability = record.get("availability")

    if isinstance(availability, str):
        text = availability.lower().strip()

        if "in stock" in text:
            availability = "in_stock"

        elif "out of stock" in text:
            availability = "out_of_stock"

        elif "add to cart" in text:
            availability = "available_for_purchase"

    # -----------------------------
    # FINAL COMMON RECORD
    # -----------------------------
    normalized = {
        "source": source_name,
        "title": record.get("title"),
        "company": record.get("company"),
        "supplier": record.get("supplier"),
        "product": record.get("product"),
        "event": record.get("event"),
        "location": record.get("location"),
        "price": price,
        "currency": currency,
        "availability": availability,
        "rating": rating,
        "review": review,
        "date": record.get("date"),
        "url": record.get("url"),

        # Added by OUR pipeline, not the website
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return normalized