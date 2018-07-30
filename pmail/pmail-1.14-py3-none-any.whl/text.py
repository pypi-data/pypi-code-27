import base64


# Various text utilities
class Text:
    # Encrypts text
    @staticmethod
    def encrypt(text, key):
        if text and key:
            encoded = base64.urlsafe_b64encode(Text.reversed(text).encode("utf-8")).decode("utf-8")
            return encoded

    # Decrypts encrypted text
    @staticmethod
    def decrypt(text, key):
        if text and key:
            decoded = base64.urlsafe_b64decode(text).decode("utf-8")
            return Text.reversed(decoded)

    # Reverses text
    @staticmethod
    def reversed(s):
        return s[::-1]