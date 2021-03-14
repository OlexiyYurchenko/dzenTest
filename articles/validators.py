def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.gif', '.jpg', '.png', '.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

    if ext.lower() == '.txt' and value.size > 102400:
        raise ValidationError('The file is too large. Maximum file size 100kB')


def validate_text_extension(value):
    import re
    from django.core.exceptions import ValidationError
    matched = bool(re.match("<\/?((?!(a|code|i|strong)\b)\w*)\/?>", value))

    if matched:
        raise ValidationError('You cannot use prohibited tags')