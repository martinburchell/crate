## -*- coding: utf-8 -*-
<%doc>

crate_anon/crateweb/specimen_archives/basic/base.mako

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

</%doc>

<%!
from crate_anon.common.constants import HelpUrl
%>

<!DOCTYPE html> <!-- HTML 5 -->
<html lang="en">
    <head>
        <%block name="head">
            <%block name="title">
                <title>CRATE Archive: ${patient_id}</title>
            </%block>
            <meta charset="utf-8">
            <%block name="extra_head_start"></%block>
            <link rel="icon" type="image/png" href="${get_static_url("scrubber.png")}" >
            <link rel="stylesheet" type="text/css" href="${get_static_url("archive.css")}" >
            <%block name="extra_head_end"></%block>
        </%block>
    </head>
    <body <%block name="body_tags"></%block>>
        <div class="title_bar row">
            <%block name="title_bar">
                <div class="float_left">CRATE basic archive demo: BRCID <b>${patient_id}</b>.</div>
                <div class="float_right">
                    [ <a href="${CRATE_HOME_URL}">Return to CRATE home</a>
                    | <a href="<%block name="helpurl">${HelpUrl.archive()}</%block>">Help</a>
                    ]
                </div>
            </%block>
        </div>
        <div class="template_description">
            <%block name="template_description">
                <div class="warning">Missing template_description for ${template}</div>
            </%block>
        </div>
        <%block name="navigate_to_root">
            <div class="navigation">
                <a href="${get_template_url("root.mako")}">Go to top</a>
            </div>
        </%block>

        ${next.body()}

        <%block name="body_end"></%block>
    </body>
</html>
