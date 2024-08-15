class PreventDuplicateMethod(object):
    def __init__(self, method):
        self.method = method
        self.previous_args = None
        self.previous_kwargs = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return lambda *args, **kwargs: self._execute_if_new(instance, *args, **kwargs)

    def _execute_if_new(self, instance, *args, **kwargs):
        if args == self.previous_args and kwargs == self.previous_kwargs:
            return
        result = self.method(instance, *args, **kwargs)
        self.previous_args = args
        self.previous_kwargs = kwargs
        return result
