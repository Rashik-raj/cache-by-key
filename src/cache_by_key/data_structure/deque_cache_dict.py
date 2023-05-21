class DequeCacheDict(dict):
    """
    This dict obj automatically removes oldest data once it exceeds its size capacity to add new key value pair
    """

    def __init__(self, *args, max_size=0, **kwargs):
        self._max_size = max_size
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        """
        sets new value to a key and removes oldest key, value pair if it exceeds the max size allocated.
        :param key:
        :param value:
        :return:
        """
        dict.__setitem__(self, key, value)
        if len(self) > self._max_size:
            self.pop(next(iter(self)))
