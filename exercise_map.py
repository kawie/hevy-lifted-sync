# Lifted exercise name -> Hevy exercise_template_id.
# Workouts with an exercise missing here are skipped and reported, so add a row when Lifted adds a new exercise.
EXERCISE_MAP = {
    "BB Romanian Deadlift": "2B4B7310",  # Romanian Deadlift (Barbell)
    "DB Bulgarian Split Squat": "B5D3A742",  # Bulgarian Split Squat (Dumbbell)
    "DB Chest Press Flat": "3601968B",  # Bench Press (Dumbbell)
    "DB Chest Press Incline": "07B38369",  # Incline Bench Press (Dumbbell)
    "DB Lateral Raises": "422B08F1",  # Lateral Raise (Dumbbell)
    "DB Lunge Alter. On The Spot": "B537D09F",  # Lunge (Dumbbell)
    "DB Lunge Pulse": "B537D09F",  # Lunge (Dumbbell)
    "DB Reverse Lunge On The Spot": "FFDA283B",  # Reverse Lunge (Dumbbell)
    "DB Reverse Lunge Pulse": "FFDA283B",  # Reverse Lunge (Dumbbell)
    "DB Standing Palms In Shoulder Press": "6AC96645",  # Overhead Press (Dumbbell)
    "DB Standing Shoulder Press": "6AC96645",  # Overhead Press (Dumbbell)
    "Lat Pull Normal Grip": "6A6C31A5",  # Lat Pulldown (Cable)
    "Lat Pull V Bar": "4E5257DE",  # Lat Pulldown - Close Grip (Cable)
    "Leg Press Normal Stance": "C7973E0E",  # Leg Press (Machine)
    "Seated Cable Row Normal Grip": "F1D60854",  # Seated Cable Row - Bar Grip
    "Seated Cable Row V Bar": "0393F233",  # Seated Cable Row - V Grip (Cable)
}

# Lifted logs the weight of one dumbbell; Hevy gets the total of both.
TWO_DUMBBELL_EXERCISES = {
    "DB Bulgarian Split Squat",
    "DB Chest Press Flat",
    "DB Chest Press Incline",
    "DB Lateral Raises",
    "DB Lunge Alter. On The Spot",
    "DB Lunge Pulse",
    "DB Reverse Lunge On The Spot",
    "DB Reverse Lunge Pulse",
    "DB Standing Palms In Shoulder Press",
    "DB Standing Shoulder Press",
}

# Lifted logs the reps of one leg; Hevy gets the total of both.
PER_LEG_EXERCISES = {
    "DB Bulgarian Split Squat",
    "DB Lunge Alter. On The Spot",
    "DB Lunge Pulse",
    "DB Reverse Lunge On The Spot",
    "DB Reverse Lunge Pulse",
}
