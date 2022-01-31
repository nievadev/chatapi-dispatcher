"""Module that contains several file examples for testing purposes"""

from pathlib import Path


with open(
    str(Path(__file__).parent / "example_base64_video"), "r", encoding="utf-8"
) as f:
    base64_video = f.read().strip()

with open(
    str(Path(__file__).parent / "example_base64_image"), "r", encoding="utf-8"
) as f:
    base64_image = f.read().strip()

with open(
    str(Path(__file__).parent / "example_base64_audio"), "r", encoding="utf-8"
) as f:
    base64_audio = f.read().strip()

with open(
    str(Path(__file__).parent / "example_base64_docx"), "r", encoding="utf-8"
) as f:
    base64_document_docx = f.read().strip()

with open(
    str(Path(__file__).parent / "example_base64_pdf"), "r", encoding="utf-8"
) as f:
    base64_document_pdf = f.read().strip()

with open(
    str(Path(__file__).parent / "example_base64_odt"), "r", encoding="utf-8"
) as f:
    base64_document_odt = f.read().strip()
