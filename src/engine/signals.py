class Signal:
    def __init__(self):
        self._callbacks = []

    def connect(self, callback):
        if not callable(callback):
            raise TypeError("Callback must be callable")
        self._callbacks.append(callback)

    def disconnect(self, callback):
        try:
            self._callbacks.remove(callback)
        except ValueError:
            pass

    def emit(self, *args, **kwargs):
        for callback in list(self._callbacks):
            callback(*args, **kwargs)

    __call__ = emit
