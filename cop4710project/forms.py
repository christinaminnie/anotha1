from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class AddForm(FlaskForm):
    name = StringField('Name of Game:')
    description = StringField('Description:')
    release_date = StringField('Release Date:')
    compatibility = StringField('Compatibility:')
    price = StringField('Price:')
    submit = SubmitField('Add Game')
    company_name = SubmitField('Company:')


class DelForm(FlaskForm):
    id = IntegerField('Id Number of Game to Remove:')
    submit = SubmitField('Remove Game')


class AddRatingForm(FlaskForm):
    video_game_id = IntegerField('Video Game ID:')
    numeric_rating = IntegerField('Numeric Rating', validators=[InputRequired(), NumberRange(min=1, max=10)],
                                  render_kw={"placeholder": "Enter numeric rating (1-10)"})
    verbal_rating = StringField('Verbal Rating', validators=[InputRequired()],
                                render_kw={"placeholder": "Enter verbal rating"})
    submit = SubmitField('Add Rating')

class gameSearchForm(FlaskForm):
    choices = [('ID', 'ID'), ('Name', 'Name'), ('Release Date', 'ReleaseDate'), ('Price', 'Price')]
    select = SelectField('Search for Video Game:', choices=choices)
    search = StringField('')
    submit = SubmitField('')
