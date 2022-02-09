from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, FloatField, IntegerField, TimeField
from wtforms.fields import EmailField, DateField
from flask_wtf.file import FileAllowed, FileField, FileRequired

class CreateProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    ptype = RadioField('Product Type', choices=[('S', 'Shirt'), ('F', 'Footwear'), ('O', 'Other')], default='O')
    price = StringField('Product Price',[validators.Length(min=1, max=150), validators.DataRequired()], default='$')
    comments = TextAreaField('Comments', [validators.Optional()])
    stock = StringField('Amount of Stock', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField(
        "Image",
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )

class CreateShirtForm(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    ptype = RadioField('Product Type', choices=[('S', 'Shirt')], default='S')
    price = StringField('Product Price',[validators.Length(min=1, max=150), validators.DataRequired()], default='$')
    comments = TextAreaField('Comments', [validators.Optional()])
    ssize = RadioField('Shirt Size', choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='S')
    color = RadioField('Shirt Color', choices=[('G', 'Green'), ('B', 'Blue'), ('R', 'Red')], default='G')
    brand = StringField('Shirt Brand', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField(
        "Image",
        validators=[
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )

class AddOrder(Form):
    order = IntegerField(
        "Order Stock",
        [
            validators.InputRequired(message="Please enter a valid integer value."),
            validators.NumberRange(min=1, max=999999999),
        ],
    )

    order_date = DateField("Delivery Date", format="%Y-%m-%d")

    order_time = TimeField("Delivery Time", [validators.DataRequired()])
