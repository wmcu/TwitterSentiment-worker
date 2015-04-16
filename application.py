import logging
import logging.handlers
import json
import flask
from flask import request, Response
from alchemyapi import AlchemyAPI

application = flask.Flask(__name__)
application.config.from_object('default_config')
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

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

@application.route('/', methods=['POST'])
def worker():
	response = None
	if request.json is None:
		response = Response("", status=415)
	else:
		message = None
		try:
			if request.json.has_key('id') and request.json.has_key('content'):
				message = request.json['content']
				alch_resp = alchemyapi.sentiment("text", message)
				logger.info("Received message: Sentiment: %s" % alch_resp["docSentiment"]["type"])
				# print "Sentiment: ", alch_resp["docSentiment"]["type"]
			else:
				logger.warning('Error retrieving request body for async work.')
				# print "No message"

		except Exception as ex:
			logging.exception('Error processing message: %s' % request.json)
			response = Response(ex.message, status=500)

	return response


if __name__ == '__main__':
	application.run(host='0.0.0.0', port=80)
