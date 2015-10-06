from __future__ import print_function

import flask

from sr.robot import Robot


R = Robot()
app = flask.Flask(__name__)


@app.route('/pages')
def pages():
    return flask.jsonify(pages=[
        {
            'name': 'my-custom-page',
            'title': 'My Custom Page',
            'import_url': '/pages/my-page'
        }
    ]), 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/pages/my-page')
def my_page():
    return """
        <dom-module id="my-custom-page">
            <template>
                <h1>It's a custom page!</h1>
            </template>

            <script>
                Polymer({
                    is: 'my-custom-page'
                });
            </script>
        </dom-module>
    """, 200, {'Access-Control-Allow-Origin': '*'}

app.run(port=10000)
