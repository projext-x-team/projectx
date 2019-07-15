from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired, url

class SearchSwimmerForm(Form):
    swimmername = StringField('Swimmer Name:', validators=[DataRequired()])

    def validate(self):
        if not self.swimmername.data:
            return False
        else:
            return True