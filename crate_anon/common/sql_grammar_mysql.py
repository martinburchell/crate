#!/usr/bin/env python
# crate_anon/crateweb/research/sql_grammar_mysql.py

"""
===============================================================================
    Copyright (C) 2015-2017 Rudolf Cardinal (rudolf@pobox.com).

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
"""

import logging
import re

from pyparsing import (
    Combine,
    cStyleComment,
    delimitedList,
    Forward,
    Group,
    infixNotation,
    Literal,
    NotAny,
    oneOf,
    OneOrMore,
    opAssoc,
    Optional,
    QuotedString,
    Regex,
    ZeroOrMore,
)

from crate_anon.common.logsupport import main_only_quicksetup_rootlogger
from crate_anon.common.sql_grammar import (
    ALL,
    AND,
    ansi_comment,
    AS,
    ASC,
    bash_comment,
    BETWEEN,
    BY,
    CASE,
    COLLATE,
    COMMA,
    CROSS,
    delim_list,
    DESC,
    DISTINCT,
    ELSE,
    END,
    EXISTS,
    FOR,
    FROM,
    GROUP,
    HAVING,
    IN,
    INDEX,
    INNER,
    integer,
    INTERVAL,
    IS,
    JOIN,
    KEY,
    LANGUAGE,
    LEFT,
    LIKE,
    literal_value,
    LPAR,
    make_regex_except_words,
    make_words_regex,
    MATCH,
    NATURAL,
    NOT,
    ON,
    OR,
    ORDER,
    OUTER,
    RIGHT,
    RPAR,
    SELECT,
    sql_keyword,
    SqlGrammar,
    test_fail,
    test_succeed,
    THEN,
    time_unit,
    UNION,
    USE,
    USING,
    WHEN,
    WHERE,
    WITH,
)

log = logging.getLogger(__name__)

AGAINST = sql_keyword("AGAINST")
BOOLEAN = sql_keyword("BOOLEAN")
EXPANSION = sql_keyword("EXPANSION")
MODE = sql_keyword("MODE")
NULLS = sql_keyword("NULLS")
QUERY = sql_keyword("QUERY")
ROW = sql_keyword("ROW")
TABLESPACE = sql_keyword("TABLESPACE")
BINARY = sql_keyword("BINARY")
DISTINCTROW = sql_keyword("DISTINCTROW")
DIV = sql_keyword("DIV")
FORCE = sql_keyword("FORCE")
HIGH_PRIORITY = sql_keyword("HIGH_PRIORITY")
IGNORE = sql_keyword("IGNORE")
LIMIT = sql_keyword("LIMIT")
MAX_STATEMENT_TIME = sql_keyword("MAX_STATEMENT_TIME")
MOD = sql_keyword("MOD")
OFFSET = sql_keyword("OFFSET")
OJ = sql_keyword("OJ")
PARTITION = sql_keyword("PARTITION")
PROCEDURE = sql_keyword("PROCEDURE")
REGEXP = sql_keyword("REGEXP")
ROLLUP = sql_keyword("ROLLUP")
SOUNDS = sql_keyword("SOUNDS")
SQL_BIG_RESULT = sql_keyword("SQL_BIG_RESULT")
SQL_BUFFER_RESULT = sql_keyword("SQL_BUFFER_RESULT")
SQL_CACHE = sql_keyword("SQL_CACHE")
SQL_CALC_FOUND_ROWS = sql_keyword("SQL_CALC_FOUND_ROWS")
SQL_NO_CACHE = sql_keyword("SQL_NO_CACHE")
SQL_SMALL_RESULT = sql_keyword("SQL_SMALL_RESULT")
STRAIGHT_JOIN = sql_keyword("STRAIGHT_JOIN")
XOR = sql_keyword("XOR")


# =============================================================================
# MySQL 5.7 grammar in pyparsing
# =============================================================================
# http://dev.mysql.com/doc/refman/5.7/en/dynindex-statement.html

