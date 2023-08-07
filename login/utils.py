from twilio.rest import Client
import random
class MessageHandler:
    phone_number = None
    otp = None

    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp(self):
        from twilio.rest import Client

        account_sid = 'enter-your-id-here'
        auth_token = 'enter-your-token-here'
        client = Client(account_sid, auth_token)

        message = client.messages.create( from_ = '+14176204460',
                                          body = f'Your OTP for Inspection is {self.otp}',
                                          to = self.phone_number
                                        )
