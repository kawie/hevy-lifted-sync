# hevy-lifted-sync

Python script that automatically syncs workouts from [Lifted Studios](https://lifted-studios.com/dashboard) into the [Hevy App](https://hevy.com).

- A Lifted workout is skipped if Hevy already has a workout on the same day. Existing Hevy workouts are never changed. This also makes it idempotent to run the sync again.
- A Lifted workout is skipped if one of its exercises has no Hevy exercise in `exercise_map.py`. (See below on how to add an exercise to the mapping file.)
- All sets are logged as normal sets with weight (kg) and reps adjusted for dumbbell and single leg exercises.
- Each workout gets the Lifted start time and lasts 45 minutes.
- The title is `Lifted <location>: <class name> (Coach <coach first name>)`.

## Requirements

- Python 3.12 or newer. There are no other dependencies. With [uv](https://docs.astral.sh/uv/), just `uv run sync.py`.
- Hevy Pro (the API is only available for Pro accounts).

## Setup

```sh
cp .env.example .env
```

[Get your API key](https://hevy.com/settings?developer) and put it in `.env`.

## Get your Lifted data

Lifted has no public API (yet?). Export your workouts by hand:

1. Log in at https://lifted-studios.com/dashboard.
2. Open dev tools and go to the Network tab.
3. Find the request to the `/exercise_logs` endpoint.
4. Save its response as `exercise_logs.json` in the root of this repository.

## Run

By default the script does a dry run. It shows what it would create and doesn't write to Hevy:

```sh
source .env
uv run sync.py exercise_logs.json
```

Options:

| Option | Meaning |
|---|---|
| `--no-dry-run` | Create the workouts in Hevy |
| `--limit N` | Create at most N workouts (oldest first) |
| `--private` | Create the workouts as private (default: public) |

The Hevy API can't delete workouts. Create one workout first and check it in the app:

```sh
uv run sync.py exercise_logs.json --no-dry-run --limit 1
```

Then sync the rest:

```sh
uv run sync.py exercise_logs.json --no-dry-run
```

## Managing `exercise_map.py`

Lifted logs the weight of one dumbbell and the reps of one leg. For Hevy, weight is doubled for exercises in `TWO_DUMBBELL_EXERCISES`, reps are doubled for exercises in `PER_LEG_EXERCISES`.

When Lifted adds a new exercise, the dry run reports `no Hevy exercise mapped for: <name>`. Find the matching Hevy exercise template ID:

```sh
source .env
curl -s -H "api-key: $HEVY_API_KEY" "https://api.hevyapp.com/v1/exercise_templates?page=1&pageSize=100"
```

There are several pages; increase `page` until you find the exercise. Custom exercises you created in Hevy are included. Then add a row to `exercise_map.py`.
