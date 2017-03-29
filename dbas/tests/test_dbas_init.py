from dbas import _environs_to_keys
from nose.tools import assert_equal

def test_parse_env_name():
    assert_equal("TEST", _environs_to_keys("DBAS_TEST", prefix="DBAS_"))
    assert_equal("TEST", _environs_to_keys("TEST", prefix=""))
    assert_equal("FOO.BAR", _environs_to_keys("DBAS_FOO_BAR", prefix="DBAS_"))
    assert_equal("FOO.BAR.BAZ", _environs_to_keys("DBAS_FOO_BAR_BAZ", prefix="DBAS_"))
    assert_equal("FOO_BAR", _environs_to_keys("DBAS_FOO__BAR", prefix="DBAS_"))
    assert_equal("FOO__BAR", _environs_to_keys("DBAS_FOO___BAR", prefix="DBAS_"))