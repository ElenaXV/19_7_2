import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

invalid_email = os.getenv('invalid_email')
invalid_password = os.getenv('invalid_password')

invalid_auth_key = {"key":"ea874148a1f19838e1c5d1413877f3691a3731380e733e785b0ae352"}

