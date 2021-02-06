from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Optional

class AddPlantForm(FlaskForm):
    plant_name = StringField('Plant Name', validators=[DataRequired()])
    adoption_date = DateField('Adoption Date', validators=[Optional()])
    pot_size = DecimalField('Pot Size (inches)', validators=[Optional(), NumberRange(0.00, 99.50)])
    purchase_location = StringField('Purchase Location', validators=[Optional()])
    purchase_price = DecimalField('Purchase Price', validators=[Optional()])
    submit = SubmitField('Add Plant')