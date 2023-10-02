from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, widgets, SubmitField


class PlaylistForm(FlaskForm):
    title = StringField('Title', render_kw={'placeholder': 'Title'})
    songs = SelectMultipleField(
        'Songs',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
        coerce=str
    )
    submit = SubmitField('Add')
