from django.core.exceptions import ValidationError


def email_validator(value):
    if '@' in value:
        return value
    else:
        raise ValidationError('please enter a correct email address')

def school_email_validator(value):
    if 'end' in value:
        return value
    else:
        raise ValidationError('please use school email address')