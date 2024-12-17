import weakref

class ValidatedProperty:
    def __init__(self, validator):
        self.validator = validator
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        instance.__dict__[self.name] = value

class UserProfileManager:
    username = ValidatedProperty(lambda x: isinstance(x, str) and len(x) > 0)
    email = ValidatedProperty(lambda x: "@" in x and "." in x)

    _cache = weakref.WeakValueDictionary()

    def __init__(self):
        self.last_login = None

    @classmethod
    def add_to_cache(cls, manager):
        cls._cache[id(manager)] = manager

    @classmethod
    def get_from_cache(cls, user_id):
        return cls._cache.get(user_id)

    def set_last_login(self, value):
        self.last_login = value

    def get_last_login(self):
        return self.last_login