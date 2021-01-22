import re
import json
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from config import URL_REG
import string
import random


class EnterForm(FlaskForm):
    """The Form for enter a link."""
    link = StringField("Вставьте или введите ссылку", validators=[DataRequired()])
    submit = SubmitField('ОК')


class HandlerLink:
    """The class for work with links."""
    def check_input_link(self, *_, **kwargs) -> bool:
        """This method can to check a link on match with pattern."""
        link_from_form = kwargs.get('link_from_form')
        if re.match(URL_REG, link_from_form):
            return True
        return False

    def generate_short_link(self, *_, **kwargs) -> str:
        """The method for change a long link."""
        link_from_form = kwargs.get('link_from_form')
        new_link = link_from_form.split('/')

        short_link = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in
                             range(random.randrange(5, 8)))
        if new_link:
            dns = link_from_form.split('/')[2] + '_'
            short_link = dns + short_link

        return short_link




