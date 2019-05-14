""" tests for options """
from pathlib import Path

import pytest

from figcon import Figcon


class TestFigconBasic:
    """ tests for finding spick configs """

    # helper funcs
    def _make_basic_sconfig(self, base, figcon, **kwargs):
        """ Make a config file. """
        path = Path(base)
        filename = figcon._config_file_name
        if not str(path).endswith(".py"):
            path = path / filename
        with path.open("w") as fi:
            for item, val in kwargs.items():
                fi.write(f"{item} = {val}\n")
        return path

    # fixtures
    @pytest.fixture
    def mocked_here_and_home(self, home_cwd, figcon):
        """ update options with modified here and home """
        cwd, home = home_cwd["primary_path"], home_cwd["secondary_path"]
        # write sconfig files
        self._make_basic_sconfig(cwd, figcon, agency={"BOBCO": "Co of Bob"},
                                 custom=1)
        self._make_basic_sconfig(home, figcon, agency={"Mob": "co"}, custom2=2)
        # update options the revert on cleanup
        figcon.update_options(**home_cwd)
        yield figcon
        figcon.update_options()

    @pytest.fixture
    def basic_option_set(self, figcon):
        """ Set the basic option, then delete it. """
        figcon.update_options()
        figcon.set_option(basic=1)
        yield figcon
        del figcon.basic

    # tests
    def test_home_overwrites_base_options(self, mocked_here_and_home):
        """
        Ensure sconfig in home overwrites default, which get overwritten in
        cwd.
        """
        assert mocked_here_and_home.agency == {"BOBCO": "Co of Bob"}
        assert mocked_here_and_home.custom == 1
        assert mocked_here_and_home.custom2 == 2

    def test_raise_on_missing_option(self, figcon):
        """  Figcon should raise an attribute error when a non-existent
        option is requested. """
        with pytest.raises(AttributeError) as e:
            _ = figcon.no_one_is_home
        msg = str(e)
        assert "no_one_is_home" in msg
        assert "Options contains no item" in msg

    def test_primary_as_path(self, tmpdir, figcon):
        """ ensure the path to the sconfig file can also be supplied. """
        path = Path(tmpdir) / "not_sconfig.py"
        new = self._make_basic_sconfig(path, figcon, bob=2, bill=2)
        figcon.update_options(primary_path=new)
        assert figcon.bob == 2
        assert figcon.bill == 2

    def test_basic_set_option(self, basic_option_set):
        """ Ensure the basic option has been set. """
        assert hasattr(basic_option_set, "basic")
        assert basic_option_set.basic == 1

    def test_sconf_path_stored(self, mocked_here_and_home, home_cwd, figcon):
        """ Ensure the path to each config file path is being stored. """
        assert figcon.primary_path == home_cwd['primary_path']
        assert figcon.secondary_path == home_cwd['secondary_path']


class TestFigConAdvanced:
    """
    Similar to above but contains classes/simple namespaces that
    should be dynamically updated.
    """

    # fixtures
    @pytest.fixture
    def updated_figcon(self, home_cwd, config_paths, figcon):
        # files to copy
        sconfig1 = config_paths["config1.py"]
        sconfig2 = config_paths["config2.py"]
        assert sconfig1.exists() and sconfig2.exists()
        # destinations
        home, cwd = home_cwd["secondary_path"], home_cwd["primary_path"]
        conf1 = Path(cwd) / figcon._config_file_name
        # hidden files should work too
        conf2 = Path(home) / ('.' + figcon._config_file_name)
        conf1.write_bytes(sconfig1.read_bytes())
        conf2.write_bytes(sconfig2.read_bytes())
        # update options the revert on cleanup
        figcon.update_options(**home_cwd)
        yield figcon
        figcon.update_options()

    # tests
    def test_new_stuff_added(self, updated_figcon):
        """ ensure the new stuff in other configs is available in options """
        # it should also have the new attrs added by other config files
        assert hasattr(updated_figcon, "something_new")
        assert hasattr(updated_figcon, "new_namespace")

    def test_dicts_updated(self, updated_figcon):
        """
        Ensure the base options classes/simple names spaces were updated.
        """
        snuff = updated_figcon.snuffler
        # snuffler namespace should retain base attributes
        assert hasattr(snuff, "phase_map")
        # cwd takes priority
        assert snuff.box_alpha == 84
        # # but home should overwrite default
        assert snuff.gap_lap_tolerance == 100

    def test_nested_classes(self, updated_figcon):
        """ ensure nested classes/namespaces work. """
        cat = updated_figcon.catalog
        assert cat.tibble.fat
        assert cat.tibble.old
        assert cat.Dribble.out == 1
