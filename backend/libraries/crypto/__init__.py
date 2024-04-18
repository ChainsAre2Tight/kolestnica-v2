"""Provides encryption controllers"""

from libraries.crypto.json_encryption import JSONEncryptionController
from libraries.crypto.token_encryption import TokenEncryptionController

json_encryptor = JSONEncryptionController.build()
token_encryptor = TokenEncryptionController.build()
