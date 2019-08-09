#!/usr/bin/env python
# crate_anon/nlp_manager/cloud_config.py

"""
===============================================================================

    Copyright (C) 2015-2019 Rudolf Cardinal (rudolf@pobox.com).

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

Config object used for cloud NLP requests.

"""

import logging
import os
from typing import TYPE_CHECKING

from crate_anon.nlp_manager.constants import (
    CloudNlpConfigKeys,
    DEFAULT_CLOUD_LIMIT_BEFORE_COMMIT,
    DEFAULT_CLOUD_MAX_CONTENT_LENGTH,
    DEFAULT_CLOUD_MAX_RECORDS_PER_REQUEST,
    DEFAULT_CLOUD_MAX_TRIES,
    DEFAULT_CLOUD_RATE_LIMIT_HZ,
    DEFAULT_CLOUD_WAIT_ON_CONN_ERR_S,
)

if TYPE_CHECKING:
    from crate_anon.nlp_manager.nlp_definition import NlpDefinition

log = logging.getLogger(__name__)


# =============================================================================
# CloudConfig
# =============================================================================

class CloudConfig(object):
    """
    Common config object for cloud NLP.
    """

    def __init__(self, nlpdef: NlpDefinition, section: str) -> None:
        """
        Reads the config from the NLP definition's config file.

        Args:
            nlpdef:
                a :class:`crate_anon.nlp_manager.nlp_definition.NlpDefinition`
            section:
                config section name for the cloud NLP configuration
        """
        self._nlpdef = nlpdef
        sectionname = section
        # todo: sectionname = full_sectionname(..., section)
        config = nlpdef.get_parser()
        self.req_data_dir = os.path.abspath(config.get_str(
            section=sectionname, option=CloudNlpConfigKeys.REQUEST_DATA_DIR,
            required=True))
        self.url = config.get_str(
            section=sectionname, option=CloudNlpConfigKeys.CLOUD_URL,
            required=True)
        self.verify_ssl = config.get_bool(
            section=sectionname, option=CloudNlpConfigKeys.VERIFY_SSL,
            default=True)
        self.username = config.get_str(
            section=sectionname, option=CloudNlpConfigKeys.USERNAME,
            default="")
        self.password = config.get_str(
            section=sectionname, option=CloudNlpConfigKeys.PASSWORD,
            default="")
        self.max_content_length = config.get_int_default_if_failure(
            section=sectionname, option=CloudNlpConfigKeys.MAX_CONTENT_LENGTH,
            default=DEFAULT_CLOUD_MAX_CONTENT_LENGTH)
        self.limit_before_commit = config.get_int_default_if_failure(
            section=sectionname, option=CloudNlpConfigKeys.LIMIT_BEFORE_COMMIT,
            default=DEFAULT_CLOUD_LIMIT_BEFORE_COMMIT)
        self.max_records_per_request = config.get_int_default_if_failure(
            section=sectionname,
            option=CloudNlpConfigKeys.MAX_RECORDS_PER_REQUEST,
            default=DEFAULT_CLOUD_MAX_RECORDS_PER_REQUEST)
        self.stop_at_failure = config.get_bool(
            section=sectionname, option=CloudNlpConfigKeys.STOP_AT_FAILURE,
            default=True)
        self.wait_on_conn_err = config.get_int_default_if_failure(
            section=sectionname, option=CloudNlpConfigKeys.WAIT_ON_CONN_ERR,
            default=DEFAULT_CLOUD_WAIT_ON_CONN_ERR_S)
        self.max_tries = config.get_int_default_if_failure(
            section=sectionname, option=CloudNlpConfigKeys.MAX_TRIES,
            default=DEFAULT_CLOUD_MAX_TRIES)
        self.rate_limit_hz = config.get_int_default_if_failure(
            section=sectionname, option=CloudNlpConfigKeys.RATE_LIMIT_HZ,
            default=DEFAULT_CLOUD_RATE_LIMIT_HZ)
        # todo: processors

    def data_filename(self) -> str:
        """
        Returns the filename to be used for storing data.
        """
        nlpname = self._nlpdef.get_name()
        return os.path.abspath(os.path.join(
            self.req_data_dir, f"request_data_{nlpname}.txt"))
