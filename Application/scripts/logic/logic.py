import re
import json
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from config import URL_REG
import string
import random
from logger.log import MyLogging
from tldextract import extract


super_logger = MyLogging().setup_logger('logic',
                                        'Application/logger/logfile.log')


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
        short_link = "".join(random.choice(string.ascii_lowercase + string.digits) for x in
                             range(random.randrange(5, 8)))

        dns = self.get_domain(url=link_from_form)
        if dns:
            short_link = 'line/' + dns + short_link
        else:
            short_link = 'line/' + short_link

        return short_link

    def get_domain(self, *_, **kwargs):
        """The method can take domen name from url."""
        url = kwargs.get('url')
        subdomain, domain, suffix = extract(url)
        ignored = ["www", "web", "ru"]
        if not subdomain or subdomain.lower() in ignored:
            return domain
        pat = r"^(?:{})\.".format("|".join(ignored))
        return re.sub(pat, "", subdomain)
