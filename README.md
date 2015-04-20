# TwitterSentiment-worker

This is the worker app for a twitter sentiment analysis app.

## Framework
Built with python WSGI interface. Read twits from SQS. Do sentiment by
sentiment api (www.mashape.com/vivekn/sentiment-3/). Publish sentiment result
to SNS.
