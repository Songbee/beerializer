# Copied from the 'six' module.
def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    class metaclass(meta):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})


try:
    basestring
except NameError:
    basestring = str


class ValidationError(Exception):

    def __init__(self, errors):
        if isinstance(errors, basestring):
            errors = [errors]
        self.errors = errors
        super(ValidationError, self).__init__(str(self.errors))


class InvalidTypeValidationError(ValidationError):

    def __init__(self, field_name, expected, got):
        super(InvalidTypeValidationError, self).__init__(
            "{} must be a {}.  Got {}.".format(field_name, expected, got))


class BaseField(object):

    def __init__(self, name=None, required=False, allow_null=True, validators=None, hidden=False, readonly=False):
        self.name = name
        self.object_field_name = name
        self.required = required
        self.allow_null = allow_null
        self.parent = None
        self.validators = validators or []
        self.hidden = hidden
        self.readonly = readonly

    def clean(self, data):
        return data

    def base_clean(self, data):
        if data is None:
            if not self.allow_null:
                raise ValidationError(
                    "{}/{} cannot be null/None".format(self.name, self.object_field_name))
            return None
        data = self.clean(data)
        for validator in self.validators:
            validator.validate(self, data)
        return data

    def object_to_data(self, obj):
        return obj

    def base_object_to_data(self, obj):
        if obj is None:
            if not self.allow_null:
                raise ValidationError(
                    "{}/{} cannot be null/None".format(self.name, self.object_field_name))
            return None
        return self.object_to_data(obj)


class DefaultMeta(object):
    pass


class DefaultModel(object):
    pass


class SerializerMetaclass(type):

    def __new__(cls, name, bases, attrs):
        options = DefaultMeta

        if "Meta" in attrs:
            options = attrs.pop("Meta")

        fields = []
        for k, v in attrs.items():
            if isinstance(v, BaseField):
                if v.name is None:
                    v.name = k
                v.object_field_name = k
                fields.append(v)

        new_class_attrs = {k: v for k,
                           v in attrs.items() if not isinstance(v, BaseField)}
        new_class_attrs["fields"] = fields
        new_class_attrs["options"] = options
        ret = super(SerializerMetaclass, cls).__new__(
            cls, name, bases, new_class_attrs)
        for field in fields:
            field.parent = ret
        return ret


class BaseSerializer(object):
    fields = []
    options = None

    def __init__(self):
        pass

    @classmethod
    def load(self, data):
        model_class = getattr(self.options, "model", DefaultModel)
        model_class_args = getattr(self.options, "model_init_args", ())
        model_class_kwargs = getattr(self.options, "model_init_kwargs", {})

        obj = model_class(*model_class_args, **model_class_kwargs)
        self.update(data, obj)
        return obj

    @classmethod
    def update(self, data, obj):
        errors = []
        for field in self.fields:
            if field.required and field.name not in data:
                errors.append("Field {} is missing.".format(field.name))

            if field.readonly and field.name in data:
                errors.append("Field {} is read only.".format(field.name))

        if errors:
            raise ValidationError(errors)

        for field in self.fields:
            try:
                field_obj = field.base_clean(data[field.name])
            except ValidationError as ex:
                errors.extend(ex.errors)
            except KeyError:
                pass
            else:
                setattr(obj, field.object_field_name, field_obj)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def dump(self, obj):
        errors = []
        for field in self.fields:
            if field.required and not hasattr(self.object, field.object_field_name):
                errors.append("Field {} is missing from object.".format(
                    field.object_field_name))

        if errors:
            raise ValidationError(errors)

        data = {}
        for field in self.fields:
            if not field.hidden:
                try:
                    field_data = field.base_object_to_data(
                        getattr(obj, field.object_field_name))
                except ValidationError as ex:
                    errors.extend(ex.errors)
                else:
                    data[field.name] = field_data

        if errors:
            raise ValidationError(errors)

        return data


class Serializer(with_metaclass(SerializerMetaclass, BaseSerializer)):
    """
    Base class for a new serializer.
    """
    pass
