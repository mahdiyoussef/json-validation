# JSON Validation (Python)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/mahdiyoussef/json-validation.svg)](https://github.com/mahdiyoussef/json-validation/issues)
[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)

A light-weight Python library inspired by JavaScript's `joi` for validating JSON-like dictionaries. Cleanly define schema rules to enforce data integrity, typing, minimum/maximum lengths, regex patterns, and cross-field conditions.

## Features

- **Chainable Object Construction**: Easily construct schema constraints using `joiobject`.
- **Type Validation**: Strings, Integers, Floats, Booleans, Datetimes.
- **Value Constraints**: `min`, `max`, `minlength`, `maxlength`.
- **String Formats**: Validate using `regex`, string-based `date` parsing formats.
- **Cross-field Logic**: Define relationships between JSON keys such as `xor` (only one exists), `and_` (all exist), `gt` (greater than), `lt` (less than), `geq` (greater or equal), and `leq` (less or equal).

## Installation

Simply clone this repository or drop `joi.py` and `joiobject.py` into your Python project.

## Usage

### 1. Build a Schema Object

Use `joiobject` to chain properties and build the rule definitions.

```python
from joiobject import joiobject
from joi import joi

# Define field rules using chainable methods
username_schema = joiobject().string().required().minlength(3).maxlength(20).get()
age_schema = joiobject().integer().required().min(18).max(99).get()

# Compile the base validation rules
schema = {
    "username": username_schema,
    "age": age_schema
}

# Initialize the validator
validator = joi(schema)
```

### 2. Validate Data

```python
test_data = {
    "username": "john_doe",
    "age": 25
}

# Run the validation
result = validator.validate(test_data)

if result["accepted"]:
    print("Validation passed!")
else:
    print("Errors:", result["wrong_field"])
    print("Missing:", result["missing_fields"])
```

### 3. Cross-Field Conditions

You can enforce constraints where fields depend on each other:

```python
validator = joi(schema)

# Either 'email' or 'phone_number' must be provided, but not both at once.
validator.xor("email", "phone_number")

# 'password' and 'confirm_password' must be submitted together
validator.and_("password", "confirm_password")

# Enforce that 'end_date' is greater than 'start_date'
validator.gt("end_date", "start_date")
```
