# -*- coding: utf-8 -*-
""" CONSTANTS FOR BOOK_STORE MODULE """

#########################################################################
# Authors
#########################################################################

NO_AUTHORS_SELECTED_MESSAGE = "No author selected!"
""" If no author selected for the book message """

#########################################################################
# Check ISBN
#########################################################################

ISBN_REGEX_PATTERN = "^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=" \
                     "(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$"
""" Checks for ISBN-10 or ISBN-13 format regex pattern """

ISBN_INVALID_MSG = "Invalid ISBN: {isbn}.\nPlease, check digits!"
""" ISBN is not valid message """

ISBN_IS_NOT_UNIQUE_MSG = "ISBN is not unique!"
""" ISBN is not unique message """

#########################################################################
# Check the book number of pages
#########################################################################

PAGE_QTY_BELLOW_ZERO_MSG = "The number of pages must be greater than 0!"
""" ISBN is not valid message """

#########################################################################
# Partner types (Author or Publisher)
#########################################################################

RES_PARTNER_AUTHOR = 'is_author'
""" Partner is Author """
RES_PARTNER_PUBLISHER = 'is_publisher'
""" Partner is Publisher """

RES_PARTNER_TYPES = [
    (RES_PARTNER_AUTHOR, 'Author'),
    (RES_PARTNER_PUBLISHER, 'Publisher'),
]
""" Partner types dictionary """

#########################################################################
# Book cover sizes
#########################################################################

BOOK_COVER_SIZE_SMALL = 'small'
BOOK_COVER_SIZE_MEDIUM = 'medium'
BOOK_COVER_SIZE_LARGE = 'large'

#########################################################################
#
#########################################################################
