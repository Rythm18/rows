# coding: utf-8

# Copyright 2014-2025 Álvaro Justen <https://github.com/turicas/rows/>
#    This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
#    Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
#    any later version.
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
#    more details.
#    You should have received a copy of the GNU Lesser General Public License along with this program.  If not, see
#    <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import unittest
from collections import OrderedDict

import rows
import rows.operations
import tests.utils as utils


class UnionOperationsTestCase(utils.RowsTestMixIn, unittest.TestCase):
    def test_union_imports(self):
        """Test that union is properly exported from rows module"""
        assert hasattr(rows, "union")
        assert rows.union is rows.operations.union

    def test_union_basic(self):
        """Test basic union of two tables with same schema"""
        # Create first table
        fields1 = OrderedDict([
            ("id", rows.fields.IntegerField),
            ("name", rows.fields.TextField),
            ("age", rows.fields.IntegerField),
        ])
        table1 = rows.Table(fields=fields1)
        table1.append({"id": 1, "name": "Alice", "age": 30})
        table1.append({"id": 2, "name": "Bob", "age": 25})

        # Create second table with same schema
        fields2 = OrderedDict([
            ("id", rows.fields.IntegerField),
            ("name", rows.fields.TextField),
            ("age", rows.fields.IntegerField),
        ])
        table2 = rows.Table(fields=fields2)
        table2.append({"id": 3, "name": "Charlie", "age": 35})
        table2.append({"id": 4, "name": "Diana", "age": 28})

        # Perform union
        result = rows.union([table1, table2])

        # Verify results
        assert len(result) == 4
        assert result.field_names == ["id", "name", "age"]
        assert result[0].id == 1
        assert result[0].name == "Alice"
        assert result[0].age == 30
        assert result[1].id == 2
        assert result[1].name == "Bob"
        assert result[2].id == 3
        assert result[2].name == "Charlie"
        assert result[3].id == 4
        assert result[3].name == "Diana"

    def test_union_multiple_tables(self):
        """Test union of more than two tables"""
        fields = OrderedDict([
            ("x", rows.fields.IntegerField),
            ("y", rows.fields.TextField),
        ])
        
        table1 = rows.Table(fields=fields)
        table1.append({"x": 1, "y": "a"})

        table2 = rows.Table(fields=fields)
        table2.append({"x": 2, "y": "b"})

        table3 = rows.Table(fields=fields)
        table3.append({"x": 3, "y": "c"})

        table4 = rows.Table(fields=fields)
        table4.append({"x": 4, "y": "d"})

        result = rows.union([table1, table2, table3, table4])

        assert len(result) == 4
        assert result[0].x == 1
        assert result[1].x == 2
        assert result[2].x == 3
        assert result[3].x == 4

    def test_union_with_type_compatibility(self):
        """Test that union enforces field type consistency"""
        # Create two tables with same field names but compatible types
        fields1 = OrderedDict([
            ("id", rows.fields.IntegerField),
            ("value", rows.fields.FloatField),
        ])
        table1 = rows.Table(fields=fields1)
        table1.append({"id": 1, "value": 10.5})

        fields2 = OrderedDict([
            ("id", rows.fields.IntegerField),
            ("value", rows.fields.FloatField),
        ])
        table2 = rows.Table(fields=fields2)
        table2.append({"id": 2, "value": 20.5})

        result = rows.union([table1, table2])

        assert len(result) == 2
        assert result.fields["value"] == rows.fields.FloatField
        assert result[0].value == 10.5
        assert result[1].value == 20.5

    def test_union_empty_tables(self):
        """Test union with empty tables"""
        fields = OrderedDict([
            ("id", rows.fields.IntegerField),
            ("name", rows.fields.TextField),
        ])
        
        table1 = rows.Table(fields=fields)
        table1.append({"id": 1, "name": "Alice"})

        table2 = rows.Table(fields=fields)  # Empty table

        table3 = rows.Table(fields=fields)
        table3.append({"id": 2, "name": "Bob"})

        result = rows.union([table1, table2, table3])

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    def test_union_field_mismatch_error(self):
        """Test that union raises error when field names don't match"""
        fields1 = OrderedDict([
            ("id", rows.fields.IntegerField),
            ("name", rows.fields.TextField),
        ])
        table1 = rows.Table(fields=fields1)
        table1.append({"id": 1, "name": "Alice"})

        fields2 = OrderedDict([
            ("id", rows.fields.IntegerField),
            ("username", rows.fields.TextField),  # Different field name
        ])
        table2 = rows.Table(fields=fields2)
        table2.append({"id": 2, "username": "Bob"})

        with self.assertRaises(ValueError) as context:
            rows.union([table1, table2])
        
        assert "field names" in str(context.exception).lower()
