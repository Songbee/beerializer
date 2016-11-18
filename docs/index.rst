Beerializer
===========

Beerializer provides easy interface for transformation and validation of
Python objects into JSON-like dicts. It's easy and fun! See for
yourself:

.. code:: py

    class Simpson(object):
        def __init__(self):
            self.first_name = ""
            self.last_name = ""

        def __str__(self):
            return self.first_name + " " + self.last_name

    class SimpsonSerializer(Serializer):
        class Meta:
            model = Simpson

        first_name = fields.StringField(name="firstName")
        last_name = fields.StringField(name="lastName")

When you get a payload that requires one of these serializers, call
``Serializer.load(data)``:

.. code:: pycon

    >>> data = {"firstName": "Homer", "lastName": "Simpson"}
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
    >>> SimpsonSerializer.dump(homer)
    {'firstName': 'Homer', 'lastName': 'Simpson'}

User’s Guide
------------

.. toctree::
   :maxdepth: 2

   foreword
   install
   quickstart

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

