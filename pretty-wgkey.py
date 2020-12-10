#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time
from base64 import b64encode
from string import ascii_uppercase, ascii_lowercase, digits

from nacl.public import PrivateKey

parser = argparse.ArgumentParser()
parser.add_argument("string", help="The string to find in the public key", type=str)
parser.add_argument(
        "-p",
        "--place",
        choices=["anywhere", "beginning"],
        default="anywhere",
        help="The place where to find the chosen string in the public key",
        type=str,
)
parser.add_argument(
        "-dt",
        "--doctest",
        action="store_true",
        help="Launch internal tests (provided by doctest)",
)
args = parser.parse_args()


def validate_string(s):
    """Check if string is combosed of base64 characters

    An arbitrary limit of maximum 10 chars has been set to limit computing time.

    >>> validate_string("string")
    True
    >>> validate_string("not-b64")
    Traceback (most recent call last):
      ...
    Exception: '-' is not a base64 character
    >>> validate_string("tooLongString")
    Traceback (most recent call last):
      ...
    Exception: String is longer than 10 characters.
    """
    allowed_chars = ascii_lowercase + ascii_uppercase + digits + "+/"
    if len(s) > 10:
        raise Exception("String is longer than 10 characters.")
    if s != "":
        for char in s:
            if char in allowed_chars:
                continue
            else:
                raise Exception("'{}' is not a base64 character".format(char))
        return True


def generate_keys() -> tuple:
    """Generate a pair of public and private keys.

    Returns a tuple (privkey, pubkey).

    >>> generate_keys()
    ('...=', '...=')
    """
    key = PrivateKey.generate()
    return (
        b64encode(bytes(key)).decode("ascii"),
        b64encode(bytes(key.public_key)).decode("ascii"),
    )


def found_in_key(method: str, string: str, pubkey: str) -> bool:
    """Search for a string

    Returns a boolean.

    >>> found_in_key("anywhere", "true", "lQeL7xeHoXQJfaa4z3/bF7DvpKTRuESk4MAqTy135Ss=")
    True
    >>> found_in_key("anywhere", "false", "lQeL7xeHoXQJfaa4z3/bF7DvpKTRuESk4MAqTy135Ss=")
    False
    >>> found_in_key("beginning", "true", "TruEyg6K3G/AP9O5uoOMyvkXrE+x0eWSh9bzBj39aHQ=")
    True
    >>> found_in_key("beginning", "false", "TruEyg6K3G/AP9O5uoOMyvkXrE+x0eWSh9bzBj39aHQ=")
    False
    """
    low_string = string.lower()
    low_key = pubkey.lower()
    if method == "anywhere":
        if low_string in low_key:
            return True
        else:
            return False
    elif method == "beginning":
        if low_key.startswith(low_string):
            return True
        else:
            return False


def get_speed(count: int, start_time: float, end_time: float) -> tuple:
    """Returns keys generated per second

    >>> get_speed(25, 1596183229.1117842, 1596183239.7695937)
    (10.658, 2.35)
    """
    duration = round(end_time - start_time, 3)
    speed = round(count / duration, 2)
    return (
        duration,
        speed,
    )


def print_matching_keys(name: str, privkey: str, pubkey: str):
    """Print matching keypair"""
    print("The following keypair matches '{}' you provided:\n".format(name))
    print("Private key: {}\tPublic key: {}\n".format(privkey, pubkey))


def main():
    name = args.string
    validate_string(name)
    method = args.place
    start_time = time.time()
    print("\nGenerating keys, this can take a long time...\n")
    found = False
    count = 0
    while not found:
        try:
            privkey, pubkey = generate_keys()
            found = found_in_key(method, name, pubkey)
            count += 1
        except KeyboardInterrupt:
            print("CTRL-C detected, aborting...\n")
            break

    if found:
        print_matching_keys(name, privkey, pubkey)

    end_time = time.time()

    duration, speed = get_speed(count, start_time, end_time)
    print(
            "{} keys generated in {} seconds ({} keys per second).\n".format(
                    count, duration, speed
            )
    )


if __name__ == "__main__":
    if args.doctest:
        import doctest

        doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
    else:
        main()
