Quickstart
==========

A simple serializer
-------------------

Let's start by creating a simple model class::

    class Simpson(object):
        def __init__(self):
            self.first_name = ""
            self.last_name = ""

        def __str__(self):
            return self.first_name + " " + self.last_name

To create a serializer, we need to map model attributes to fields of
the resulting DTO::

    from beerializer import Serializer, fields

    class SimpsonSerializer(Serializer):
        class Meta:
            model = Simpson

        first_name = fields.StringField(name="firstName")
        last_name = fields.StringField(name="lastName")

When you get a payload that requires one of these serializers, call
``Serializer.load(data)``::

    >>> data = {
    ...     "firstName": "Homer",
    ...     "lastName": "Simpson",
    ... }
    >>> s = SimpsonSerializer.load(data)
    >>> s
    <__main__.Simpson object at ...>
    >>> str(s)
    'Homer Simpson'

To go the other way. Pass the object you want to transfer into the
``dump`` method::

    >>> homer = Simpson()
    >>> homer.first_name = "Homer"
    >>> homer.last_name = "Simpson"
    >>> SimpsonSerializer.dump(homer)
    {'firstName': 'Homer', 'lastName': 'Simpson'}

Readonly and hidden fields
--------------------------

To hide a field from output, use keyword ``hidden``::

    >>> class BartSerializer(Serializer):
    ...     grade = fields.StringField(hidden=True)
    ...
    >>> o = BartSerializer.load({"grade": "C"})
    >>> o.grade
    'C'
    >>> BartSerializer.dump(o)
    {}

To make a field readonly, use... well, you guessed it::

    >>> class NewBartSerializer(Serializer):
    ...     grade = fields.StringField(readonly=True)
    ...
    >>> NewBartSerializer.load({"grade": "C"})
    Traceback (most recent call last):
      [...]
    beerializer.base.ValidationError: ['Field grade is read only.']

SQLAlchemy
----------

SQLAlchemy support comes in an additional package:

.. code:: bash

    pip install beerializer-sqlalchemy

Now you only need to specify model on a serializer::

    >>> from beerializer_sqlalchemy import ModelSerializer
    >>> from .models import User
    >>> class UserSerializer(ModelSerializer):
    ...     class Meta:
    ...         model = User
    ...
    >>> homer = User.query.get(1)
    >>> UserSerializer.dump(homer)
    {'id': 1, 'first_name': 'Homer', 'last_name': 'Simpson', ...}

You can specify which fields to dump by specifying ``Meta.fields``::

    >>> class MiniUserSerializer(ModelSerializer):
    ...     class Meta:
    ...         model = User
    ...         fields = ["last_name"]
    ...
    >>> MiniUserSerializer.dump(homer)
    {'last_name': 'Simpson'}

To override any options for a field or if its type can't be guessed,
just add it as you would usually do::

    >>> from lazy_serializer.contrib.sqlalchemy import ModelSerializer
    >>> class StrangeUserSerializer(ModelSerializer):
    ...     first_name = fields.StringField(name="firstName")
    ...     class Meta:
    ...         model = User
    ...
    >>> StrangeUserSerializer.dump(homer)
    {'id': 1, 'firstName': 'Camel', 'last_name': 'Snake', ...}

Fields
------

To implement your own fields, derive from ``Field`` and implement
``clean`` and ``object_to_data``. ``ValidationError`` should be thrown
if the data is bad.

::

    import uuid
    class UUIDField(fields.Field):
        def clean(self, data):
            try:
                return uuid.UUID(data)
            except ValueError:
                raise ValidationError("{} is required to conform to the canonical UUID.".format(self.name))

        def object_to_data(self, obj):
            return str(obj)

When you go to create your serializer, just use the field as you would
any other field.

::

    >>> class BartSerializer(Serializer):
    ...     uuid = UUIDField()
    ...
    >>> s = BartSerializer()
    >>> s.validate({"uuid": "01234567-89ab-cdef-0123-456789abcdef"})
    <object ...>
    >>> _.uuid
    UUID('01234567-89ab-cdef-0123-456789abcdef')

Validators
----------

You can specify custom validators for individual fields. These are just
objects with a 'validate' method that accepts the field and the data as
parameters. ValidationError should be raised if there is a problem with
validation.

::

    class EnumValidator(object):
        def __init__(self, *choices):
            self.choices = choices

        def validate(self, field, data):
            if data not in self.choices:
                raise ValidationError(
                    "{} must be one of {}. Got {}."
                        .format(field.name, self.choices, data))

Use the 'validators' key word argument to use the validator with a
particular field.

::

    >>> class LisaSerializer(Serializer):
    ...     grade = fields.StringField(validators=[EnumValidator("A+", "A")])
    ...
    >>> lisa = LisaSerializer.load({"grade": "A+"})
    >>> lisa.grade
    'A+'

    >>> try:
    ...     lisa = LisaSerializer.load({"grade": "A-"})
    ... except ValidationError as ex:
    ...     print("Validation failed:")
    ...     print(ex.errors)
    Validation failed:
    ["grade must be one of ('A+', 'A').  Got A-."]

