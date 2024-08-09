# Third Party Stuff
# import nexmo
import requests
from phone_verify.backends.base import BaseBackend


class BdsmsBackend(BaseBackend):

    def __init__(self, **options):
        super().__init__(**options)

        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}
        self._key = options.get("key", None)
        self._secret = options.get("secret", None)
        self._from = options.get("from", None)

        # specific to bdsms
        self._bdsms_token = options.get("bdsms_token", None)
        self._bdsms_endpoint = options.get("bdsms_endpoint", None)

        # Create a Nexmo Client object
        # self.client = nexmo.Client(key=self._key, secret=self._secret)

    def send_sms(self, number, message):
        # Implement your service's SMS sending functionality
        data = {
            'token': self._bdsms_token,
            'to': number,
            'message': message,
        }
        # TODO: Remove this line in production
        print(f"message: {message}")
        responses = requests.post(url=self._bdsms_endpoint, data=data)

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(self, number=number, message=message)
