from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
# form album
class AlbumForm(FlaskForm):
    title = StringField('Title', render_kw={'placeholder': 'Title'})
    genre = StringField('Genre', render_kw={'placeholder': 'Genre'})
    submit = SubmitField('Add')