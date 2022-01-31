"""Module that contains type aliases for schema classes' fields, arguments,
etc"""

# pylint: disable=too-few-public-methods

import re
from typing import Dict, Any
from pathlib import Path

# pylint: disable-next=no-name-in-module
from pydantic import ConstrainedStr


# Base 64 patterns are strict, but in reality you can
# send any file through an HTTP URL, since
# I can't know whether is it the correct type
# for the field or not

with open(
    str(Path(__file__).parent / "pattern_base_64_image"), "r", encoding="utf-8"
) as f:
    base_64_pattern_image = f.read().strip()

with open(
    str(Path(__file__).parent / "pattern_base_64_video"), "r", encoding="utf-8"
) as f:
    base_64_pattern_video = f.read().strip()

with open(
    str(Path(__file__).parent / "pattern_base_64_audio"), "r", encoding="utf-8"
) as f:
    base_64_pattern_audio = f.read().strip()

with open(
    str(Path(__file__).parent / "pattern_base_64_file"), "r", encoding="utf-8"
) as f:
    base_64_pattern_file = f.read().strip()

with open(
    str(Path(__file__).parent / "pattern_base_64_document"),
    "r",
    encoding="utf-8"
) as f:
    base_64_pattern_document = f.read().strip()

JsonDict = Dict[str, Any]


class NonEmpty(ConstrainedStr):
    """Type for schema classes field strings that must be non-empty"""

    min_length = 1
    strict = True


class Phone(ConstrainedStr):
    """Type for schema classes field strings that must be a phone number"""

    max_length = 13
    regex = re.compile(r"\d+")
    strict = True
    min_length = 9


class Base64(NonEmpty):
    """Type for schema classes base64 string fields, contains base regex
    pattern"""

    strict = True
    max_length = 150000
    regex = re.compile(base_64_pattern_file)


class Base64Audio(Base64):
    """Type for schema classes audio base64 string fields, contains ogg regex
    pattern"""

    max_length = 10000
    regex = re.compile(base_64_pattern_audio)


class Base64Image(Base64):
    """Type for schema classes image base64 string fields, contains image
    mimetype regex pattern"""

    regex = re.compile(base_64_pattern_image)


class Base64Video(Base64):
    """Type for schema classes video base64 string fields, contains video
    mimetype regex pattern"""

    regex = re.compile(base_64_pattern_video)


class Base64Document(Base64):
    """Type for schema classes video base64 string fields, contains video
    mimetype regex pattern"""

    regex = re.compile(base_64_pattern_document)


class MessageBody(NonEmpty):
    """Type for schema classes field strings that must be a message body"""

    max_length = 20000
    strict = True


class Filename(NonEmpty):
    """Type for schema classes field strings that must be a filename"""

    strict = True
    max_length = 300


class Endpoint(NonEmpty):
    """Type for schema classes field strings that must be an endpoint, contains
    endpoint regex"""

    strict = True
    regex = re.compile(r"(\/{1})([-a-zA-Z0-9()@:%_.~#?&=]*)")