class SqlGrammarMySQL(SqlGrammar):
    # -------------------------------------------------------------------------
    # Forward declarations
    # -------------------------------------------------------------------------
    expr = Forward()
    select_statement = Forward()

    # -------------------------------------------------------------------------
    # Keywords
    # -------------------------------------------------------------------------
    all_keywords = """
        AGAINST ALL ALTER AND ASC AS
        BETWEEN BINARY BOOLEAN BY
        CASE CASCADE COLLATE CREATE CROSS
        DATETIME DATE DELETE DESC DISTINCTROW DISTINCT DIV DROP
        ELSE END ESCAPE EXISTS EXPANSION
        FALSE FIRST FORCE FOR FROM
        GROUP
        HAVING HIGH_PRIORITY
        IGNORE INDEX INNER INSERT INTERVAL INTO IN IS
        JOIN
        KEY
        LANGUAGE LAST LEFT LIKE LIMIT
        MATCH MAX_STATEMENT_TIME MODE MOD
        NATURAL NOT NULLS NULL
        OFFSET OJ ONLY ON ORDER OR OUTER
        PARTITION PROCEDURE
        QUERY
        REGEXP RESTRICT RIGHT ROLLUP ROW
        SELECT SET SOUNDS SQL_BIG_RESULT SQL_BUFFER_RESULT
            SQL_CACHE SQL_CALC_FOUND_ROWS SQL_NO_CACHE SQL_SMALL_RESULT
            STRAIGHT_JOIN
        TABLESPACE TABLE THEN TIMESTAMP TIME TRUE
        UNION UPDATE USE USING UNKNOWN
        VALUES
        WITH WHEN WHERE
        XOR
    """
    keyword = make_words_regex(all_keywords, caseless=True, name="keyword")

    # -------------------------------------------------------------------------
    # Comments
    # -------------------------------------------------------------------------
    # http://dev.mysql.com/doc/refman/5.7/en/comments.html
    comment = (ansi_comment | bash_comment | cStyleComment)

    # -----------------------------------------------------------------------------
    # identifier
    # -----------------------------------------------------------------------------
    # http://dev.mysql.com/doc/refman/5.7/en/identifiers.html
    bare_identifier_word = make_regex_except_words(
        r"\b[a-zA-Z0-9$_]*\b",
        all_keywords,
        caseless=True,
        name="bare_identifier_word"
    )
    identifier = (
        bare_identifier_word |
        QuotedString(quoteChar="`", unquoteResults=False)
    ).setName("identifier")
    # http://dev.mysql.com/doc/refman/5.7/en/charset-collate.html
    collation_name = identifier.copy()
    column_name = identifier.copy()
    column_alias = identifier.copy()
    table_name = identifier.copy()
    table_alias = identifier.copy()
    index_name = identifier.copy()
    function_name = identifier.copy()
    parameter_name = identifier.copy()
    database_name = identifier.copy()
    partition_name = identifier.copy()

    no_dot = NotAny('.')
    table_spec = (
        Combine(database_name + '.' + table_name + no_dot) |
        table_name + no_dot
    ).setName("table_spec")
    column_spec = (
        Combine(database_name + '.' + table_name + '.' + column_name + no_dot) |
        Combine(table_name + '.' + column_name + no_dot) |
        column_name + no_dot
    ).setName("column_spec")

    # http://dev.mysql.com/doc/refman/5.7/en/expressions.html
    bind_parameter = Literal('?')

    # http://dev.mysql.com/doc/refman/5.7/en/user-variables.html
    variable = Regex(r"@[a-zA-Z0-9\.$_]+").setName("variable")

    # http://dev.mysql.com/doc/refman/5.7/en/functions.html
    argument_list = (
        delimitedList(expr).setName("arglist").setParseAction(', '.join)
    )
    # ... we don't care about sub-parsing the argument list, so use combine=True
    # or setParseAction: http://stackoverflow.com/questions/37926516
    function_call = Combine(function_name + LPAR) + argument_list + RPAR

    # http://dev.mysql.com/doc/refman/5.7/en/partitioning-selection.html
    partition_list = (
        LPAR + delim_list(partition_name, combine=True) + RPAR
    ).setName("partition_list")

    # http://dev.mysql.com/doc/refman/5.7/en/index-hints.html
    index_list = delim_list(index_name, combine=False)
    # ... see pyparsing_bugtest_delimited_list_combine
    index_hint = (
        (
            USE + (INDEX | KEY) +
            Optional(FOR + (JOIN | (ORDER + BY) | (GROUP + BY))) +
            LPAR + Optional(index_list) + RPAR
        ) |
        (
            IGNORE + (INDEX | KEY) +
            Optional(FOR + (JOIN | (ORDER + BY) | (GROUP + BY))) +
            LPAR + index_list + RPAR
        ) |
        (
            FORCE + (INDEX | KEY) +
            Optional(FOR + (JOIN | (ORDER + BY) | (GROUP + BY))) +
            LPAR + index_list + RPAR
        )
    )
    index_hint_list = delim_list(index_hint, combine=True).setName(
        "index_hint_list")

    # -----------------------------------------------------------------------------
    # CASE
    # -----------------------------------------------------------------------------
    # NOT THIS: https://dev.mysql.com/doc/refman/5.7/en/case.html
    # THIS: https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case  # noqa
    case_expr = (
        (
            CASE + expr +
            OneOrMore(WHEN + expr + THEN + expr) +
            Optional(ELSE + expr) +
            END
        ) | (
            CASE +
            OneOrMore(WHEN + expr + THEN + expr) +
            Optional(ELSE + expr) +
            END
        )
    ).setName("case_expr")

    # -------------------------------------------------------------------------
    # MATCH
    # -------------------------------------------------------------------------
    # https://dev.mysql.com/doc/refman/5.7/en/fulltext-search.html#function_match
    search_modifier = (
        (IN + NATURAL + LANGUAGE + MODE + Optional(WITH + QUERY + EXPANSION)) |
        (IN + BOOLEAN + MODE) |
        (WITH + QUERY + EXPANSION)
    )
    match_expr = (
        MATCH + LPAR + delim_list(column_spec) + RPAR +
        AGAINST + LPAR + expr + Optional(search_modifier) + RPAR
    ).setName("match_expr")

    # -----------------------------------------------------------------------------
    # Expressions
    # -----------------------------------------------------------------------------
    # http://dev.mysql.com/doc/refman/5.7/en/expressions.html
    # https://pyparsing.wikispaces.com/file/view/select_parser.py
    # http://dev.mysql.com/doc/refman/5.7/en/operator-precedence.html
    expr_term = (
        INTERVAL + expr + time_unit |
        # "{" + identifier + expr + "}" |  # see MySQL notes; antique ODBC syntax  # noqa
        Optional(EXISTS) + LPAR + select_statement + RPAR |
        # ... e.g. mycol = EXISTS(SELECT ...)
        # ... e.g. mycol IN (SELECT ...)
        LPAR + delim_list(expr) + RPAR |
        # ... e.g. mycol IN (1, 2, 3)
        case_expr |
        match_expr |
        bind_parameter |
        variable |
        function_call |
        literal_value |
        column_spec  # not just identifier
    )
    UNARY_OP, BINARY_OP, TERNARY_OP = 1, 2, 3
    expr << infixNotation(expr_term, [
        # https://pythonhosted.org/pyparsing/

        # Having lots of operations in the list here SLOWS IT DOWN A LOT.
        # Just combine them into an ordered list.
        (BINARY | COLLATE | oneOf('! - + ~'), UNARY_OP, opAssoc.RIGHT),
        (
            oneOf('^ * / %') | DIV | MOD |
            oneOf('+ - << >> & | = <=> >= > <= < <> !=') |
            (IS + Optional(NOT)) | LIKE | REGEXP | (Optional(NOT) + IN) |
            (SOUNDS + LIKE),  # RNC; presumably at same level as LIKE
            BINARY_OP,
            opAssoc.LEFT
        ),
        ((BETWEEN, AND), TERNARY_OP, opAssoc.LEFT),
        # CASE handled above (hoping precedence is not too much of a problem)
        (NOT, UNARY_OP, opAssoc.RIGHT),
        (AND | '&&' | XOR | OR | '||' | ':=', BINARY_OP, opAssoc.LEFT),
    ], lpar=LPAR, rpar=RPAR)
    # ignores LIKE [ESCAPE]

    # -------------------------------------------------------------------------
    # SELECT
    # -------------------------------------------------------------------------

    compound_operator = UNION + Optional(ALL | DISTINCT)
    # no INTERSECT or EXCEPT in MySQL?

    ordering_term = (
        expr + Optional(COLLATE + collation_name) + Optional(ASC | DESC)
    )
    # ... COLLATE can appear in lots of places;
    # http://dev.mysql.com/doc/refman/5.7/en/charset-collate.html

    join_constraint = Optional(Group(  # join_condition in MySQL grammar
        (ON + expr) |
        (USING + LPAR + delim_list(column_name) + RPAR)
    ))

    # http://dev.mysql.com/doc/refman/5.7/en/join.html
    join_op = Group(
        COMMA |
        STRAIGHT_JOIN |
        NATURAL + (Optional(LEFT | RIGHT) + Optional(OUTER)) + JOIN |
        (INNER | CROSS) + JOIN |
        Optional(LEFT | RIGHT) + Optional(OUTER) + JOIN
        # ignores antique ODBC "{ OJ ... }" syntax
    )

    join_source = Forward()
    single_source = (
        (
            table_spec.copy().setResultsName("from_tables",
                                             listAllMatches=True) +
            Optional(PARTITION + partition_list) +
            Optional(Optional(AS) + table_alias) +
            Optional(index_hint_list)
        ) |
        (select_statement + Optional(AS) + table_alias) +
        (LPAR + join_source + RPAR)
    )
    join_source << Group(
        single_source + ZeroOrMore(join_op + single_source + join_constraint)
    )("join_source")
    # ... must have a Group to append to it later, it seems
    # ... but name it "join_source" here, or it gets enclosed in a further list
    #     when you name it later

    result_column = (
        # AS expression must come first (to be greediest)
        expr + Optional(Optional(AS) + column_alias) |
        '*' |
        Combine(table_name + '.' + '*') |
        column_spec
    ).setResultsName("select_columns", listAllMatches=True)

    # -------------------------------------------------------------------------
    # SELECT
    # -------------------------------------------------------------------------
    # http://dev.mysql.com/doc/refman/5.7/en/select.html
    """
    SELECT
        [ALL | DISTINCT | DISTINCTROW ]
          [HIGH_PRIORITY]
          [MAX_STATEMENT_TIME = N]
          [STRAIGHT_JOIN]
          [SQL_SMALL_RESULT] [SQL_BIG_RESULT] [SQL_BUFFER_RESULT]
          [SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
        select_expr [, select_expr ...]
        [FROM table_references
          [PARTITION partition_list]
        [WHERE where_condition]
        [GROUP BY {col_name | expr | position}
          [ASC | DESC], ... [WITH ROLLUP]]
        [HAVING where_condition]
        [ORDER BY {col_name | expr | position}
          [ASC | DESC], ...]
        [LIMIT {[offset,] row_count | row_count OFFSET offset}]

    ... ignore below here...

        [PROCEDURE procedure_name(argument_list)]
        [INTO OUTFILE 'file_name'
            [CHARACTER SET charset_name]
            export_options
          | INTO DUMPFILE 'file_name'
          | INTO var_name [, var_name]]
        [FOR UPDATE | LOCK IN SHARE MODE]]
    """
    select_core = (
        SELECT +
        Group(Optional(ALL | DISTINCT | DISTINCTROW))("select_specifier") +
        Optional(HIGH_PRIORITY) +
        Optional(MAX_STATEMENT_TIME + '=' + integer) +
        Optional(STRAIGHT_JOIN) +
        Optional(SQL_SMALL_RESULT) +
        Optional(SQL_BIG_RESULT) +
        Optional(SQL_BUFFER_RESULT) +
        Optional(SQL_CACHE | SQL_NO_CACHE) +
        Optional(SQL_CALC_FOUND_ROWS) +
        Group(delim_list(result_column))("select_expression") +
        Optional(
            FROM + join_source +
            Optional(PARTITION + partition_list) +
            Group(Optional(WHERE + Group(expr)("where_expr")))("where_clause") +
            Optional(
                GROUP + BY +
                delim_list(ordering_term +
                           Optional(ASC | DESC))("group_by_term") +
                Optional(WITH + ROLLUP)
            ) +
            Optional(HAVING + expr("having_expr"))
        )
    )
    select_statement << (
        select_core +
        ZeroOrMore(compound_operator + select_core) +
        Optional(
            ORDER + BY +
            delim_list(ordering_term +
                       Optional(ASC | DESC))("order_by_terms")
        ) +
        Optional(LIMIT + (
            (Optional(integer("offset") + COMMA) + integer("row_count")) |
            (integer("row_count") + OFFSET + integer("offset"))
        ))
        # PROCEDURE ignored
        # rest ignored
    )
    select_statement.ignore(comment)

    # http://dev.mysql.com/doc/refman/5.7/en/identifiers.html
    # ... approximately (and conservatively):
    MYSQL_INVALID_FIRST_IF_UNQUOTED = re.compile(r"[^a-zA-Z_$]")
    MYSQL_INVALID_IF_UNQUOTED = re.compile(r"[^a-zA-Z0-9_$]")

    def __init__(self):
        super().__init__()

    @classmethod
    def quote_identifier(cls, identifier: str) -> str:
        return "`{}`".format(identifier)

    @classmethod
    def is_quoted(cls, identifier: str) -> bool:
        return identifier.startswith("`") and identifier.endswith("`")

    @classmethod
    def requires_quoting(cls, identifier: str) -> bool:
        assert identifier, "Empty identifier"
        if cls.MYSQL_INVALID_IF_UNQUOTED.search(identifier):
            return True
        firstchar = identifier[0]
        if cls.MYSQL_INVALID_FIRST_IF_UNQUOTED.search(firstchar):
            return True
        return False

    @classmethod
    def get_grammar(cls):
        # Grammar (here, just SELECT)
        return cls.select_statement

    @classmethod
    def get_column_spec(cls):
        return cls.column_spec

    @classmethod
    def get_join_op(cls):
        return cls.join_op

    @classmethod
    def get_table_spec(cls):
        return cls.table_spec

    @classmethod
    def get_join_constraint(cls):
        return cls.join_constraint

    @classmethod
    def get_select_statement(cls):
        return cls.select_statement

    @classmethod
    def get_expr(cls):
        return cls.expr

    @classmethod
    def test(cls, test_expr: bool = True):
        # ---------------------------------------------------------------------
        # Identifiers
        # ---------------------------------------------------------------------
        log.info("Testing keyword")
        # print(cls.keyword.pattern)
        test_succeed(cls.keyword, "TABLE")
        test_fail(cls.keyword, "thingfor")  # shouldn't match FOR
        test_fail(cls.keyword, "forename")  # shouldn't match FOR

        log.info("Testing bare_identifier_word")
        test_succeed(cls.bare_identifier_word, "blah")
        test_fail(cls.bare_identifier_word, "FROM")
        test_succeed(cls.bare_identifier_word, "forename")

        log.info("Testing identifier")
        test_succeed(cls.identifier, "blah")
        test_succeed(cls.identifier, "idx1")
        test_succeed(cls.identifier, "idx2")
        test_succeed(cls.identifier, "a")
        test_succeed(cls.identifier, "`a`")
        test_succeed(cls.identifier, "`FROM`")
        test_succeed(cls.identifier, "`SELECT FROM`")
        log.info("... done")

        log.info("Testing table_spec")
        test_succeed(cls.table_spec, "mytable")
        test_succeed(cls.table_spec, "mydb.mytable")
        test_succeed(cls.table_spec, "mydb.`my silly table`")
        test_fail(cls.table_spec, "mydb . mytable")
        test_fail(cls.table_spec, "mydb.mytable.mycol")

        log.info("Testing column_spec")
        test_succeed(cls.column_spec, "mycol")
        test_succeed(cls.column_spec, "forename")
        test_succeed(cls.column_spec, "mytable.mycol")
        test_succeed(cls.column_spec, "t1.a")
        test_succeed(cls.column_spec, "`my silly table`.`my silly column`")
        test_succeed(cls.column_spec, "mydb.mytable.mycol")
        test_fail(cls.column_spec, "mydb . mytable . mycol")

        log.info("Testing variable")
        test_succeed(cls.variable, "@myvar")

        log.info("Testing argument_list")
        test_succeed(cls.argument_list, "@myvar, 5")

        log.info("Testing function_call")
        test_succeed(cls.function_call, "myfunc(@myvar, 5)")

        log.info("Testing index_list")
        test_succeed(cls.index_list, "idx1, idx2")

        log.info("Testing index_hint")
        test_succeed(cls.index_hint, "USE INDEX FOR JOIN (idx1, idx2)")

        # ---------------------------------------------------------------------
        # Expressions
        # ---------------------------------------------------------------------

        log.info("Testing expr_term")
        test_succeed(cls.expr_term, "5")
        test_succeed(cls.expr_term, "-5")
        test_succeed(cls.expr_term, "5.12")
        test_succeed(cls.expr_term, "'string'")
        test_succeed(cls.expr_term, "mycol")
        test_succeed(cls.expr_term, "myfunc(myvar, 8)")
        test_succeed(cls.expr_term, "INTERVAL 5 MICROSECOND")
        test_succeed(cls.expr_term, "(SELECT 1)")
        test_succeed(cls.expr_term, "(1, 2, 3)")

        if test_expr:
            log.info("Testing expr")
            test_succeed(cls.expr, "5")
            test_succeed(cls.expr, "-5")
            test_succeed(cls.expr, "a")
            test_succeed(cls.expr, "mycol1 || mycol2")
            test_succeed(cls.expr, "+mycol")
            test_succeed(cls.expr, "-mycol")
            test_succeed(cls.expr, "~mycol")
            test_succeed(cls.expr, "!mycol")
            test_succeed(cls.expr, "a | b")
            test_succeed(cls.expr, "a & b")
            test_succeed(cls.expr, "a << b")
            test_succeed(cls.expr, "a >> b")
            test_succeed(cls.expr, "a + b")
            test_succeed(cls.expr, "a - b")
            test_succeed(cls.expr, "a * b")
            test_succeed(cls.expr, "a / b")
            test_succeed(cls.expr, "a DIV b")
            test_succeed(cls.expr, "a MOD b")
            test_succeed(cls.expr, "a % b")
            test_succeed(cls.expr, "a ^ b")
            test_succeed(cls.expr, "a ^ (b + (c - d) / e)")
            test_succeed(cls.expr, "a NOT IN (SELECT 1)")
            test_succeed(cls.expr, "a IN (1, 2, 3)")
            test_succeed(cls.expr, "a IS NULL")
            test_succeed(cls.expr, "a IS NOT NULL")
            test_fail(cls.expr, "IS NULL")
            test_fail(cls.expr, "IS NOT NULL")
            test_succeed(cls.expr, "(a * (b - 3)) > (d - 2)")

        log.info("Testing case_expr")
        test_succeed(cls.case_expr, """
            CASE v
              WHEN 2 THEN x
              WHEN 3 THEN y
              ELSE -99
            END
        """)

        log.info("Testing match_expr")
        test_succeed(cls.match_expr, """
             MATCH (content_field)
             AGAINST('+keyword1 +keyword2' IN BOOLEAN MODE)
        """)

        log.info("Testing join_op")
        test_succeed(cls.join_op, ",")
        test_succeed(cls.join_op, "INNER JOIN")

        log.info("Testing join_source")
        test_succeed(cls.join_source, "a")
        test_succeed(cls.join_source, "a INNER JOIN b")
        test_succeed(cls.join_source, "a, b")

        log.info("Testing result_column")
        test_succeed(cls.result_column, "t1.a")
        test_succeed(cls.result_column, "col1")
        test_succeed(cls.result_column, "t1.col1")
        test_succeed(cls.result_column, "col1 AS alias")
        test_succeed(cls.result_column, "t1.col1 AS alias")

        log.info("Testing select_statement")
        cls.test_select("SELECT t1.a, t1.b FROM t1 WHERE t1.col1 IN (1, 2, 3)")
        cls.test_select("SELECT a, b FROM c")  # no WHERE
        cls.test_select("SELECT a, b FROM c WHERE d > 5 AND e = 4")
        cls.test_select("SELECT a, b FROM c INNER JOIN f WHERE d > 5 AND e = 4")
        cls.test_select("SELECT t1.a, t1.b FROM t1 WHERE t1.col1 > 5")

        log.info("Testing SELECT something AS alias")
        cls.test_select("SELECT col1 AS alias FROM t1")
        cls.test_select("SELECT t1.col1 AS alias FROM t1")

        log.info("Testing nested query: IN")
        cls.test_select("SELECT col1 FROM table1 WHERE col2 IN (SELECT col3 FROM table2)")  # noqa

    @classmethod
    def test_select(cls, text: str) -> None:
        test_succeed(cls.select_statement, text, verbose=True)


# =============================================================================
# main
# =============================================================================

def main() -> None:
    log.info("TESTING MYSQL DIALECT")
    mysql = SqlGrammarMySQL()
    mysql.test()
    log.info("ALL TESTS SUCCESSFUL")


if __name__ == '__main__':
    main_only_quicksetup_rootlogger()
    main()
