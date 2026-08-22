EXPECTED_SCHEMA = {
    "source": (str, type(None)),
    "title": (str, type(None)),
    "company": (str, type(None)),
    "supplier": (str, type(None)),
    "product": (str, type(None)),
    "event": (str, type(None)),
    "location": (str, type(None)),
    "price": (int, float, type(None)),
    "currency": (str, type(None)),
    "availability": (str, type(None)),
    "rating": (int, float, type(None)),
    "review": (str, type(None)),
    "date": (str, type(None)),
    "url": (str, type(None)),
    "timestamp": (str, type(None))
}


def check_schema(record):

    issues = []

    # Check for missing fields
    for field in EXPECTED_SCHEMA:

        if field not in record:
            issues.append(
                f"Missing field: {field}"
            )

    # Check field types
    for field, allowed_types in EXPECTED_SCHEMA.items():

        if field not in record:
            continue

        value = record[field]

        if not isinstance(value, allowed_types):
            issues.append(
                f"Invalid type for {field}: "
                f"{type(value).__name__}"
            )

    # Detect unexpected fields
    for field in record:

        if field not in EXPECTED_SCHEMA:
            issues.append(
                f"Unexpected field: {field}"
            )

    return issues