import logging

class Customer ():
    def __init__(self, id, date, email):
        self.id = id
        self.date = date
        self.email = email

    def get_customer_details(self):
        logging.info(f"The customer {self.email} has the id ({self.id}) and was created on {self.date}.")
