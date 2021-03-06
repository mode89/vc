class Grid:

    def __init__(self, params_dict):
        self.params_dict = params_dict

    def __iter__(self):
        return Grid.Iterator(self.params_dict)

    class Iterator:

        def __init__(self, params_dict):
            self.params_dict = params_dict
            self.params = dict()
            for key in self.params_dict:
                self.params[key] = self.params_dict[key][0]

        def __iter__(self):
            return self

        def __next__(self):
            if self.params is None:
                raise StopIteration()

            retval = self.params.copy()

            increment = True
            for key in self.params_dict.keys():
                if increment:
                    values = self.params_dict[key]
                    index = values.index(self.params[key])
                    if index == len(values) - 1:
                        self.params[key] = values[0]
                        increment = True
                    else:
                        self.params[key] = values[index + 1]
                        increment = False

            if increment:
                self.params = None

            return retval

        # Python 2.7 uses next() instead of __next__()
        def next(self):
            return self.__next__()
