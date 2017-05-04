from .base import ValidationError

try:
    import jsonschema
except ImportError:
    jsonschema = None


class EnumValidator(object):

    def __init__(self, *choices):
        self.choices = choices

    def validate(self, field, data):
        if data not in self.choices:
            raise ValidationError("{} must be one of {}.  Got {}.".format(
                field.name, self.choices, data))


class JSONSchemaValidator:
    def __init__(self, schema):
        if jsonschema is None:
            raise EnvironmentError("jsonschema must be installed for "
                                   "JSONSchemaValidator to work. "
                                   "(pip install jsonschema)")
        self.schema = schema

    def validate(self, field, data):
        try:
            jsonschema.validate(data, self.schema)
        except jsonschema.ValidationError as je:
            raise ValidationError(je.message) from je