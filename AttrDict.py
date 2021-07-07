class AttrDict(dict):
    """
    dict subclass which allows access to keys as attributes: mydict.myattr
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

