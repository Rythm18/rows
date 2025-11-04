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


class SelectOperationTestCase(utils.RowsTestMixIn, unittest.TestCase):
    def test_select_imports(self):
        """Test that select is properly imported"""
        assert hasattr(rows, 'select')
        assert rows.select is rows.operations.select

    def test_select_single_column(self):
        """Test selecting a single column from a table"""
        table = rows.Table(fields=OrderedDict([
            ('name', rows.fields.TextField),
            ('age', rows.fields.IntegerField),
            ('city', rows.fields.TextField),
        ]))
        table.append({'name': 'Alice', 'age': 30, 'city': 'NYC'})
        table.append({'name': 'Bob', 'age': 25, 'city': 'LA'})

        result = rows.select(table, ['name'])
        
        assert result.field_names == ['name']
        assert len(result) == 2
        assert result[0].name == 'Alice'
        assert result[1].name == 'Bob'
        # Ensure other columns are not present
        assert not hasattr(result[0], 'age')
        assert not hasattr(result[0], 'city')

    def test_select_multiple_columns(self):
        """Test selecting multiple columns from a table"""
        table = rows.Table(fields=OrderedDict([
            ('name', rows.fields.TextField),
            ('age', rows.fields.IntegerField),
            ('city', rows.fields.TextField),
            ('country', rows.fields.TextField),
        ]))
        table.append({'name': 'Alice', 'age': 30, 'city': 'NYC', 'country': 'USA'})
        table.append({'name': 'Bob', 'age': 25, 'city': 'LA', 'country': 'USA'})

        result = rows.select(table, ['name', 'city'])
        
        assert result.field_names == ['name', 'city']
        assert len(result) == 2
        assert result[0].name == 'Alice'
        assert result[0].city == 'NYC'
        assert result[1].name == 'Bob'
        assert result[1].city == 'LA'
        assert not hasattr(result[0], 'age')
        assert not hasattr(result[0], 'country')

    def test_select_all_columns(self):
        """Test selecting all columns (should return equivalent table)"""
        table = rows.Table(fields=OrderedDict([
            ('name', rows.fields.TextField),
            ('age', rows.fields.IntegerField),
        ]))
        table.append({'name': 'Alice', 'age': 30})
        table.append({'name': 'Bob', 'age': 25})

        result = rows.select(table, ['name', 'age'])
        
        assert result.field_names == table.field_names
        assert len(result) == len(table)
        for orig_row, result_row in zip(table, result):
            assert orig_row == result_row

    def test_select_preserves_column_order(self):
        """Test that selected columns maintain the requested order"""
        table = rows.Table(fields=OrderedDict([
            ('a', rows.fields.TextField),
            ('b', rows.fields.TextField),
            ('c', rows.fields.TextField),
        ]))
        table.append({'a': '1', 'b': '2', 'c': '3'})

        result = rows.select(table, ['c', 'a'])
        
        assert result.field_names == ['c', 'a']
        assert result[0].c == '3'
        assert result[0].a == '1'

    def test_select_nonexistent_column_raises_error(self):
        """Test that selecting non-existent column raises ValueError"""
        table = rows.Table(fields=OrderedDict([
            ('name', rows.fields.TextField),
            ('age', rows.fields.IntegerField),
        ]))
        table.append({'name': 'Alice', 'age': 30})

        with self.assertRaises(ValueError) as context:
            rows.select(table, ['name', 'nonexistent'])
        
        assert 'nonexistent' in str(context.exception).lower()

    def test_select_empty_columns_list_raises_error(self):
        """Test that empty columns list raises ValueError"""
        table = rows.Table(fields=OrderedDict([
            ('name', rows.fields.TextField),
        ]))
        table.append({'name': 'Alice'})

        with self.assertRaises(ValueError):
            rows.select(table, [])

    def test_select_with_different_field_types(self):
        """Test selecting columns with different data types"""
        import datetime
        import decimal
        
        table = rows.Table(fields=OrderedDict([
            ('name', rows.fields.TextField),
            ('age', rows.fields.IntegerField),
            ('balance', rows.fields.DecimalField),
            ('birthday', rows.fields.DateField),
            ('active', rows.fields.BoolField),
        ]))
        table.append({
            'name': 'Alice',
            'age': 30,
            'balance': decimal.Decimal('1000.50'),
            'birthday': datetime.date(1993, 5, 15),
            'active': True,
        })

        result = rows.select(table, ['name', 'balance', 'active'])
        
        assert result.field_names == ['name', 'balance', 'active']
        assert result.fields['name'] == rows.fields.TextField
        assert result.fields['balance'] == rows.fields.DecimalField
        assert result.fields['active'] == rows.fields.BoolField
        assert result[0].name == 'Alice'
        assert result[0].balance == decimal.Decimal('1000.50')
        assert result[0].active is True

    def test_select_from_csv_file(self):
        """Test selecting columns from an imported CSV file"""
        table = rows.import_from_csv('tests/data/brazilian-cities.csv')
        original_field_count = len(table.field_names)
        
        # Select subset of columns
        result = rows.select(table, ['city', 'state'])
        
        assert len(result.field_names) == 2
        assert result.field_names == ['city', 'state']
        assert len(result.field_names) < original_field_count
        assert len(result) == len(table)

    def test_select_preserves_table_mode(self):
        """Test that select preserves the table mode (eager/stream/etc)"""
        # Test with eager mode
        table_eager = rows.Table(
            fields=OrderedDict([('a', rows.fields.TextField), ('b', rows.fields.TextField)]),
            mode='eager'
        )
        table_eager.append({'a': '1', 'b': '2'})
        
        result = rows.select(table_eager, ['a'])
        assert result.mode == 'eager'
