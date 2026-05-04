"""
Services for validating input.

Functions:
    parse_count: Parses and validates count.
"""


from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM


def parse_count(raw_count: str) -> int:
    """
    Parses and validates count from a raw string.

    :param str raw_count: The raw count.
    :return: The parsed and validated count.
    :rtype: int
    :raises ValueError: If the value is not a positive integer.
    """
    try:
        count = int(raw_count)
    except ValueError as e:
        raise ValueError(INPUT_INVALID_NUM) from e
    if count <= 0:
        raise ValueError(INPUT_GREATER_ZERO)
    return count
