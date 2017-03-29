from dbas import _environs_to_keys

def test_parse_env_name():
    self.assertEqual("TEST", _environs_to_keys("DBAS_TEST", prefix="DBAS_"))
    self.assertEqual("TEST", _environs_to_keys("TEST", prefix=""))
    self.assertEqual("FOO.BAR", _environs_to_keys("DBAS_FOO_BAR", prefix="DBAS_"))
    self.assertEqual("FOO_BAR", _environs_to_keys("DBAS_FOO__BAR", prefix="DBAS_"))
    self.assertEqual("FOO__BAR", _environs_to_keys("DBAS_FOO___BAR", prefix="DBAS_"))