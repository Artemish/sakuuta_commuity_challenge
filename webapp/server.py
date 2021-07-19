from flask import Flask, render_template, request
from glob import glob
from pprint import pprint
from collections import defaultdict
import regex
import pandas
import json

app = Flask(__name__)

translations = pandas.read_csv('normalized.csv', index_col='lineno')

def completion_stats(section):
    return {
        'lines': len(section),
        'translated': len(section[section.translated]),
    }

def check_translated(line):
    return '\\u' in ascii(line['en_text'])

@app.route('/')
def hello_world():
    return render_template('page.html')

@app.route('/sections/<section_id>')
def get_section(section_id):
    qualified = "txt_scripts_jp/" + section_id
    section = translations[translations.section == qualified]
    completed = completion_stats(section)
    lines = [(l[1], l[2]) for l in section.to_records()]
    return render_template('section.html', section_id=section_id, lines=lines, completed=completed)

@app.route('/sections/<section_id>/as_json')
def get_section_json(section_id):
    qualified = "txt_scripts_jp/" + section_id
    section = translations[translations.section == qualified]
    x = json.loads(section.to_json())
    return section.to_json()

@app.route('/translate/<line_id>', methods=["POST"])
def translate_id(line_id):
    translated = request.data.decode('utf-8')
    line_id = int(line_id)
    translations.loc[line_id, "en_text"] = translated
    translations.loc[line_id, "translated"] = True
    translations.to_csv('normalized.csv')
    return '', 204
