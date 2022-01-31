"""Module that contains several examples of requests"""

from src.schemas import message_dto


examples_message_dto = {
    "text_message": {
        "summary": "A text message example",
        "description":
            "A text message is being sent with a valid phone number, a valid\
instance and a valid token",
        "value": message_dto.text_template,
    },
    "image_message": {
        "summary": "An image message example",
        "description":
            "An image message is being sent with a valid phone number, a valid\
instance and a valid token",
        "value": message_dto.image_template,
    },
    "video_message": {
        "summary": "A video message example",
        "description":
            "A video message is being sent with a valid phone number, a valid\
instance and a valid token",
        "value": message_dto.video_template,
    },
    "audio_message": {
        "summary": "An audio message example",
        "description":
            "An audio message is being sent with a valid phone number, a valid\
instance and a valid token",
        "value": message_dto.audio_template,
    },
    "document_docx_message": {
        "summary": "A docx document message example",
        "description":
            "A docx document message example is being sent with a valid phone\
number, a valid instance and a valid token",
        "value": message_dto.document_template_docx
    },
    "document_odt_message": {
        "summary": "An odt document message example",
        "description":
            "An odt document message example is being sent with a valid phone\
number, a valid instance and a valid token",
        "value": message_dto.document_template_odt
    },
    "document_pdf_message": {
        "summary": "A pdf document message example",
        "description":
            "A pdf document message example is being sent with a valid phone\
number, a valid instance and a valid token",
        "value": message_dto.document_template_pdf
    },
    "document_pdf_base64_message": {
        "summary": "A base-64 pdf document message example",
        "description":
            "A base-64 encoded pdf document message example is being sent with\
a valid phone number, a valid instance and a valid token",
        "value": message_dto.document_template_base64_pdf
    },
    "document_odt_base64_message": {
        "summary": "A base-64 odt document message example",
        "description":
            "A base-64 encoded odt document message example is being sent with\
a valid phone number, a valid instance and a valid token",
        "value": message_dto.document_template_base64_odt
    },
    "document_docx_base64_message": {
        "summary": "A base-64 docx document message example",
        "description":
            "A base-64 encoded docx document message example is being sent\
with a valid phone number, a valid instance and a valid token",
        "value": message_dto.document_template_base64_docx
    },
}
