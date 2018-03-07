from dbas import _environs_to_keys
from nose.tools import assert_equal


def test_parse_env_name():
    assert_equal("test", _environs_to_keys("TEST", prefix=""))
    assert_equal("test", _environs_to_keys("TEST", prefix=""))
    assert_equal("foo.bar", _environs_to_keys("FOO_BAR", prefix=""))
    assert_equal("foo.bar.baz", _environs_to_keys("FOO_BAR_BAZ", prefix=""))
    assert_equal("foo_bar", _environs_to_keys("FOO__BAR", prefix=""))
    assert_equal("foo__bar", _environs_to_keys("FOO___BAR", prefix=""))
    assert_equal("foo__bar", _environs_to_keys("FOO____BAR", prefix=""))
