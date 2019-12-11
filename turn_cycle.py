class TurnIterator:

    def __init__(self, collection, reverse=False):
        self._collection = list(collection)
        self._reverse = reverse
        self.position = -1 if reverse else 0

    def __next__(self):
        try:
            self.position += -1 if self._reverse else 1
            value = self._collection[self.position]
        except IndexError:
            self.position = -1 if self._reverse else 0
            value = self._collection[self.position]

        return value

    def reverse(self):
        self._reverse = not self._reverse

        return
