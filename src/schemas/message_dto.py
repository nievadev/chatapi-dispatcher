"""Module that contains the MessageDTO schema along with plenty of templates"""

import os
from typing import Optional, Union, NoReturn, Dict, Any, ClassVar, Tuple
from urllib.parse import urlparse, unquote
from mimetypes import guess_extension

# pylint: disable-next=no-name-in-module
from pydantic import BaseModel, HttpUrl, root_validator, Field, validator

from src.utils.type_aliases import (
    Phone,
    JsonDict,
    Base64Audio,
    Base64Image,
    Base64Video,
    Base64Document,
    MessageBody,
    NonEmpty,
)

from src.utils import errors, file_examples
from src.env_variables import env_variables


Audio = Union[Base64Audio, HttpUrl]
Image = Union[Base64Image, HttpUrl]
Video = Union[Base64Video, HttpUrl]
Document = Union[Base64Document, HttpUrl]

# NIEVATODO: Move these examples' definitions somewhere else
required_template = {
    "instance": env_variables.TEST_INSTANCE,
    "token": env_variables.TEST_TOKEN,
    "phone": env_variables.TEST_PHONE,
}

text_template = {"text": "Hello Martin!", **required_template}

image_template = {
    "image": "\
https://www.applecoredesigns.co.uk/wp-content/uploads/2018/08/button-ok.png\
",
    **required_template,
}

video_template = {
    "video": "http://techslides.com/demos/sample-videos/small.mp4",
    **required_template,
}

audio_template = {
    "audio": "https://filesamples.com/samples/audio/opus/sample3.opus",
    **required_template,
}

audio_template_base64 = {
    "audio": file_examples.base64_audio,
    **required_template
}

image_template_base64 = {
    "image": file_examples.base64_image,
    **required_template
}

video_template_base64 = {
    "video": file_examples.base64_video,
    **required_template
}

document_template_base64_odt = {
    "document": file_examples.base64_document_odt,
    **required_template
}

document_template_base64_docx = {
    "document": file_examples.base64_document_docx,
    **required_template
}

document_template_base64_pdf = {
    "document": file_examples.base64_document_pdf,
    **required_template
}

document_template_pdf = {
    "document": "\
https://dagrs.berkeley.edu/sites/default/files/2020-01/sample.pdf",
    **required_template
}

document_template_docx = {
    "document": "\
https://filesamples.com/samples/document/docx/sample3.docx",
    **required_template
}

document_template_odt = {
    "document": "\
https://filesamples.com/samples/document/odt/sample3.odt",
    **required_template
}


def get_filename_from_base64(base64_string: str) -> Optional[str]:
    """Function that gets a filename from a base64 string

    It gets the string between 'data:' and until the ';' to pass it to
    the guess_extension function. In case the guess_extension returns None,
    it's not a valid mimetype and hence this function returns None
    """

    len_first_base64_chars = len("data:")
    where_does_finish_mimetype = base64_string.find(";")

    mimetype = base64_string[len_first_base64_chars:where_does_finish_mimetype]

    extension = guess_extension(mimetype)

    if extension:
        return f"noname{extension}"

    return None


def get_filename_from_url(url: str) -> Optional[str]:
    """Function that gets a filename from a URL

    It parses the whole URL with urlparse function to get the
    urllib.parse.ParseResult object, and if there is no 'netloc' in it (None),
    it's not a valid URL and hence this function returns None
    """

    parsed_url = urlparse(url)

    if not parsed_url.netloc:
        return None

    return unquote(os.path.basename(parsed_url.path), "utf-8")


class MessageDTO(BaseModel):
    """MessageDTO schema class"""

    # pylint: disable-next=too-few-public-methods
    class Config:
        """Config metaclass"""

        underscore_attrs_are_private = True

    incompatible_fields: ClassVar[Tuple[Tuple[str, ...], ...]] = (
        ("text", "image", "video", "audio", "document"),
    )

    at_least_fields: ClassVar[Tuple[str, ...]] = (
        "image", "video", "text", "audio", "document"
    )

    image: Optional[Image] = Field(
        default=None, title="Image file", description="\
The image in HTTP URL or Base64"
    )

    video: Optional[Video] = Field(
        default=None, title="Video file", description="\
The video in HTTP URL or Base64"
    )

    document: Optional[Document] = Field(
        default=None, title="Document file", description="\
The document in HTTP URL or Base64"
    )

    text: Optional[MessageBody] = Field(
        default=None, title="Text body", description="The text of the message"
    )

    audio: Optional[Audio] = Field(
        default=None,
        title="Audio file",
        description="\
The audio in HTTP URL or Base64. It must be in OGG Opus format!",
    )

    phone: Phone = Field(
        default=...,
        title="Phone number",
        description="The phone number that must be in international format",
    )

    token: NonEmpty = Field(
        default=...,
        title="Message sender token",
        description="\
The message sender token that is gonna be used for credentials",
    )

    instance: NonEmpty = Field(
        default=...,
        title="Message instance id",
        description="\
The message instance id that is gonna be used for credentials",
    )

    filename: Optional[str] = Field(
        default=None,
        title="Filename of the resource sent",
        description="\
This is the filename of the resource sent. Do not set, as it'll be ignored,\
 since this is an auto-defined value on validation",
    )

    @root_validator(pre=True)
    def check_only_one(
        cls, values: JsonDict
    ) -> Union[JsonDict, NoReturn]:
        # pylint: disable=no-self-argument
        # pylint: disable=no-self-use

        """Validator function that reads into incompatible_fields and
        checks that there are no incompatibilities in the current instance's
        fields"""

        for incompatible in cls.incompatible_fields:
            ocurrences = 0

            for field in incompatible:
                if values.get(field):
                    ocurrences += 1

                if ocurrences > 1:
                    break

            else:
                continue

            the_fields = {
                k: values.get(k)
                for k in incompatible
            }

            raise errors.OnlyOneOfThemError(
                only_one=tuple(the_fields.keys()),
                values=tuple(the_fields.values())
            )

        return values

    @root_validator(pre=True)
    def check_at_least_one(
        cls, values: JsonDict
    ) -> Union[JsonDict, NoReturn]:
        # pylint: disable=no-self-argument
        # pylint: disable=no-self-use

        """Validator function that checks after every field has been
        validated that there is at least ONE field of the ones located in
        the iterable at_least_fields"""

        the_fields = {
            k: values.get(k)
            for k in cls.at_least_fields
        }

        fields_set = set(the_fields.values())

        if len(fields_set) > 1 or None not in fields_set:
            return values

        raise errors.AtLeastOneOfThemError(
            at_least=cls.at_least_fields,
            values=tuple(the_fields.values())
        )

    @validator("filename", always=True)
    def check_valid_filename(cls, _, values: Dict[str, Any]):
        # pylint: disable=no-self-argument
        # pylint: disable=no-self-use

        """Validator function that checks that the given assets have an
        autodetectable file extension, Chat API can error based on that, so
        this is a measure, it also sets the filename"""

        to_parse = (
            values.get("image") or
            values.get("video") or
            values.get("document")
        )

        filename = None

        if not to_parse:
            return filename

        if isinstance(to_parse, HttpUrl):
            filename = get_filename_from_url(str(to_parse))

        elif isinstance(to_parse, str):
            filename = get_filename_from_base64(to_parse)

        if not filename:
            raise errors.BadFilenameNotRecognizedError

        return filename
