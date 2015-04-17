import cred_aws
import boto.sns
import logging
import logging.handlers
import json
from alchemyapi import AlchemyAPI
import base64
from wsgiref.simple_server import make_server

alchemyapi = AlchemyAPI()

# Connect sns
sns = boto.sns.connect_to_region(
    "us-east-1",
    aws_access_key_id=cred_aws.aws_access_key_id,
    aws_secret_access_key=cred_aws.aws_secret_access_key)
topicarn = cred_aws.aws_sns_topicarn

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler
LOG_FILE = '/opt/python/log/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

def application(environ, start_response):
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size).decode()
                domain = base64.b64decode(request_body)
                domain = json.loads(domain)
                try:
                    message = domain['content']
                    mid = domain['id']
                    alch_resp = alchemyapi.sentiment('text', message)
                    senti = alch_resp["docSentiment"]["type"]
                    logger.info("Received message: Sentiment: %s" %senti)
                    sns.publish(topicarn, json.dumps({'id': mid, 'senti': senti}))
                except Exception:
                    logger.warning('Error receiving data')
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = ''
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]



if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
