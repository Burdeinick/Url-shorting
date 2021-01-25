import os
import json
import sqlite3
from scripts.logic.logic import EnterForm, HandlerLink
from scripts.logic.FDataBase import FDataBase
from flask import Flask, request, render_template, g, redirect
from config import DATABASE, SECRET_KEY
from logger.log import MyLogging


super_logger = MyLogging().setup_logger('logic',
                                        'Application/logger/logfile.log')


app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    """The function can connect to db."""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """The get_db function can be used to get the current database connection."""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """The function for close connect with db."""
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/", methods=['POST', 'GET'])
def index():
    """The function for work with start page."""
    input_link = EnterForm()

    if input_link.validate_on_submit():
        data_from_form = input_link.link.data
        if 'https://' not in data_from_form and 'http://' not in data_from_form:
            return render_template('bad_link.html')

        if HandlerLink().check_input_link(link_from_form=data_from_form):
            short_link = HandlerLink().generate_short_link(link_from_form=data_from_form)
            add_links_to_db = dbase.add_links(long_link=data_from_form, short_link=short_link)

            if short_link and add_links_to_db:
                return render_template('short_link.html', short_link=short_link)
        return render_template('bad_link.html')

    return render_template('index.html', form=input_link)


@app.route("/new_line/<short_link>")
def short_link_redirect(short_link):
    """The function for redirect a link to origin url."""
    try:
        origin_link = dbase.get_long_link(short_link="new_line/" + short_link)
        if origin_link:
            return redirect(origin_link)

        else:
            return render_template('bad_link.html')

    except Exception as e:
        super_logger.error(f'Error {str(e)} in short_link_redirect(file - main.py)', exc_info=True)
        return render_template('bad_link.html')


if __name__ == "__main__":
    app.run()
