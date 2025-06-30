from twilio.rest import Client
from django.conf import settings

def send_otp_sms(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print("Twilio SMS sent:", message.sid)
        return True
    except Exception as e:
        print("Error sending SMS:", e)
        return False
