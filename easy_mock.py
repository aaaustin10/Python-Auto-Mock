import types, re

class easy_mock(object):
    locked = False
    def __init__(self, name):
        self.name = name

    def __getattr__(self, attr):
        if easy_mock.locked:
            raise Exception('Attribute "%s" of "%s" used and not defined before lock.' % (attr, self.name))
        e_mock = easy_mock(attr)
        setattr(self, attr, e_mock)
        return e_mock

    def __setattr__(self, name, value):
        if easy_mock.locked:
            raise Exception('Attribute "%s" of "%s" modified after lock.' % (name, self.name))
        self.__dict__[name] = value

    def __getitem__(self, item):
        return None

class easy_func_mock(easy_mock):
    __call__ = lambda self, *args, **kwargs: self.callee(*args, **kwargs)
    def callee(self, *args, **kwargs):
        raise Exception('Function "%s" called without being mocked.' % self.name)

    def set_callee(self, function):
        self.callee = function

class full_mock(object):
    def __init__(self, module_name, function_name, stubs, init_args=[], init_kwargs={}, keepers=None):
        # subclasses haven't been addressed yet
        # as the need hasn't been seen
        # should work so long as you don't need to initialize the subclass with different
        # info than you are using with the parent

        # mocking the dunder items is both going down the rabbit hole and not a likely use case
        keepers = keepers or "__.*__"
        self.unit_names = function_name.split('.')
        self.module = __import__(module_name, fromlist=[self.unit_names[0]])

        self.preserved_unit_list = []
        unit = self.module
        self.old_values = {'module' : {}}
        curr_old_value_node = self.old_values['module']
        for i, name in enumerate(self.unit_names):
            preserved_unit = getattr(unit, name)
            self.preserved_unit_list.append(preserved_unit)
            if isinstance(preserved_unit, (type, types.ClassType)):
                instance = preserved_unit(*init_args, **init_kwargs)
                preserved_unit = instance
            things_to_mock = [item for item in dir(unit) if not re.match(keepers, item)]
            for item_name in things_to_mock:
                is_callable = callable(getattr(unit, item_name))
                curr_old_value_node[item_name] = getattr(unit, item_name)
                new_value = easy_func_mock(item_name) if is_callable else easy_mock(item_name)
                if item_name != name:
                    setattr(unit, item_name, stubs.get(item_name, new_value))
            stubs = stubs.get(self.unit_names[i], {})
            curr_old_value_node[name] = {}
            curr_old_value_node = curr_old_value_node[name]
            unit = preserved_unit
        self.non_stubbed_item = unit

    def __enter__(self):
        easy_mock.locked = True
        return self.non_stubbed_item

    def __exit__(self, exception_type, exception_value, traceback):
        def reconstruct(unit_names, old_value_node, attr):
            if len(unit_names) == 0:
                return
            for name, val in old_value_node.iteritems():
                setattr(attr, name, val)
            # unbinding the method if necessary
            if getattr(self.preserved_unit_list[0], '__self__', None):
                setattr(attr, unit_names[0], self.preserved_unit_list[0].__func__)
            else:
                setattr(attr, unit_names[0], self.preserved_unit_list[0])
            self.preserved_unit_list = self.preserved_unit_list[1:]
            reconstruct(unit_names[1:], old_value_node[unit_names[0]], getattr(attr, unit_names[0]))

        reconstruct(self.unit_names, self.old_values['module'], self.module)
        easy_mock.locked = False
