import re
from datetime import datetime

class joi:
    """
    Main validator class for JSON schemas.
    Evaluates form data against defined criteria, type constraints, and relationships.
    """
    __xor_conditions = []
    __and_conditions = []
    __gt_conditions = []
    __lt_conditions = []
    __geq_conditions = []
    __leq_conditions = []

    def __init__(self, joi):
        """
        Initializes the joi validator.
        :param joi: A dictionary schema built using joiobject().
        """
        self.joi = joi

    def get_joi(self):
        """Returns the base validation schema."""
        return self.joi

    def get_keys(self):
        """Returns all keys expected in the base schema."""
        return [i for i in self.joi.keys()]

    def xor(self, *args):
        """
        Exclusive OR condition. 
        Only one of the provided field names must exist in the object payload.
        """
        self.__xor_conditions.append(args)
        return self

    def and_(self, *args):
        """
        AND condition.
        All fields mentioned in the arguments must exist simultaneously.
        """
        self.__and_conditions.append(args)
        return self

    def gt(self, gt, lw):
        """
        Greater-than condition across two fields.
        :param gt: Field name that should have the greater value.
        :param lw: Field name that should have the smaller value.
        """
        self.__gt_conditions.append([gt, lw])
        return self

    def lt(self, lt, gt):
        """
        Less-than condition across two fields.
        :param lt: Field name that should have the smaller value.
        :param gt: Field name that should have the greater value.
        """
        self.__lt_conditions.append([lt, gt])
        return self

    def geq(self, gt, lw):
        """
        Greater-than-or-equal condition across two fields.
        :param gt: Field name that has the larger/equal value.
        :param lw: Field name that has the smaller/equal value.
        """
        self.__geq_conditions.append([gt, lw])
        return self

    def leq(self, lw, gt):
        """
        Less-than-or-equal condition across two fields.
        :param lw: Field name with the smaller/equal value.
        :param gt: Field name with the larger/equal value.
        """
        self.__leq_conditions.append([lw, gt])
        return self

    def __isgt(self, value1, value2):
        value1object = self.joi[value1]
        value2object = self.joi[value2]

        if value1object.get("format", False) == "date" and value2object.get("format", False) == "date":
            date1 = datetime.strptime(value1, value1object["dateformat"])
            date2 = datetime.strptime(value2, value2object["dateformat"])
            return date1 > date2
        else:
            return value1 > value2

    def __is_lt(self, value1, value2):
        return value1 < value2

    def __is_geq(self, value1, value2):
        return value1 >= value2

    def __is_leq(self, value1, value2):
        return value1 <= value2

    def __check_string_properties(self, form, key, form_keys) -> bool:
        field_keys = [i for i in self.joi[key].keys()]
        properties_exists = "minlength" in field_keys or "maxlength" in field_keys
        return (key in form_keys and isinstance(form[key], self.joi[key]["type"])
                and type(form[key]) in [str] and properties_exists)

    def __check_max_and_min_for_numbers(self, form, key, form_keys) -> bool:
        field_keys = [i for i in self.joi[key].keys()]
        max_or_min_exists = "min" in field_keys or "max" in field_keys
        return (key in form_keys and isinstance(form[key], self.joi[key]["type"])
                and type(form[key]) in [int, float] and max_or_min_exists)

    def __check_regex(self, form, key, form_keys) -> bool:
        field_keys = [i for i in self.joi[key].keys()]
        is_regex_exists = "regex" in field_keys
        return (key in form_keys and isinstance(form[key], self.joi[key]["type"])
                and type(form[key]) in [str] and is_regex_exists)

    def __check_date(self, form, key, form_keys) -> bool:
        field_keys = [i for i in self.joi[key].keys()]
        is_date_format = "format" in field_keys and "dateformat" in field_keys and self.joi[key]["format"] == "date"
        return (key in form_keys and isinstance(form[key], self.joi[key]["type"])
                and type(form[key]) in [str] and is_date_format)

    def validate(self, form):
        """
        Validates the given dictionary payload against the compiled rules.
        :param form: Dictionary of values to validate.
        :return: A dictionary payload with validation status, missing fields, and error details.
        """
        missing_fields = []
        wrong_field = []
        base_form_keys = self.get_keys()
        form_keys = [i for i in form.keys()]
        for key in base_form_keys:
            if key in form_keys and not isinstance(form[key], self.joi[key]["type"]):
                wrong_field.append({ f"{key}": { "message": "wrong type" } })
            elif self.__check_max_and_min_for_numbers(form, key, form_keys):
                field_keys = [i for i in self.joi[key].keys()]
                if "max" in field_keys and form[key] > self.joi[key]["max"]:
                    wrong_field.append({ f"{key}": { "message": "wrong filed , the value is bigger than maximum" } })
                elif "min" in field_keys and form[key] < self.joi[key]["min"]:
                    wrong_field.append({ f"{key}": { "message": "wrong filed , the value is smaller than minimum" } })
            elif self.__check_regex(form, key, form_keys):
                regexp = self.joi[key]["regex"]
                result_regex = re.match(regexp, form[key])
                if not result_regex:
                    wrong_field.append({ f"{key}": { "message": f"{key} is not a correct format" } })
            elif self.__check_string_properties(form, key, form_keys):
                field_keys = [i for i in self.joi[key].keys()]
                if "maxlength" in field_keys and len(form[key]) > self.joi[key]["maxlength"]:
                    wrong_field.append({ f"{key}": { "message": f"{key} is too long" } })
                elif "minlength" in field_keys and len(form[key]) < self.joi[key]["minlength"]:
                    wrong_field.append({ f"{key}": { "message": f"{key} is too short" } })

            elif self.__check_date(form, key, form_keys):
                field_keys = [i for i in self.joi[key].keys()]
                date = None
                try:
                    date = datetime.strptime(form[key], self.joi[key]["dateformat"])
                except Exception as e:
                    wrong_field.append({ f"{key}": { "message": f"{key} is not a correct format" } })

                if date is not None and "min" in field_keys and isinstance(self.joi[key]["min"], datetime) and date < self.joi[key]["min"]:
                    wrong_field.append({ f"{key}": { "message": f"{key} is lower than the minimum" } })
                if date is not None and "max" in field_keys and isinstance(self.joi[key]["max"], datetime) and date > self.joi[key]["max"]:
                    wrong_field.append({ f"{key}": { "message": f"{key} is higher than the maximum" } })

            elif self.joi[key].get("required", False) and key not in form_keys:
                missing_fields.append({ f"{key}": { "message": "missing required field" } })

        for key in form_keys:
            if key not in base_form_keys:
                wrong_field.append({ f"{key}": { "message": "wrong key" } })

        for i in self.__and_conditions:
            missing_and_fields_number = 0
            for j in i:
                if j not in form_keys:
                    missing_and_fields_number += 1
            if missing_and_fields_number > 0:
                missing_fields.append({ f"{str(i)}": { "message": "missing fields, should all of them exists" } })

        for i in self.__xor_conditions:
            number_of_existing_fields = 0
            for j in i:
                if j in form_keys:
                    number_of_existing_fields += 1
            if number_of_existing_fields == 0 or number_of_existing_fields > 1:
                wrong_field.append({ f"{str(i)}": { "message": "wrong xo condition, must one of them exists" } })

        for i in self.__gt_conditions:
            if not self.__isgt(form[i[0]], form[i[1]]):
                wrong_field.append({ f"gt:{str(i)}": { "message": f"{i[0]} must be $gt than {i[1]}" } })
        for i in self.__leq_conditions:
            if not self.__is_lt(form[i[0]], form[i[1]]):
                wrong_field.append({ f"leq:{str(i)}": { "message": f"{i[0]} must be $leq than {i[1]}" } })
        for i in self.__geq_conditions:
            if not self.__is_geq(form[i[0]], form[i[1]]):
                wrong_field.append({ f"geq:{str(i)}": { "message": f"{i[0]} must be $geq than {i[1]}" } })
        for i in self.__leq_conditions:
            if not self.__is_leq(form[i[0]], form[i[1]]):
                wrong_field.append({ f"leq:{str(i)}": { "message": f"{i[0]} must be $leq than {i[1]}" } })

        form_accepted = (len(missing_fields) == 0 and len(wrong_field) == 0)
        return dict(accepted=form_accepted, missing_fields=missing_fields, wrong_field=wrong_field)
