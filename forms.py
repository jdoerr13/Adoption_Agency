from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional
from wtforms.widgets import CheckboxInput
from wtforms.fields import SelectField

class AddPetForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired("please add a name")])
    species = SelectField("Species", choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()],)
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)],)
    notes = TextAreaField("Notes")
    available = BooleanField("Available", widget=CheckboxInput())


class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL", validators=[Optional()])
    notes = TextAreaField("Notes")
    available = BooleanField("Available")