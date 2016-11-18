Beerializer
===========

|Documentation Status|

A fork of awesome `R2DTO <https://github.com/nickswebsite/r2dto>`__ by
@nickswebsite.

Provides easy interface for transformation and validation of arbitrary
python objects into DTOs suitable for receiving from and delivering to
other services.

Quick Start
-----------

Let's start by creating a simple model class:

.. code:: python

    class Simpson(object):
        def __init__(self):
            self.first_name = ""
            self.last_name = ""

        def __str__(self):
            return self.first_name + " " + self.last_name

To create a serializer, we need to map attributes to fields of our DTO:

.. code:: python

    class SimpsonSerializer(Serializer):
        class Meta:
            model = Simpson

        first_name = fields.StringField(name="firstName")
        last_name = fields.StringField(name="lastName")

When you get a payload that requires one of these serializers, call
``Serializer.load(data)``.

.. code:: pycon

    >>> data = {
    ...     "firstName": "Homer",
    ...     "lastName": "Simpson",
    ... }
    >>> s = SimpsonSerializer.load(data)
    >>> s
    <class '__main__.Simpson'>
    >>> str(s)
    'Homer Simpson'

To go the other way. Pass the object you want to transfer into the
``dump`` method:

.. code:: pycon

    >>> homer = Simpson()
    >>> homer.first_name = "Homer"
    >>> homer.last_name = "Simpson"
    >>> s = SimpsonSerializer.dump(homer)
    >>> s
    {'firstName': 'Homer', 'lastName': 'Simpson'}

.. |Documentation Status| image:: https://readthedocs.org/projects/beerializer/badge/?version=latest
   :target: http://beerializer.readthedocs.io/en/latest/?badge=latest
