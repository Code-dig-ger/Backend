from .exception import ValidationException
from . import validator_functions as validators


def isValidRequest(request, validation_dict):
    """
    :param request: Request Object 
    :param validation_dict: a dictionary of validators
    Dict[str(key), str(validation method)]
    Example : 
    {
        'page' : 'required|numeric',
        'per_page' : 'optional'
    }
    Format of validation method string - 
    optional/required (default: required) | functions 
    you can provide default value if optional   
    """

    param = request.query_params
    for key, val_method in validation_dict:

        methods = val_method.split('|')

        if key in param:
            for method in methods:
                param = getattr(validators, method)(param=param, key=key)

        elif 'required' in methods:
            raise ValidationException('{} is required', key)
