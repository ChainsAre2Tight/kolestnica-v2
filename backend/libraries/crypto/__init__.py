"""Provides encryption controllers"""

from .json_encryption import JSONEncryptionController
from .token_encryption import TokenEncryptionController

json_encryptor = JSONEncryptionController.build()
token_encryptor = TokenEncryptionController.build()
