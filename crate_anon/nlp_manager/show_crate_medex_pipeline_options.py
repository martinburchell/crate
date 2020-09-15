#!/usr/bin/env python

"""
crate_anon/nlp_manager/show_crate_medex_pipeline_options.py

===============================================================================

    Copyright (C) 2015-2020 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

**Run the compiled CrateMedexPipeline (Java) and show options.**

"""

import logging
import os

from cardinal_pythonlib.logs import main_only_quicksetup_rootlogger

from crate_anon.common.constants import (
    CRATE_NLP_JAVA_CLASS_DIR,
    ENVVAR_MEDEX_HOME,
)
from crate_anon.common.sysops import check_call_verbose, get_envvar_or_die


def main() -> None:
    """
    Command-line entry point.
    """
    main_only_quicksetup_rootlogger(level=logging.DEBUG)
    medex_home = get_envvar_or_die(ENVVAR_MEDEX_HOME)
    check_call_verbose([
        "java",
        "-classpath",
        f"{CRATE_NLP_JAVA_CLASS_DIR}:{medex_home}/bin:{medex_home}/lib/*",
        "CrateMedexPipeline",
        "--help",
        "-v", "-v",
    ])


if __name__ == "__main__":
    main()
