import subprocess
import sys


def call_self_healing(reason):
    print("=" * 60)
    print("SELF-HEALING CALL")
    print("=" * 60)

    print(f"Reason: {reason}")
    print("\nStarting self-healing controller...")

    result = subprocess.run(
        [sys.executable, "self_heal_controller.py"],
        check=False
    )

    if result.returncode == 0:
        print("\nSelf-healing controller completed successfully.")
    else:
        print(
            f"\nSelf-healing controller exited "
            f"with code: {result.returncode}"
        )


if __name__ == "__main__":

    reason = input(
        "Enter the healing reason: "
    ).strip()

    if not reason:
        print("No healing reason supplied.")
        sys.exit(1)

    call_self_healing(reason)