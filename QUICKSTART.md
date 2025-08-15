# Quick Start Guide

## Installation
```bash
pip install pandas
```

## 1. GUI Mode (Default)
```bash
python data_collection_csv.py
```

## 2. Command Line Mode

### Show available columns:
```bash
python data_collection_csv.py -i your_file.csv --show-columns
```

### Filter CSV:
```bash
python data_collection_csv.py -i input.csv -c "column1,column2" -o output.csv
```

## 3. Python Module

```python
from data_collection_csv import CSVProcessor

# Initialize
processor = CSVProcessor('input.csv')

# Get columns
columns = processor.get_columns()

# Filter data
result = processor.filter_columns(['col1', 'col2'], 'output.csv')
```

## Examples

### Basic filtering:
```bash
python data_collection_csv.py -i example.csv -c "name,age" -o filtered.csv
```

### Multiple columns:
```bash
python data_collection_csv.py -i data.csv -c "id,name,email,phone" -o contacts.csv
```

### In Python script:
```python
from data_collection_csv import CSVProcessor

processor = CSVProcessor('employees.csv')
processor.filter_columns(['name', 'salary', 'department'], 'payroll.csv')
```
