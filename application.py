from flask import Flask
from flask import jsonify
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import logging

application = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

application.json_encoder = DecimalEncoder

dynamodb = boto3.resource(service_name='dynamodb',
                          region_name='us-east-1',
                          # endpoint_url="http://localhost:8000"
                          )

table = dynamodb.Table('Movies')


@application.route('/')
def api_intro():

    intro = \
    """
    <h2> Welcome to the DataNorth API!  </h2>
    <h4> The following endpoints are available: </h4>

    <ul>
      <li>/movies/year</li>
    </ul>
    """

    return intro


@application.route('/movies/<year>/')
def movies(year):
    """ Sample movies endpoint. """
    fe = Key('year').eq(int(year));
    pe = "#yr, title, info.rating"
    # Expression Attribute Names for Projection Expression only.
    ean = { "#yr": "year", }
    esk = None


    response = table.scan(
        FilterExpression=fe,
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
        )

    results = [i for i in response['Items']]

    # for i in response['Items']:
    #     print(json.dumps(i, cls=DecimalEncoder))

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=pe,
            FilterExpression=fe,
            ExpressionAttributeNames= ean,
            ExclusiveStartKey=response['LastEvaluatedKey']
            )

        for i in response['Items']:
            # print(json.dumps(i, cls=DecimalEncoder))
            results.append(i)

    return jsonify(items=results)


if __name__ == "__main__":
    application.debug = True
    application.run()