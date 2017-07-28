from dbas import _environs_to_keys
from nose.tools import assert_equal


def test_parse_env_name():
    assert_equal("test", _environs_to_keys("DBAS_TEST", prefix="DBAS_"))
    assert_equal("test", _environs_to_keys("TEST", prefix=""))
    assert_equal("foo.bar", _environs_to_keys("DBAS_FOO_BAR", prefix="DBAS_"))
    assert_equal("foo.bar.baz", _environs_to_keys("DBAS_FOO_BAR_BAZ", prefix="DBAS_"))
    assert_equal("foo_bar", _environs_to_keys("DBAS_FOO__BAR", prefix="DBAS_"))
    assert_equal("foo__bar", _environs_to_keys("DBAS_FOO___BAR", prefix="DBAS_"))
    assert_equal("foo__bar", _environs_to_keys("DBAS_FOO____BAR", prefix="DBAS_"))
