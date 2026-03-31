from datetime import datetime

class joiobject:
    """
    A builder pattern class used to construct validation schemas.
    Each method returns the instance so they can be chained easily.
    """

    def __init__(self):
        """Initializes a new empty validation schema object."""
        self.object = {}

    def string(self):
        """Sets the type constraint to string."""
        self.object['type'] = str
        return self

    def integer(self):
        """Sets the type constraint to integer."""
        self.object['type'] = int
        return self

    def float(self):
        """Sets the type constraint to float."""
        self.object['type'] = float
        return self

    def boolean(self):
        """Sets the type constraint to boolean."""
        self.object['type'] = bool
        return self

    def datetime(self):
        """Sets the type constraint to datetime."""
        self.object['type'] = datetime
        return self

    def type(self, value):
        """Sets a custom type constraint."""
        self.object['type'] = value
        return self

    def required(self):
        """Marks the field as required in the validation schema."""
        self.object['required'] = True
        return self

    def optional(self):
        """Marks the field as optional in the validation schema."""
        self.object['required'] = False
        return self

    def min(self, value):
        """Sets the minimum value (for numbers) or minimum date (for datetimes)."""
        self.object['min'] = value
        return self

    def max(self, value):
        """Sets the maximum value (for numbers) or maximum date (for datetimes)."""
        self.object['max'] = value
        return self

    def format(self, value):
        """Sets a format constraint (e.g. 'date')."""
        self.object['format'] = value
        return self

    def dateformat(self, value):
        """Sets a specific datetime parsing format like '%Y-%m-%d'."""
        self.object['dateformat'] = value
        return self

    def get(self):
        """Returns the compiled dictionary ruleset."""
        return self.object

    def maxlength(self, value):
        """Sets the maximum length for a string."""
        self.object['maxlength'] = value
        return self

    def minlength(self, value):
        """Sets the minimum length for a string."""
        self.object['minlength'] = value
        return self
