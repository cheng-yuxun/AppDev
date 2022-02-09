from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, ValidationError, FileField
from datetime import datetime
from wtforms.fields import DateField

class CreateForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    points = StringField('Points', [validators.Length(min=1, max=50), validators.DataRequired()])

    def validate_points(form, points):
        if not points.data.isdigit():
            raise ValidationError("Points must be in numerical form")

    category = SelectField('Category', [validators.Length(min=1, max=50), validators.DataRequired()],
                           choices=[('', 'Select'), ('Product', 'Product'), ('Electronics', 'Electronics')], default='')
    redemption = StringField('Redemption', default=0)
    code = StringField('Code', [validators.Length(min=1, max=50), validators.DataRequired()])
    def validate_code(form,code):
        if not code.data[:2].isalpha():
            raise ValidationError("First 2 characters must be in alphabet form")
        elif not code.data[2:].isdigit():
            raise ValidationError("After the 2 characters, the rest of the characters must be in numerical form")
    description = TextAreaField("Description", [validators.DataRequired()])
    date_start = DateField('Start date', format="%Y-%m-%d")
    date_expire = DateField('Expiry date', format="%Y-%m-%d")
    picture = FileField("Picture")
    #date_start = datetime.now().strftime("%d/%m/%Y")
    #date_expire = datetime.now().strftime("%d/%m/%Y")



class CreateAchievements(Form):
    subject = StringField('Subject', [validators.Length(min=1, max=50), validators.DataRequired()])
    content = TextAreaField('Content', [validators.DataRequired()])
    date_start = datetime.now().strftime("%d/%m/%Y")
    date_expire = datetime.now().strftime("%d/%m/%Y")
