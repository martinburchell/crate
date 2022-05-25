from io import StringIO
from unittest import TestCase

from crate_anon.common.extendedconfigparser import ConfigSection


class ConfigSectionTests(TestCase):
    def test_handles_line_endings(self):
        text = "[test]\r\nfoo = bar\n"

        section = ConfigSection("test", fileobj=StringIO(text))
        self.assertEqual(section.opt_str("foo"), "bar")
