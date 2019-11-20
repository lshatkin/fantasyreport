"""Insta485 development configuration."""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\r\xb3\xa2\x81\xc7\xe50\x0e\x1bO\x8d\xe2\x81\xc5C\xbdp`;Z9\x064\x96'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'uploads'
)

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'fantasyApp.sqlite3'
)
