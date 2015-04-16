import logging
import logging.handlers
import json
# import flask
# from flask import request, Response
from alchemyapi import AlchemyAPI
import base64
from wsgiref.simple_server import make_server

# application = flask.Flask(__name__)
# application.config.from_object('default_config')
# application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

alchemyapi = AlchemyAPI()

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

# @application.route('/', methods=['POST'])
# def worker():
# 	response = None
# 	if request.json is None:
# 		response = Response("", status=415)
# 	else:
# 		message = None
# 		try:
# 			if request.json.has_key('id') and request.json.has_key('content'):
# 				message = request.json['content']
# 				alch_resp = alchemyapi.sentiment("text", message)
# 				logger.info("Received message: Sentiment: %s" % alch_resp["docSentiment"]["type"])
# 				# print "Sentiment: ", alch_resp["docSentiment"]["type"]
# 			else:
# 				logger.warning('Error retrieving request body for async work.')
# 				# print "No message"

# 		except Exception as ex:
# 			logging.exception('Error processing message: %s' % request.json)
# 			response = Response(ex.message, status=500)

# 	return response

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
                	# mid = domain['id']
                	alch_resp = alchemyapi.sentiment('text', message)
                	logger.info("Received message: Sentiment: %s" % alch_resp["docSentiment"]["type"])
                except Exception:
                	logger.warning('Error receiving data')
                # logger.info("Received message: %s" % domain)
            # elif path == '/scheduled':
            #     logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'], environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = welcome
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()

# if __name__ == '__main__':
# 	application.run(host='0.0.0.0')