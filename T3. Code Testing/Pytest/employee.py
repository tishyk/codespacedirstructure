# One more module for testing
import requests


class Employee():
    """A sample Employee class"""

    raise_amt = 1.05

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @property
    def email(self):
        return "{}.{}@email.com.ua".format(self.first, self.last)

    @property
    def fullname(self):
        return "{} {}".format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)

    def weekly_report(self, week):
        response = requests.get('http://company/com/{0}/reports/{1}'.format(self.first, week))
        # Test result will depend on site respond
        if response.ok:
            return response.text
        else:
            return "No response!"
