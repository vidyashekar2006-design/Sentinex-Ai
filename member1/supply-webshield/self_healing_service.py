import json
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

STATE_FILE = PROCESSED_DIR / "self_healing_status.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    """
    Load the current self-healing state.
    """

    if not STATE_FILE.exists():
        return {
            "status": "idle",
            "source": None,
            "reason": None,
            "healing_started_at": None,
            "repair_ready_at": None,
            "healed_at": None,
            "self_healed_count": 0
        }

    try:
        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {
            "status": "idle",
            "source": None,
            "reason": None,
            "healing_started_at": None,
            "repair_ready_at": None,
            "healed_at": None,
            "self_healed_count": 0
        }


def save_state(state):
    """
    Save self-healing state.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            state,
            file,
            indent=2,
            ensure_ascii=False
        )


def mark_healing_required(
    reason,
    source=None
):
    """
    Record that the pipeline detected a
    condition that requires healing.
    """

    state = load_state()

    state["status"] = "healing_required"
    state["source"] = source
    state["reason"] = reason
    state["healing_started_at"] = None
    state["repair_ready_at"] = None
    state["healed_at"] = None

    save_state(state)

    return state


def mark_repair_requested():
    """
    Record that the Bright Data healing request
    has been started.
    """

    state = load_state()

    state["status"] = "repair_requested"

    if not state.get("healing_started_at"):
        state["healing_started_at"] = utc_now()

    save_state(state)

    return state


def mark_repair_ready():
    """
    Record that Bright Data has generated a
    repair and it is ready for approval.
    """

    state = load_state()

    state["status"] = "repair_ready"
    state["repair_ready_at"] = utc_now()

    save_state(state)

    return state


def mark_healed():
    """
    Record a REAL successful recovery.

    This function should only be called after
    the repaired scraper has been executed and
    its output has passed validation.
    """

    state = load_state()

    previous_count = state.get(
        "self_healed_count",
        0
    )

    state["status"] = "healed"
    state["healed_at"] = utc_now()
    state["self_healed_count"] = (
        previous_count + 1
    )

    save_state(state)

    return state


def reset_to_idle():
    """
    Reset the state after a normal healthy run.
    """

    state = load_state()

    state["status"] = "idle"
    state["source"] = None
    state["reason"] = None
    state["healing_started_at"] = None
    state["repair_ready_at"] = None
    state["healed_at"] = None

    save_state(state)

    return state