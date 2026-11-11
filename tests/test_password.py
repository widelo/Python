"""Regression tests for the alternative password generator."""

from collections import Counter

import pytest

from other.password import alternative_password_generator


@pytest.mark.parametrize(
    ("chars_incl", "length"),
    [
        ("abcdefgh", 5),
        ("abcd", 3),
        ("abcde", 3),
        ("a", 0),
        ("", -1),
        ("abc", -1),
    ],
)
def test_alternative_password_generator_rejects_impossible_length(
    chars_incl: str, length: int
) -> None:
    """Reject requests that cannot contain every required character."""
    with pytest.raises(ValueError, match=r"^Password length must be at least"):
        alternative_password_generator(chars_incl, length)


@pytest.mark.parametrize(
    ("chars_incl", "length"),
    [
        ("", 0),
        ("", 1),
        ("", 2),
        ("", 8),
        ("a", 1),
        ("aab!", 4),
        ("aab!", 5),
        ("aab!", 6),
        ("aab!", 7),
        ("aab!", 8),
        ("aab!", 9),
    ],
)
def test_alternative_password_generator_preserves_length_and_required_characters(
    chars_incl: str, length: int
) -> None:
    """Preserve the requested length and required character multiplicities."""
    password = alternative_password_generator(chars_incl, length)

    assert len(password) == length
    assert not Counter(chars_incl) - Counter(password)
