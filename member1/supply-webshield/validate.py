from urllib.parse import urlparse


KNOWN_SOURCES = {
    "deodap",
    "tradeindia",
    "meesho"
}


def validate_record(record):
    """
    Validate one normalized supply-chain record.

    Returns:
        valid: True/False
        issues: list of detected problems
    """

    issues = []

    # -----------------------------------------
    # 1. SOURCE
    # -----------------------------------------

    source = str(record.get("source","")).strip().lower()

    if not source:
        issues.append("Missing source")

    elif source not in KNOWN_SOURCES:
        issues.append(f"Unknown source: {record.get('source')}")

    # -----------------------------------------
    # 2. TITLE
    # -----------------------------------------

    title = record.get("title")

    if not title or not isinstance(title, str):
        issues.append("Missing or invalid title")

    # -----------------------------------------
    # 3. PRODUCT
    # -----------------------------------------

    product = record.get("product")

    if not product or not isinstance(product, str):
        issues.append("Missing or invalid product")

    # -----------------------------------------
    # 4. URL
    # -----------------------------------------

    url = record.get("url")

    if not url:
        issues.append("Missing URL")

    elif not isinstance(url, str):
        issues.append("Invalid URL type")

    else:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            issues.append("Invalid URL")

        if not parsed.netloc:
            issues.append("Invalid URL domain")

     # -----------------------------------------
# 5. PRICE
# -----------------------------------------

    price = record.get("price")

# Price is OPTIONAL.
# Missing price is allowed because some
# B2B products do not publish a price.

    if price is None:
        pass

    elif isinstance(price, (int, float)):

        if price < 0:
           issues.append(
            f"Negative price: {price}"
        )

    elif isinstance(price, str):

        if not price.strip():
        # Empty price is treated as missing
          pass

    else:

     issues.append(
        f"Invalid price type: "
        f"{type(price).__name__}"
    )


    # -----------------------------------------
    # 6. RATING
    # -----------------------------------------  

    rating = record.get("rating")

    if rating is not None:

        if not isinstance(rating, (int, float)):
            issues.append("Rating is not numeric")

        elif rating < 0 or rating > 5:
            issues.append(
                f"Rating outside 0-5 range: {rating}"
            )

    # -----------------------------------------
    # 7. AVAILABILITY
    # -----------------------------------------

    availability = record.get("availability")

    if availability is not None:

        if not isinstance(availability, str):
            issues.append(
                "Availability is not text"
            )

    # -----------------------------------------
    # 8. TIMESTAMP
    # -----------------------------------------

    if not record.get("timestamp"):
        issues.append("Missing timestamp")

    # -----------------------------------------
    # RESULT
    # -----------------------------------------

    valid = len(issues) == 0

    return valid, issues