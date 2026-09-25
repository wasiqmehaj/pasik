import random

def generate_otp() -> str:
    """Generates a 6-digit OTP as a string."""
    return str(random.randint(100000, 999999))

def send_otp(phone: str) -> str:
    """
    Fake OTP sender for local development.
    In production this will call an SMS provider (e.g. MSG91/Twilio).
    For now it just prints the OTP so we can test the flow.
    """
    otp = generate_otp()
    print(f"[FAKE SMS] Sending OTP {otp} to {phone}")
    return otp

'''
if __name__ == "__main__":
    send_otp("9999999999")
'''