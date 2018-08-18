class Email(object):
    def __init__(self, harvested_date, sent_date, email_body, email_id, label, messages):
        self.harvested_date = harvested_date
        self.sent_date = sent_date
        self.email_body = email_body
        self.email_id = email_id
        self.label = label
        self.messages = messages

    def parse_email(self):
        # TODO implement this method to return a string of Message objects
        pass
