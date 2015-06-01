Python Auto Mock
================
``auto_mock`` is a module for mocking during unit testing.
It automatically replaces all variables and functions external to the unit with default values to help developers exclude external state in their unit tests.

Installation
------------
``pip install python-auto-mock``

Usage
-----

In the example we will be making use of myclass.py

``myclass.py``

.. code:: python

    X = 1
    Y = 2
    Z = 3

    class MyClass():
        def addition_with_globals(self):
            print(X)
            print(Y)
            print(X + Y)
            return X + Y

To test this class we will write a test script.

.. code:: python

    import auto_mock

    def test_my_class_addition():
        stubs = {
            'X' : 36,
            'Y' : 35,
        }

        with auto_mock.full_mock('myclass', 'MyClass.addition_with_globals', stubs) as addition_with_globals:
            if addition_with_globals() != 71:
                print("Addition is broken")

    def main():
        test_my_class_addition()

    main()

Done correctly this should print out

::

    36
    35
    71

``full_mock`` takes 3 non optional arguments.

1. The module name where the code is located.
2. The specific function or method that is being tested.
3. The dictionary of stubs/mocks that you would like to override the values with.

The stubs variable contains the names of the variables that are being mocked.
In this example we have ``X``, ``Y``, and ``Z`` as global variables.
We only use ``X`` and ``Y`` in this example, so they are the only variables that are in the stubs dictionary.

``full_mock`` returns the function or method that you are trying to test with the external variables mocked.
If the variable is not within the stubs then it is mocked with a default object.
Inside the with block you can test that the function does what it is supposed to do.
