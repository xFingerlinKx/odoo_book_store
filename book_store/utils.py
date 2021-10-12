""" Helper and utilits methods for book_store module """

# 1 : imports of python lib
import re

# 2 :  imports of odoo
from odoo.exceptions import ValidationError

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
from . import constants


def check_is_isbn_valid(isbn):
    """
    Checks for ISBN-10 or ISBN-13 format
    :param isbn: {str} book ISBN number
    :raise: ValidationError if ISBN is not valid
    """
    regex = re.compile(constants.ISBN_REGEX_PATTERN)

    if not regex.search(isbn):
        raise ValidationError(constants.ISBN_INVALID_MSG.format(isbn=isbn))

    # Remove non ISBN digits, then split into a list
    chars = list(re.sub("[- ]|^ISBN(?:-1[03])?:?", "", isbn))
    # Remove the final ISBN digit from 'chars', and assign it to 'last'
    last = chars.pop()

    if len(chars) == 9:
        # Compute the ISBN-10 check digit
        val = sum((x + 2) * int(y) for x, y in enumerate(reversed(chars)))
        check = 11 - (val % 11)
        if check == 10:
            check = "X"
        elif check == 11:
            check = "0"
    else:
        # Compute the ISBN-13 check digit
        val = sum((x % 2 * 2 + 1) * int(y) for x, y in enumerate(chars))
        check = 10 - (val % 10)
        if check == 10:
            check = "0"

    if not str(check) == last:
        raise ValidationError(constants.ISBN_INVALID_MSG.format(isbn=isbn))
