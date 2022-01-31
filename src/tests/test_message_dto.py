"""Module that contains the tests for message_dto module"""

from __future__ import annotations

import unittest

import pydantic

from src.schemas.message_dto import (
    MessageDTO,
    get_filename_from_url,
    get_filename_from_base64,
    text_template,
    required_template,
    image_template,
    image_template_base64,
    video_template,
    video_template_base64,
    audio_template,
    document_template_base64_docx,
    document_template_base64_odt,
    document_template_base64_pdf,
    document_template_docx,
    document_template_odt,
    document_template_pdf
)

from src.utils import help_functions, file_examples, errors
from src.utils.type_aliases import (
    JsonDict,
    Phone,
    Base64,
    Base64Image,
    Base64Video,
    Base64Document,
    Base64Audio,
    MessageBody
)


def check_only_one_expected_exception(
    self: TestMessageDTO,
    request_body: JsonDict
):
    """Helper function that checks that the exception thrown
    at the time of setting incompatible values is the one I expect"""

    def func():
        MessageDTO(**request_body)

    exc = help_functions.get_exception(
        pydantic.ValidationError,
        func
    )

    list_errors_must_be = (
        errors.Error(
            "('__root__',)",
            str(errors.OnlyOneOfThemError(
                only_one=MessageDTO.incompatible_fields[0],
                values=tuple(
                    request_body.get(v)
                    for v in MessageDTO.incompatible_fields[0]
                )
            ))
        ),
    )

    self.assertTrue(exc)

    if exc:
        self.assertEqual(
            errors.ErrorFormatter.format_list_from_pydantic_errors(
                exc.errors()
            ),
            errors.ErrorFormatter.format_list(list_errors_must_be)
        )


