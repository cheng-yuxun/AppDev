from wtforms import (
    Form,
    StringField,
    RadioField,
    DateField,
    SelectField,
    ValidationError,
    validators
    )

class Search(Form):
    search = StringField(
        "Search", [validators.Optional()]
    )

class EventFilter(Form):
    def date_check(form, field):
        if field.data >= form.end_date.data:
            raise ValidationError('Invalid date duration')

    onsite = RadioField('Onsite', choices=[('Onsite', 'Onsite')])
    livestream = RadioField('Livestream', choices=[('Livestream', 'Livestream')])
    start_date = DateField("Start Date", format="%Y-%m-%d", validators=[date_check])
    end_date = DateField("End Date", format="%Y-%m-%d")
    status = SelectField('Status', [validators.Optional()],
                        choices=[('', 'Select'), 
                        ('Active', 'Active'), 
                        ('Inactive', 'Inactive'),
                        ('Ongoing', 'Ongoing'),
                        ('Expired', 'Expired'),
                        ('Full', 'Full')
                        ], 
                        default='')
