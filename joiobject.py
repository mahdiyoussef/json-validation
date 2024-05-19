
class joiobject:

    def __init__(self):
        self.object = {}

    def string(self):
        self.object['type'] = str
        return self

    def integer(self):
        self.object['type'] = int
        return self

    def float(self):
        self.object['type'] = float
        return self

    def boolean(self):
        self.object['type'] = bool

    def datetime(self):
        self.object['type'] = datetime
        return self

    def type(self, value):
        self.object['type'] = value
        return self

    def required(self):
        self.object['required'] = True
        return self

    def optional(self):
        self.object['required'] = False
        return self

    def min(self, value):
        self.object['min'] = value
        return self

    def max(self, value):
        self.object['max'] = value
        return self

    def format(self, value):
        self.object['format'] = value
        return self

    def dateformat(self, value):
        self.object['dateformat'] = value
        return self

    def get(self):
        return self.object

    def maxlength(self, value):
        self.object['maxlength'] = value
        return self

    def minlength(self, value):
        self.object['minlength'] = value
        return self
