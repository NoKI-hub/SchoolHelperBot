from pydantic import Field

import re


fullname_field = Field(min_length=6, max_length=120,)


def validate_fullname(fullname):
    names = fullname.split()
    if len(names) != 3:
        return False
    for name in names:
        if not re.match(r'[А-Яа-яЁёA-Za-z\-]+', name):
            return False
    return True
