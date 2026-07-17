from __future__ import annotations

import pytest
from eventbroker.topic import Topic
def test_topic_segments() -> None:
    t = Topic("a.b.c")
    assert t.segments == ("a", "b", "c")


def test_matches_exact() -> None:
    assert Topic("a.b").matches("a.b")
    assert not Topic("a.b").matches("a.c")


def test_matches_wildcard() -> None:
    assert Topic("a.b").matches("a.*")
    assert Topic("orders.created").matches("orders.*")
    assert not Topic("orders.updated").matches("orders.created")


def test_mismatched_length() -> None:
    assert not Topic("a.b").matches("*")


def test_empty_topic_raises() -> None:
    with pytest.raises(ValueError):
        Topic("")
