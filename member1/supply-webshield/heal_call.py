from self_heal_controller import run_self_healing


def call_self_healing(reason):
    print("=" * 60)
    print("SELF-HEALING CALL")
    print("=" * 60)

    print(f"Reason: {reason}")
    print("\nStarting Bright Data self-healing workflow...")

    try:
        result = run_self_healing(reason)

        print("\nSelf-healing workflow completed.")

        return result

    except Exception as error:

        print(
            "\nSelf-healing workflow failed:"
        )

        print(error)

        return False


if __name__ == "__main__":

    reason = input(
        "Enter the healing reason: "
    ).strip()

    if not reason:

        print(
            "No healing reason supplied."
        )

    else:

        call_self_healing(reason)