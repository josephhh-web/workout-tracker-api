from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

# Exercise Model
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')

    # Table constraints: name must be unique
    __table_args__ = (
        UniqueConstraint('name', name='uq_exercise_name'),
    )

    # Model validations
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be blank")
        return name

    @validates('category')
    def validate_category(self, key, category):
        if not category:
            raise ValueError("Category cannot be blank")
        return category

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


# Workout Model
class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')

    # Table constraints: duration must be positive
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    # Model validations
    @validates('duration_minutes')
    def validate_duration(self, key, duration_minutes):
        if duration_minutes <= 0:
            raise ValueError("Duration must be greater than zero")
        return duration_minutes

    @validates('date')
    def validate_date(self, key, date):
        if not date:
            raise ValueError("Date cannot be blank")
        return date

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


# Join Table Model
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Table constraints for reps and sets
    __table_args__ = (
        CheckConstraint('reps >= 0', name='check_reps_positive'),
        CheckConstraint('sets >= 0', name='check_sets_positive'),
    )


# --- Marshmallow Schemas ---

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()
    
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Str(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()
    
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)