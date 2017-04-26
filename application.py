from flask import Flask
application = Flask(__name__)


@application.route('/')
def hello_world():

    return 'Please use /api to use the DataNorth API.'

@application.route('/api')
def api_intro():

    intro = \
    """
    <h2> Welcome to the DataNorth API!  </h2>
    <h4> The following endpoints are available: </h4>

    <ul>
      <li>/api/crime</li>
      <li>/api/energy</li>
      <li>/api/housing</li>
    </ul>
    """

    return intro


if __name__ == "__main__":
    application.debug = True
    application.run()