from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']

    if ext not in valid_extensions:
        raise ValidationError(
            'Unsupported file extension. Allowed extensions: ' + ', '.join(valid_extensions)
        )
