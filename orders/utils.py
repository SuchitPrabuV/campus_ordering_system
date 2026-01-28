import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def create_qr_image(token):
    qr = qrcode.make(str(token))
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()
