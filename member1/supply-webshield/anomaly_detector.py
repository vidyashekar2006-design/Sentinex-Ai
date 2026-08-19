import statistics


def detect_price_anomalies(records, min_records=10):

    anomalies = []

    # Group prices by source
    source_prices = {}

    for record in records:

        source = record.get("source")
        price = record.get("price")

        if not source:
            continue

        if not isinstance(price, (int, float)):
            continue

        if price <= 0:
            continue

        source_prices.setdefault(source, []).append(price)

    # Analyze each source separately
    for source, prices in source_prices.items():

        # Too few records for a meaningful statistical baseline
        if len(prices) < min_records:
            continue

        median_price = statistics.median(prices)

        # Median-based detection is more resistant
        # to extreme prices than a simple mean.
        for record in records:

            if record.get("source") != source:
                continue

            price = record.get("price")

            if not isinstance(price, (int, float)):
                continue

            if price <= 0:
                continue

            # Flag values more than 10x the median
            # as suspicious, but do NOT delete them.
            if price > median_price * 10:

                anomalies.append({
                    "source": source,
                    "product": record.get("product"),
                    "price": price,
                    "median_source_price": median_price,
                    "reason": (
                        "Price is more than "
                        "10x the source median"
                    ),
                    "url": record.get("url")
                })

    return anomalies