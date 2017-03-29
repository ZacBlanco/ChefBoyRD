from datetime import datetime, timedelta
from random import randrange
import math

class TestMessages(object):
    """
    test class that emulates how twilio stores messages, so that this can be run to test the funtions without a connection to twilio
    """
    def __init__ (self, sid, date_sent, body, from_):
        self.sid = sid
        self.date_sent = date_sent
        self.body = body
        self.from_ = from_

def test_sms_data(n,date_from):
    """
    Creates n samples of SMS of a pre-determined body, listed in sample_messages
    If n is >5, then more sample feedback messages must be added to the list below
    """
    #d = random_date(date_from,datetime.now(), n)
    sample_messages = ["First timer. Ordered at counter. Wide selection of healthy choices. Had \"Fish & Chips\" pain plus cup of red pepper soup. Very tasty but pain bun to thick. Tuesday after Labor Day not very busy.",
                        "I was very impressed with Mixed! Not only was the food delicious (I had the club panini & lasagna soup) the staff was extremely friendly. Will definitely be back and highly recommend!! Great find for a fresh and healthy option.",
                        "Visiting family from California and we dropped by this place. My mom loved the Caribbean crunch salad. I had the opah and is was okay. It had black olive instead of kalamata olives which was disappointing. Serving sizes are huge but overall I was underwhelmed by my salad. My brother had a wrap that looked tastey",
                        "It's just ok. Nothing to write home about or admit to anyone that I came here on a Friday night.",
                        "The food was amazing and the service was excellent! 5/5!"
                        ] # sample messages for running tests. TODO: generate/scrape random feedback
    messages = []
    for y in range(0,n):
        msg = TestMessages(y, datetime.now(),sample_messages[y], "+12345678905")
        messages.append(msg)
    return messages


