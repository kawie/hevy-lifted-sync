import argparse
import json
import os
import urllib.error
import urllib.request
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from exercise_map import EXERCISE_MAP

HEVY_API = "https://api.hevyapp.com/v1"
LOCAL_TZ = ZoneInfo("Europe/Berlin")
CLASS_DURATION = timedelta(minutes=45)


def main():
    parser = argparse.ArgumentParser(description="Sync Lifted Studios workouts into Hevy.")
    parser.add_argument("file", help="Lifted export, e.g. exercise_logs.json")
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="show what would be created, write nothing (default); --no-dry-run writes to Hevy",
    )
    parser.add_argument("--limit", type=int, help="create at most this many workouts (oldest first)")
    parser.add_argument("--private", action="store_true", help="create the workouts as private")
    args = parser.parse_args()

    with open(args.file) as file:
        lifted_workouts = json.load(file)

    sync(os.environ["HEVY_API_KEY"], lifted_workouts, args.dry_run, args.limit, args.private)


def sync(api_key, lifted_workouts, dry_run, limit, is_private):
    hevy_days = fetch_hevy_workout_days(api_key)
    created = 0

    for lifted in sorted(lifted_workouts, key=lambda workout: workout["start_datetime"]):
        if limit is not None and created >= limit:
            break

        start = datetime.fromisoformat(lifted["start_datetime"])
        day = local_day(start)
        if day in hevy_days:
            print(f"{day}  skipped: Hevy already has a workout on this day")
            continue

        unmapped = sorted({log["exercise_name"] for log in lifted["exercise_logs"]} - EXERCISE_MAP.keys())
        if unmapped:
            print(f"{day}  skipped: no Hevy exercise mapped for: {', '.join(unmapped)}")
            continue

        workout = to_hevy_workout(lifted, start, is_private)
        if not dry_run:
            hevy_request(api_key, "POST", "/workouts", {"workout": workout})
        hevy_days.add(day)
        created += 1
        status = "would create" if dry_run else "created"
        print(f"{day}  {status}: {workout['title']}  {workout['start_time']} - {workout['end_time']}")


def to_hevy_workout(lifted, start, is_private):
    exercises = {}
    for log in sorted(lifted["exercise_logs"], key=lambda log: (log["exercise_number"], log["set_number"])):
        exercise = exercises.setdefault(
            log["exercise_number"],
            {"exercise_template_id": EXERCISE_MAP[log["exercise_name"]], "sets": []},
        )
        exercise["sets"].append({"type": "normal", "weight_kg": log["weight"], "reps": log["reps"]})

    return {
        "title": f"Lifted: {lifted['timer_name']} (with {lifted['coach_first_name']})",
        "start_time": format_time(start),
        "end_time": format_time(start + CLASS_DURATION),
        "is_private": is_private,
        "exercises": list(exercises.values()),
    }


def fetch_hevy_workout_days(api_key):
    days = set()
    page = 1
    page_count = 1
    while page <= page_count:
        data = hevy_request(api_key, "GET", f"/workouts?page={page}&pageSize=10")
        page_count = data["page_count"]
        days.update(local_day(datetime.fromisoformat(workout["start_time"])) for workout in data["workouts"])
        page += 1
    return days


def local_day(time):
    return time.astimezone(LOCAL_TZ).date().isoformat()


def format_time(time):
    return time.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def hevy_request(api_key, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        f"{HEVY_API}{path}",
        data=data,
        method=method,
        headers={"api-key": api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Hevy {method} {path} failed: {error.code} {error.read().decode()}") from error


if __name__ == "__main__":
    main()
