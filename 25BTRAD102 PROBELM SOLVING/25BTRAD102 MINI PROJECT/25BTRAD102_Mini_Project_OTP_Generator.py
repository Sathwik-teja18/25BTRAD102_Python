"""
USN: 25BTRAD102
MINI PROJECT 2: TIME-BASED ONE-TIME PASSWORD (TOTP) GENERATOR

A standalone implementation of the TOTP algorithm. It does not use pyotp or
another OTP-specific package. Only Python's standard library is used:

- secrets: cryptographically secure secret generation
- base64: Base32 secret encoding
- hmac and hashlib: HMAC-SHA1
- struct: 8-byte moving counter encoding
- time: 30-second time counter
- urllib.parse: authenticator provisioning URI

Algorithm:
1. Generate a random secret and encode it as Base32.
2. Calculate counter = floor(Unix time / 30).
3. Calculate HMAC-SHA1(secret, counter).
4. Apply dynamic truncation to obtain a 31-bit integer.
5. Reduce modulo 10^6 to produce a six-digit OTP.
6. Verify with constant-time comparison and an optional clock-drift window.

Security note: Keep the shared secret private. A production authentication
system also needs protected secret storage, rate limiting, secure enrollment,
recovery controls, and a security review.
"""

import base64
import hashlib
import hmac
import secrets
import struct
import time
from urllib.parse import quote, urlencode

DEFAULT_DIGITS = 6
DEFAULT_PERIOD = 30


class TOTPAuthenticator:
    """Generate and verify time-based one-time passwords."""

    def __init__(self, secret, digits=DEFAULT_DIGITS, period=DEFAULT_PERIOD):
        if not 6 <= digits <= 8:
            raise ValueError("OTP length must be between 6 and 8 digits.")
        if period <= 0:
            raise ValueError("Time period must be greater than zero.")
        self.secret = self._decode_secret(secret)
        self.digits = digits
        self.period = period

    @staticmethod
    def generate_secret(byte_length=20):
        """Return a cryptographically random Base32 secret."""
        if byte_length < 16:
            raise ValueError("Use at least 16 random bytes for the secret.")
        raw_secret = secrets.token_bytes(byte_length)
        return base64.b32encode(raw_secret).decode("ascii").rstrip("=")

    @staticmethod
    def _decode_secret(secret):
        """Decode a Base32 secret, accepting whitespace and omitted padding."""
        if not isinstance(secret, str):
            raise TypeError("The shared secret must be text.")
        cleaned = "".join(secret.split()).upper()
        if not cleaned:
            raise ValueError("The shared secret cannot be empty.")
        padded = cleaned + ("=" * ((8 - len(cleaned) % 8) % 8))
        try:
            return base64.b32decode(padded, casefold=True)
        except (ValueError, base64.binascii.Error) as error:
            raise ValueError("Invalid Base32 secret. Check the copied key.") from error

    def generate(self, timestamp=None):
        """Generate the OTP for the supplied Unix timestamp or current time."""
        current_time = time.time() if timestamp is None else float(timestamp)
        if current_time < 0:
            raise ValueError("Timestamp cannot be negative.")
        counter = int(current_time // self.period)
        counter_bytes = struct.pack(">Q", counter)
        digest = hmac.new(self.secret, counter_bytes, hashlib.sha1).digest()

        # Dynamic truncation: low four bits of the final digest byte.
        offset = digest[-1] & 0x0F
        binary_code = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
        otp_value = binary_code % (10 ** self.digits)
        return f"{otp_value:0{self.digits}d}"

    def verify(self, supplied_code, timestamp=None, valid_window=1):
        """Verify a code at current time +/- valid_window time steps."""
        code = str(supplied_code).strip()
        if len(code) != self.digits or not code.isdigit():
            return False
        if valid_window < 0:
            raise ValueError("Valid window cannot be negative.")

        current_time = time.time() if timestamp is None else float(timestamp)
        current_counter = int(current_time // self.period)
        for offset in range(-valid_window, valid_window + 1):
            counter_time = (current_counter + offset) * self.period
            if counter_time < 0:
                continue
            expected = self.generate(counter_time)
            if hmac.compare_digest(expected, code):
                return True
        return False

    def seconds_remaining(self, timestamp=None):
        """Return seconds remaining in the current OTP time step."""
        current_time = time.time() if timestamp is None else float(timestamp)
        elapsed = int(current_time) % self.period
        return self.period - elapsed

    def provisioning_uri(self, account_name, issuer="25BTRAD102"):
        """Build an otpauth URI for adding the secret to an authenticator app."""
        encoded_secret = base64.b32encode(self.secret).decode("ascii").rstrip("=")
        label = quote(f"{issuer}:{account_name}", safe=":")
        parameters = urlencode({
            "secret": encoded_secret,
            "issuer": issuer,
            "algorithm": "SHA1",
            "digits": self.digits,
            "period": self.period,
        })
        return f"otpauth://totp/{label}?{parameters}"


def create_new_authenticator():
    print("\n--- CREATE AUTHENTICATOR SECRET ---")
    account_name = input("Enter account name / label: ").strip() or "student-account"
    secret = TOTPAuthenticator.generate_secret()
    authenticator = TOTPAuthenticator(secret)
    print("\nYour new Base32 shared secret is:")
    print(secret)
    print("\nSave this secret privately. Anyone who obtains it can generate your OTPs.")
    print("Do not post it, commit it to GitHub, or share it.")
    print("\nProvisioning URI (for authenticator-app setup):")
    print(authenticator.provisioning_uri(account_name))


def load_authenticator():
    secret = input("Enter your Base32 shared secret: ").strip()
    try:
        return TOTPAuthenticator(secret)
    except (TypeError, ValueError) as error:
        print(f"Unable to load secret: {error}")
        return None


def generate_current_otp():
    print("\n--- GENERATE CURRENT OTP ---")
    authenticator = load_authenticator()
    if authenticator is None:
        return
    print(f"Current rotating OTP: {authenticator.generate()}")
    print(f"This code changes in approximately {authenticator.seconds_remaining()} second(s).")


def verify_otp():
    print("\n--- VERIFY OTP ---")
    authenticator = load_authenticator()
    if authenticator is None:
        return
    supplied_code = input(f"Enter the {authenticator.digits}-digit OTP: ").strip()
    if authenticator.verify(supplied_code, valid_window=1):
        print("Verification successful!")
    else:
        print("Verification failed. The code may be incorrect or expired.")


def main():
    while True:
        print("\n========== TOTP AUTHENTICATOR ==========")
        print("1. Generate a new shared secret")
        print("2. Generate the current OTP")
        print("3. Verify an OTP")
        print("4. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            create_new_authenticator()
        elif choice == "2":
            generate_current_otp()
        elif choice == "3":
            verify_otp()
        elif choice == "4":
            print("Exiting OTP authenticator.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
