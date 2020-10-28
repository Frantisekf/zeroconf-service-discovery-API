import markdown
import os
from flask import Flask

# create instance of flask
app = Flask(__name__)


@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + '/README.md') as markdown_file:

        content = markdown_file.read()

        return markdown.markdown(content)
