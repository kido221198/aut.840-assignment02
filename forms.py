from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, SubmitField, RadioField
from wtforms.validators import DataRequired


class HistoryForm(FlaskForm):
    date = DateTimeLocalField("Start: ", "End: ")
    submit = SubmitField("Add Order")


class RobotHistoryForm(FlaskForm):
    robot_options = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10']
    robot = RadioField("Robot: ", choices=robot_options, validators=[DataRequired()])
    submit = SubmitField("Add Order")
