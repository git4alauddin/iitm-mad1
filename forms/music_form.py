# imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac'}

# form music
class MusicForm(FlaskForm):
    title = StringField('Title', render_kw={'placeholder': 'Title'})
    artist = StringField('Artist', render_kw={'placeholder': 'Artist'})
    genre = StringField('Genre', render_kw={'placeholder': 'Genre'})
    lyrics = TextAreaField('Lyrics', render_kw={'placeholder': 'Lyrics'})
    audio_file = FileField('Choose a file', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Only audio files are allowed')])
    submit = SubmitField('Add')

  


