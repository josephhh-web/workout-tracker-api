#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Deleting old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")
    ex1 = Exercise(name="Pushups", category="Strength", equipment_needed=False)
    ex2 = Exercise(name="Squats", category="Strength", equipment_needed=False)
    ex3 = Exercise(name="Running", category="Cardio", equipment_needed=True)

    db.session.add_all([ex1, ex2, ex3])
    db.session.commit()

    print("Creating workouts...")
    w1 = Workout(date="2026-06-01", duration_minutes=45, notes="Leg day and cardio")
    w2 = Workout(date="2026-06-03", duration_minutes=30, notes="Quick upper body")

    db.session.add_all([w1, w2])
    db.session.commit()

    print("Linking workouts and exercises...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex2.id, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id=w2.id, exercise_id=ex1.id, reps=10, sets=4)

    db.session.add_all([we1, we2])
    db.session.commit()

    print("Done seeding!")