# **Pretty Tables**

This is a python package that aims to provide a simple and pretty way of printing tables to the console making use of a class.

The idea started as an attempt to reproduce the behavior of the [PM2](https://pm2.keymetrics.io) package when it displays tables to show data. Later, heavy inspiration came
of two other python packages:

- [Jazzband's](https://github.com/jazzband) [prettytable](https://github.com/jazzband/prettytable) (The names are similar by accident). Uses a class too.
- [Astanin's](https://github.com/astanin) [tabulate](https://github.com/astanin/python-tabulate). A very simple to use and efficient package.

A big part of the behavior of this package was replicated from these.

# Installation
``pip install prettyTables`` on Windows.

``pip3 install prettyTables`` on Linux

# Usage
Creating a table is simple.
### Code Example
```
from prettyTables import Table

new_table = Table()
print(new_table)
```
### Output
```
++

++

++
```
This is an empty table. It has no data so it only displays this strange thing.

It's possible to add data as columns or rows, or even alternating each one. Any untitled column will be named automatically.

### Code Example
```
new_table.add_column('Name', ['Jade', 'John', 'Jane'])
new_table.add_column('Age', [20, 30, 40])
new_table.add_column('Results', [9.651, 3, 245.7])
print(new_table)
```

### Output
```
+----------------------+
| Name   Age   Results |
+======+=====+=========+
| Jade |  20 |   9.651 |
| John |  30 |   3     |
| Jane |  40 | 245.7   |
+------+-----+---------+
```

### Code Example
```
new_table = Table()
new_table.add_column('Name', ['Jade', 'John', 'Jane'])
new_table.add_column('Age', [20, 30, 40])
new_table.add_column('Test\nResults', [9.651, 3, 245.7])
new_table.add_row(['Piotr\nBaltimore', 27, 3.5])
new_table.add_row(['Sam', 21, 0.6519])
print(new_table)
```

### Output
```
+----------------------------+
| Name        Age       Test |
|                    Results |
+===========+=====+==========+
| Jade      |  20 |   9.651  |
| John      |  30 |   3      |
| Jane      |  40 | 245.7    |
| Piotr     |  27 |   3.5    |
| Baltimore |     |          |
| Sam       |  21 |   0.6519 |
+-----------+-----+----------+
```
As it is visible, the table will format automatically new lines and data types, for now without trying to parse strings that could be converted to another type.

The ``Table`` class offers a variety of options that allow things like showing the index of each row, changing the style of the table, hiding the headers, etc.

See style examples [here](/style_examples.md).

### Code Example
```
new_table = Table()
new_table.add_column('Name', ['Jade', 'John'])
new_table.add_column('Age', [20, 30])
new_table.add_column('Test\nResults', [9.651, 3, 245.7])
new_table.add_row(['Piotr\nBaltimore', 27, 3.5])
new_table.add_row(['Sam', 21])
new_table.show_index = True
new_table.style_name = 'pretty_columns'
new_table.missing_value = '?'
print(new_table)
```

### Output
```
╒═══╤═══════════╤═════╤═════════╕
│ i │ Name      │ Age │    Test │
│   │           │     │ Results │
╞═══╪═══════════╪═════╪═════════╡
│ 0 │ Jade      │  20 │   9.651 │
│ 1 │ John      │  30 │   3     │
│ 2 │ ?         │   ? │ 245.7   │
│ 3 │ Piotr     │  27 │   3.5   │
│   │ Baltimore │     │         │
│ 4 │ Sam       │  21 │       ? │
╘═══╧═══════════╧═════╧═════════╛
```
The missing value aligns as if it was of the same type of the other data in the column.

This shows how to get the row and column count. If the index is shown, this count remains unaffected by that column, although, you can get the internal count.

### Code Example
```
new_table.show_index = False
new_table.show_headers = False
print(new_table)
print('row:', new_table.row_count)
print('columns:', new_table.column_count)
new_table.show_index = True
print(new_table)
print('internal_row_count:', new_table.internal_row_count)
print('internal_column_count:', new_table.internal_column_count)
```

### Output
```
╒═══════════╤════╤═════════╕
│ Jade      │ 20 │   9.651 │
│ John      │ 30 │   3     │
│ ?         │  ? │ 245.7   │
│ Piotr     │ 27 │   3.5   │
│ Baltimore │    │         │
│ Sam       │ 21 │       ? │
╘═══════════╧════╧═════════╛
row: 5
columns: 3
╒═══╤═══════════╤════╤═════════╕
│ 0 │ Jade      │ 20 │   9.651 │
│ 1 │ John      │ 30 │   3     │
│ 2 │ ?         │  ? │ 245.7   │
│ 3 │ Piotr     │ 27 │   3.5   │
│   │ Baltimore │    │         │
│ 4 │ Sam       │ 21 │       ? │
╘═══╧═══════════╧════╧═════════╛
internal_row_count: 5
internal_column_count: 4
```

# Known Issues
- Alignment only works when sending data as its type. Type parsing is still missing.
- When auto-wrapping is ``False`` the adjusting of the table to the console will potentially fail.
- Naming a column ``"i"`` will mess up what columns show if the index column is displaying.
- Exponential numbers only align incorrectly.
