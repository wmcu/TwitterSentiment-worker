# -*- coding: utf-8 -*-
import requests

class SentimentAPI():
    endpoint = r"https://community-sentiment.p.mashape.com/text/"

    def __init__(self):
        with open("api_key.txt", "r") as f:
            self.api_key = f.read().strip()

        self.header = {
            "X-Mashape-Key": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

    def sentiment(self, text):
        response = requests.post(self.endpoint,
            headers=self.header,
            data={"txt": unicode(text)}
        )
        try:
            # print response.text
            result = response.json()
            ret = result["result"]["sentiment"].lower()
        except:
            ret = None
        return ret


if __name__ == '__main__':
    api = SentimentAPI()
    # for i in range(1000):
    #     result = api.sentiment("Today is a good day")
    #     if result != "Positive":
    #         print "Error %s" % i
    #         break
    result = api.sentiment(u"渣渣")
    print result

    result = api.sentiment(u"happy")
    print result
