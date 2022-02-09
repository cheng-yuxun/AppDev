from wtforms import (
    Form,
    IntegerField,
    StringField,
    TimeField,
    TextAreaField,
    DateField,
    SelectField,
    validators,
    ValidationError
)
from flask_wtf.file import FileAllowed, FileField, FileRequired
import datetime


class OnsiteEvents(Form):
    def date_check(form, field):
        if field.data < datetime.date.today():
            raise ValidationError('Invalid Date!')

    def time_check(form, field):
        if field.data > form.end_time.data:
            raise ValidationError('Invalid Time!')

    name = StringField(
        "Name", [validators.DataRequired(), validators.length(min=1, max=100)]
    )

    desc = TextAreaField("Description", [validators.DataRequired()])

    date = DateField("Date", format="%Y-%m-%d", validators=[date_check])

    start_time = TimeField("Start Time", [validators.DataRequired(), time_check])

    end_time = TimeField("End Time", [validators.DataRequired()])

    image = FileField(
        "Image",
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
            
        ],
    )

    location = SelectField(
        "Location",
        [validators.DataRequired()],
        choices=[
            ("", "Select"),
            ("Decathlon SGLab", "Decathlon SGLab"),
            ("Decathlon Bedok", "Decathlon Bedok"),
        ],
        default="",
    )

    quantity = IntegerField(
        "Quantity (Pax)",
        [
            validators.InputRequired(message="Please enter a valid integer value."),
            validators.NumberRange(min=1, max=999999999),
        ],
    )

    price = IntegerField(
        "Price ($)",
        [
            validators.InputRequired(message="Please enter a valid integer value."),
            validators.NumberRange(min=1, max=999999999),
        ],
    )


class LivestreamEvents(Form):

    def end_time_check(form, field):
        if field.data < form.start_time.data:
            raise ValidationError('End Time must not be earlier than Start Time!')

    def start_time_check(form, field):
        if field.data > form.end_time.data:
            raise ValidationError('Start Time must not be earlier than End Time!')

    name = StringField(
        "Name", [validators.DataRequired(), validators.length(min=1, max=100)]
    )

    desc = TextAreaField("Description", [validators.DataRequired()])

    date = DateField("Date", format="%Y-%m-%d")

    start_time = TimeField("Start Time", [validators.DataRequired(), start_time_check])

    end_time = TimeField("End Time", [validators.DataRequired(), end_time_check])

    image = FileField(
        "Image",
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
            
        ],
    )

    link = TextAreaField("Link", [validators.DataRequired()])


class UpdateOnsiteEvents(Form):

    def end_time_check(form, field):
        if field.data < form.start_time.data:
            raise ValidationError('End Time must not be earlier than Start Time!')

    def start_time_check(form, field):
        if field.data > form.end_time.data:
            raise ValidationError('Start Time must not be earlier than End Time!')

    name = StringField(
        "Name", [validators.Optional(), validators.length(min=1, max=100)]
    )

    desc = TextAreaField("Description", [validators.Optional()])

    date = DateField("Date", format="%Y-%m-%d", validators=(validators.Optional(),))

    start_time = TimeField("Start Time", [validators.Optional(), start_time_check])

    end_time = TimeField("End Time", [validators.Optional(), end_time_check])

    image = FileField(
        "Image (leave blank if unchanged)",
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )

    location = SelectField(
        "Location (leave blank if unchanged)",
        [validators.Optional()],
        choices=[
            ("empty", "Select"),
            ("Decathlon SGLab", "Decathlon SGLab"),
            ("Decathlon Bedok", "Decathlon Bedok"),
        ],
        default="",
    )

    quantity = IntegerField(
        "Quantity (Pax)",
        [
            validators.Optional(),
            validators.NumberRange(min=1, max=999999999),
        ],
    )

    price = IntegerField(
        "Price ($)",
        [
            validators.Optional(),
            validators.NumberRange(min=1, max=999999999),
        ],
    )


class UpdateLivestreamEvents(Form):

    def end_time_check(form, field):
        if field.data < form.start_time.data:
            raise ValidationError('End Time must not be earlier than Start Time!')

    def start_time_check(form, field):
        if field.data > form.end_time.data:
            raise ValidationError('Start Time must not be earlier than End Time!')

    name = StringField(
        "Name", [validators.Optional(), validators.length(min=1, max=100)]
    )

    desc = TextAreaField("Description", [validators.Optional()])

    date = DateField("Date", format="%Y-%m-%d")

    start_time = TimeField("Start Time", [validators.Optional(), start_time_check])

    end_time = TimeField("End Time", [validators.Optional(), end_time_check])

    image = FileField(
        "Image (leave blank if unchanged)",
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )

    link = TextAreaField("Link", [validators.Optional()])
