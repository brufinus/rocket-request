"""
Services for validating input.

Functions:
    parse_silo_count: Parses and validates the silo count.
"""


from data.constants import INPUT_GREATER_ZERO, INPUT_INVALID_NUM


def parse_silo_count(raw_count: str) -> int:
    """
    Parses and validates silo count from a raw string.

    :param str raw_count: The silo count.
    :return: Parsed, validated silo count or -1 if invalid.
    :rtype: int
    :raises ValueError: If the value is not a positive integer.
    """
    try:
        num_silos = int(raw_count)
    except ValueError as e:
        raise ValueError(INPUT_INVALID_NUM) from e
    if num_silos <= 0:
        raise ValueError(INPUT_GREATER_ZERO)
    return num_silos
