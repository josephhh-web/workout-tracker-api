from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise, ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Schemas setup
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

@app.route('/')
def index():
    return "Workout API Home"

# Get all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)

# Get single exercise by id
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    return make_response(exercise_schema.dump(exercise), 200)

# Create an exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        new_data = exercise_schema.load(data)
        new_exercise = Exercise(**new_data)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(new_exercise), 201)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)
    except ValueError as e:
        return make_response({"error": str(e)}, 400)

# Delete an exercise
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    
    db.session.delete(exercise)
    db.session.commit()
    return make_response('', 204)

# Get all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)

# Get single workout
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    return make_response(workout_schema.dump(workout), 200)

# Create a workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        new_data = workout_schema.load(data)
        new_workout = Workout(**new_data)
        db.session.add(new_workout)
        db.session.commit()
        return make_response(workout_schema.dump(new_workout), 201)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)
    except ValueError as e:
        return make_response({"error": str(e)}, 400)

# Delete a workout
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    
    db.session.delete(workout)
    db.session.commit()
    return make_response('', 204)

# Add exercise to workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return make_response({"error": "Workout or Exercise not found"}, 404)

    data = request.get_json() or {}
    try:
        payload = {
            "workout_id": workout_id,
            "exercise_id": exercise_id,
            "reps": data.get("reps"),
            "sets": data.get("sets"),
            "duration_seconds": data.get("duration_seconds")
        }
        validated = workout_exercise_schema.load(payload)
        we = WorkoutExercise(**validated)
        db.session.add(we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(we), 201)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)
    except ValueError as e:
        return make_response({"error": str(e)}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)