class TestMessageDTO(unittest.TestCase):
    """Test class that contains tests for MessageDTO schema class"""

    def test_get_filename_from_url(self):
        """Test function that checks that the get_filename_from_url
        function returns the filename accordingly, and None if a filename
        could not be parsed"""

        filename = get_filename_from_url(
            "http://techslides.com/demos/sample-videos/sm%61ll.mp4"
        )

        self.assertEqual(filename, "small.mp4")

        filename = get_filename_from_url(
            "\
https://www.applecoredesigns.co.uk/wp-content/uploads/2018/08/button-ok.png"
        )

        self.assertEqual(filename, "button-ok.png")

        filename = get_filename_from_url("")

        self.assertEqual(filename, None)

        filename = get_filename_from_url("129igqrgf28g283d")

        self.assertEqual(filename, None)

    def test_get_filename_from_base64(self):
        """Test function that checks that the get_filename_from_base64
        function returns the filename accordingly, and None if a filename
        could not be parsed from the bad base64 string"""

        filename = get_filename_from_base64(
            file_examples.base64_audio
        )

        self.assertEqual(filename, "noname.oga")

        filename = get_filename_from_base64(
            file_examples.base64_image
        )

        self.assertEqual(filename, "noname.jpg")

        filename = get_filename_from_base64(
            file_examples.base64_video
        )

        self.assertEqual(filename, "noname.mp4")

        filename = get_filename_from_base64(
            f"asdaasd{file_examples.base64_video}"
        )

        self.assertIs(filename, None)

        no_mimetype = file_examples.base64_image[
            file_examples.base64_image.find(';'):
        ]

        with_fake_mimetype = f"data:image/ddddd{no_mimetype}"

        filename = get_filename_from_base64(with_fake_mimetype)

        self.assertIs(filename, None)

    def test_check_nulled_values(self):
        # pylint: disable=unnecessary-lambda

        """Test function that checks that the validators work properly
        at the time of sending data with some null values"""

        self.assertFalse(
            help_functions.get_exception(
                pydantic.ValidationError,
                lambda: MessageDTO(
                    **{
                        **required_template,
                        "text": "Hello!",
                        "image": None,
                        "video": None,
                        "audio": None,
                    }
                ),
            )
        )

        self.assertFalse(
            help_functions.get_exception(
                pydantic.ValidationError,
                lambda: MessageDTO(
                    **{
                        **required_template,
                        "text": None,
                        "image": "\
https://openclipart.org/image/800px/svg_to_png/199202/primary-button-ok.png",
                        "video": None,
                        "audio": None,
                    }
                ),
            )
        )

        self.assertFalse(
            help_functions.get_exception(
                pydantic.ValidationError,
                lambda: MessageDTO(
                    **{
                        **required_template,
                        "text": None,
                        "image": None,
                        "video": "\
https://openclipart.org/image/800px/svg_to_png/199202/primary-button-ok.png",
                        "audio": None,
                    }
                ),
            )
        )

        self.assertFalse(
            help_functions.get_exception(
                pydantic.ValidationError,
                lambda: MessageDTO(
                    **{
                        **required_template,
                        "text": None,
                        "image": None,
                        "video": None,
                        "audio": "\
https://openclipart.org/image/800px/svg_to_png/199202/primary-button-ok.png",
                    }
                ),
            )
        )

    def test_check_only_one(self):
        """Test function that checks that there's only one field set
        of the incompatible ones of MessageDTO"""

        for incompatible in MessageDTO.incompatible_fields:
            for field in incompatible:
                for field2 in incompatible:
                    if field2 == field:
                        continue

                    check_only_one_expected_exception(self, {
                        **required_template,
                        field: "\
https://openclipart.org/image/800px/svg_to_png/199202/primary-button-ok.png",
                        field2: "\
https://openclipart.org/image/800px/svg_to_png/199202/primary-button-ok.png"
                    })

    def test_check_at_least_one(self):
        """Test function that checks that there's at least one field set at the
        moment of passing data to MessageDTO"""

        exc = help_functions.get_exception(
            pydantic.ValidationError,
            lambda: MessageDTO(**required_template)
        )

        self.assertTrue(exc)
        self.assertEqual(
            errors.ErrorFormatter.format_list_from_pydantic_errors(
                exc.errors()
            ),
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('__root__',)",
                        errors.AtLeastOneOfThemError(
                            at_least=MessageDTO.at_least_fields,
                            values=tuple(
                                None
                                for _ in range(
                                    len(MessageDTO.at_least_fields)
                                )
                            )
                        )
                    )
                ]
            )
        )

    def test_filename(self):
        """Test function that checks that the filename validator raises
        an exception when expected and detects a filename properly"""

        def create_func(data):
            def _():
                inst = MessageDTO(**data)

                self.assertIsInstance(inst.filename, str)
                self.assertRegex(inst.filename, r"\w+\.\w+")

            return _

        no_exceptions_data = (
            image_template,
            image_template_base64,
            video_template,
            video_template_base64,
            document_template_docx,
            document_template_odt,
            document_template_pdf,
            document_template_base64_docx,
            document_template_base64_odt,
            document_template_base64_pdf
        )

        for data in no_exceptions_data:
            exc = help_functions.get_exception(
                pydantic.ValidationError,
                create_func(data)
            )

            self.assertIs(exc, None)

        # Creating bad assets to fire a filename error
        exceptions_data = (
            {**image_template, "image":
                f"{image_template['image']}/"},
            {**video_template, "video":
                f"{video_template['video']}/"},
            {**document_template_odt, "document": f"\
{document_template_odt['document']}/"},
            {**document_template_pdf, "document": f"\
{document_template_pdf['document']}/"},
            {**document_template_docx, "document": f"\
{document_template_docx['document']}/"},
            {**document_template_base64_docx, "document": f"""\
data:application/asd{
    document_template_base64_docx['document'][
        document_template_base64_docx['document'].find(';'):
    ]
}"""},
            {**document_template_base64_odt, "document": f"""\
data:application/asd{
    document_template_base64_odt['document'][
        document_template_base64_odt['document'].find(';'):
    ]
}"""},
            {**document_template_base64_pdf, "document": f"""\
data:application/asd{
    document_template_base64_pdf['document'][
        document_template_base64_pdf['document'].find(';'):
    ]
}"""},
            {**image_template_base64, "image": f"""\
data:image/asd{
    image_template_base64['image'][
        image_template_base64['image'].find(';'):
    ]
}"""},
            {**video_template_base64, "video": f"""\
data:video/asd{
    video_template_base64['video'][
        video_template_base64['video'].find(';'):
    ]
}"""},
        )

        for data in exceptions_data:
            exc = help_functions.get_exception(
                pydantic.ValidationError,
                create_func(data)
            )

            self.assertTrue(exc)
            self.assertEqual(
                errors.ErrorFormatter.format_list_from_pydantic_errors(
                    exc.errors()
                ),
                errors.ErrorFormatter.format_list(
                    [
                        errors.Error(
                            "('filename',)",
                            str(errors.BadFilenameNotRecognizedError)
                        )
                    ]
                )
            )

    def test_bad_phone(self):
        # pylint: disable=unnecessary-lambda

        """Test function that checks that validation works properly
        when provided a bad phone value"""

        exc = help_functions.get_exception(
            pydantic.ValidationError,
            lambda: MessageDTO(**{
                **text_template,
                "phone": ""
            })
        )

        self.assertTrue(exc)
        self.assertEqual(
            errors.ErrorFormatter.format_list_from_pydantic_errors(
                exc.errors()
            ),
            errors.ErrorFormatter.format_list(
                (
                    errors.Error(
                        "('phone',)",
                        # pylint: disable-next=c-extension-no-member
                        str(pydantic.errors.AnyStrMinLengthError(
                            limit_value=Phone.min_length
                        ))
                    ),
                )
            )
        )

        exc = help_functions.get_exception(
            pydantic.ValidationError,
            lambda: MessageDTO(**{
                **text_template,
                "phone": "d" * 10
            })
        )

        self.assertTrue(exc)
        self.assertEqual(
            errors.ErrorFormatter.format_list_from_pydantic_errors(
                exc.errors()
            ),
            errors.ErrorFormatter.format_list(
                (
                    errors.Error(
                        "('phone',)",
                        # pylint: disable-next=c-extension-no-member
                        str(pydantic.errors.StrRegexError(
                            pattern=Phone.regex.pattern
                        ))
                    ),
                )
            )
        )

        exc = help_functions.get_exception(
            pydantic.ValidationError,
            lambda: MessageDTO(**{
                **text_template,
                "phone": "1" * 14
            })
        )

        self.assertTrue(exc)
        self.assertEqual(
            errors.ErrorFormatter.format_list_from_pydantic_errors(
                exc.errors()
            ),
            errors.ErrorFormatter.format_list(
                (
                    errors.Error(
                        "('phone',)",
                        # pylint: disable-next=c-extension-no-member
                        str(pydantic.errors.AnyStrMaxLengthError(
                            limit_value=Phone.max_length
                        ))
                    ),
                )
            )
        )

        exc = help_functions.get_exception(
            pydantic.ValidationError,
            lambda: MessageDTO(**{
                **text_template,
                "phone": "1" * 8
            })
        )

        self.assertTrue(exc)
        self.assertEqual(
            errors.ErrorFormatter.format_list_from_pydantic_errors(
                exc.errors()
            ),
            errors.ErrorFormatter.format_list(
                (
                    errors.Error(
                        "('phone',)",
                        # pylint: disable-next=c-extension-no-member
                        str(pydantic.errors.AnyStrMinLengthError(
                            limit_value=Phone.min_length
                        ))
                    ),
                )
            )
        )

    def test_bad_image_bad_video_bad_document_bad_audio(self):
        """Test function that checks that validation works properly
        when provided a bad file value"""

        for test_data in (
            {
                "pattern_base64": Base64Image.regex.pattern,
                "field": "image",
                "template": image_template
            },
            {
                "pattern_base64": Base64Video.regex.pattern,
                "field": "video",
                "template": video_template
            },
            {
                "pattern_base64": Base64Document.regex.pattern,
                "field": "document",
                "template": document_template_docx
            },
            {
                "pattern_base64": Base64Audio.regex.pattern,
                "field": "audio",
                "template": audio_template
            },
        ):
            def get_schema_test_func(data: JsonDict):
                def func():
                    MessageDTO(**data)

                return func

            exc = help_functions.get_exception(
                pydantic.ValidationError,
                get_schema_test_func({
                    **test_data["template"],
                    test_data["field"]: ""
                })
            )

            self.assertTrue(exc)
            self.assertEqual(
                errors.ErrorFormatter.format_list_from_pydantic_errors(
                    exc.errors()
                ),
                errors.ErrorFormatter.format_list(
                    (
                        errors.Error(
                            f"('{test_data['field']}',)",
                            # pylint: disable-next=c-extension-no-member
                            str(pydantic.errors.AnyStrMinLengthError(
                                # pylint: disable-next=no-member
                                limit_value=pydantic.HttpUrl.min_length
                            ))
                        ),
                        errors.Error(
                            f"('{test_data['field']}',)",
                            # pylint: disable-next=c-extension-no-member
                            str(pydantic.errors.AnyStrMinLengthError(
                                # pylint: disable-next=no-member
                                limit_value=Base64.min_length
                            ))
                        ),
                    )
                )
            )

            exc = help_functions.get_exception(
                pydantic.ValidationError,
                get_schema_test_func({
                    **test_data["template"],
                    test_data["field"]: "asdasdasdasd"
                })
            )

            self.assertTrue(exc)
            self.assertEqual(
                errors.ErrorFormatter.format_list_from_pydantic_errors(
                    exc.errors()
                ),
                errors.ErrorFormatter.format_list(
                    (
                        errors.Error(
                            f"('{test_data['field']}',)",
                            # pylint: disable-next=c-extension-no-member
                            str(pydantic.errors.StrRegexError(
                                pattern=test_data["pattern_base64"]
                            ))
                        ),
                        errors.Error(
                            f"('{test_data['field']}',)",
                            # pylint: disable-next=c-extension-no-member
                            str(pydantic.errors.UrlSchemeError())
                        ),
                    )
                )
            )

            exc = help_functions.get_exception(
                pydantic.ValidationError,
                get_schema_test_func({
                    **test_data["template"],
                    test_data["field"]: "a" * 2084
                })
            )

            self.assertTrue(exc)
            self.assertEqual(
                errors.ErrorFormatter.format_list_from_pydantic_errors(
                    exc.errors()
                ),
                errors.ErrorFormatter.format_list(
                    (
                        errors.Error(
                            f"('{test_data['field']}',)",
                            # pylint: disable-next=c-extension-no-member
                            str(pydantic.errors.StrRegexError(
                                # pylint: disable-next=no-member
                                pattern=test_data["pattern_base64"]
                            ))
                        ),
                        errors.Error(
                            f"('{test_data['field']}',)",
                            # pylint: disable-next=c-extension-no-member
                            str(pydantic.errors.AnyStrMaxLengthError(
                                # pylint: disable-next=no-member
                                limit_value=pydantic.HttpUrl.max_length
                            ))
                        ),
                    )
                )
            )

    def test_bad_text(self):
        # pylint: disable=unnecessary-lambda

        """Test function that checks that validation works properly
        when provided a bad text value"""

        exc = help_functions.get_exception(
            pydantic.ValidationError,
            lambda: MessageDTO(**{
                **text_template,
                "text": ""
            })
        )

        self.assertTrue(exc)
        self.assertEqual(
            errors.ErrorFormatter.format_list_from_pydantic_errors(
                exc.errors()
            ),
            errors.ErrorFormatter.format_list(
                (
                    errors.Error(
                        "('text',)",
                        # pylint: disable-next=c-extension-no-member
                        str(pydantic.errors.AnyStrMinLengthError(
                            limit_value=MessageBody.min_length
                        ))
                    ),
                )
            )
        )

        exc = help_functions.get_exception(
            pydantic.ValidationError,
            lambda: MessageDTO(**{
                **text_template,
                "text": "a" * 20001
            })
        )

        self.assertTrue(exc)
        self.assertEqual(
            errors.ErrorFormatter.format_list_from_pydantic_errors(
                exc.errors()
            ),
            errors.ErrorFormatter.format_list(
                (
                    errors.Error(
                        "('text',)",
                        # pylint: disable-next=c-extension-no-member
                        str(pydantic.errors.AnyStrMaxLengthError(
                            limit_value=MessageBody.max_length
                        ))
                    ),
                )
            )
        )
