def should_trigger_healing(
    total_records,
    invalid_records,
    schema_warnings,
    price_anomalies
):
    """
    Decide whether the scraper appears broken enough
    to request Bright Data self-healing.
    """
    # No data at all is a strong scraper failure signal
    if total_records == 0:
        return True, "No records were collected."

    # Calculate invalid-record percentage
    invalid_percentage = (
        invalid_records / total_records
    ) * 100

    # Too many invalid records suggests the scraper
    # may no longer be extracting the required fields.
    if invalid_percentage >= 20:
        return True, (
            f"{invalid_percentage:.1f}% of records are invalid."
        )

    # A large number of schema failures can indicate
    # that the website structure changed.
    if schema_warnings >= 5:
        return True, (
            f"{schema_warnings} schema warnings detected."
        )

    # Price anomalies alone should NOT trigger healing.
    # A genuinely expensive industrial product can be valid.
    #
    # Therefore price_anomalies is intentionally not used
    # as an automatic healing trigger here.

    return False, "Scraper appears healthy."