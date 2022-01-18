from utils.exception import ValidationException


def numeric(param, key, *args, **kwargs):
    if not param[key].isnumeric():
        raise ValidationException('{} must be numeric'.format(key))
    return param


def alphanumeric(param, key, *args, **kwargs):
    if not param[key].isalnum():
        raise ValidationException(
            '{} can only contain alphabet or digit'.format(key))
    return param


def required(param, *args, **kwargs):
    return param


def optional(param, *args, **kwargs):
    return param
