# CSV Column Selector

A versatile program for selecting columns from large CSV files with multiple interfaces: graphical user interface, command line, and programmatic API.

## Features

- **Multiple Interfaces**: GUI, command line, and programmatic API
- Handles very large CSV files (even 4+ million rows)
- Graphical interface for column selection using checkboxes
- Command line interface for automation and scripting
- Python API for integration into other programs
- Preview of first 1000 rows of data
- Automatic column width adjustment based on content
- Custom file name and location selection for output
- Automatic creation of filtered CSV file with selected columns
- Safe error handling (try-catch blocks throughout)
- Multi-threaded processing for better responsiveness
- Detailed file information (size, row count, column count)

## Requirements

- Python 3.7+
- pandas
- tkinter (usually included with Python by default)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 1. Graphical User Interface (GUI)

Run the program without arguments to launch the GUI:

```bash
python data_collection_csv.py
```

Or explicitly launch GUI:
```bash
python data_collection_csv.py --gui
```

Steps:
1. Click "Select CSV File" and choose your file
2. The program will show columns and preview of the first 1000 rows
3. Select columns you want to keep using checkboxes
4. Use "Select All" or "Deselect All" buttons for convenience
5. Click "Save Selected Columns"
6. Choose the location and name for your output file
7. The program will create a new CSV file with only the selected columns

### 2. Command Line Interface

#### Show available columns:
```bash
python data_collection_csv.py -i example.csv --show-columns
```

#### Filter CSV file:
```bash
python data_collection_csv.py -i input.csv -c "column1,column2,column3" -o output.csv
```

#### Examples:
```bash
# Filter employee data to include only name and salary
python data_collection_csv.py -i employees.csv -c "name,surname,salary" -o payroll.csv

# Extract specific columns from large dataset
python data_collection_csv.py -i data.csv -c "id,timestamp,value" -o filtered_data.csv

# Show all available columns first
python data_collection_csv.py -i data.csv --show-columns
```

#### Command Line Arguments:
- `-i, --input`: Input CSV file path (required)
- `-c, --columns`: Comma-separated list of column names to keep
- `-o, --output`: Output CSV file path
- `--show-columns`: Show available columns and exit
- `--gui`: Launch graphical user interface

### 3. Programmatic API

Use as a Python module in your code:

```python
from data_collection_csv import CSVProcessor

# Initialize processor
processor = CSVProcessor('input.csv')

# Get available columns
columns = processor.get_columns()
print("Available columns:", columns)

# Filter and save specific columns
result = processor.filter_columns(
    selected_columns=['name', 'age', 'city'],
    output_file='filtered_output.csv'
)

print(f"Processed {result['rows']} rows")
print(f"Output file size: {result['output_size_mb']:.2f} MB")
```

#### API Methods:

**CSVProcessor(input_file)**
- `input_file`: Path to input CSV file

**get_columns()**
- Returns: List of column names

**load_csv(nrows=None)**
- `nrows`: Number of rows to load (optional)
- Returns: pandas DataFrame

**filter_columns(selected_columns, output_file, show_progress=True)**
- `selected_columns`: List of column names to keep
- `output_file`: Path for output file
- `show_progress`: Whether to show progress information
- Returns: Dictionary with operation details

## Example Data

For file `example.csv`:
```
name,surname,number,age,city,profession
Jan,Kowalski,123,25,Warsaw,Developer
Marta,Kasprzak,1245,30,Kraków,Designer
...
```

### GUI Example:
After selecting `name` and `surname` columns, a new file will be created:
```
name,surname
Jan,Kowalski
Marta,Kasprzak
...
```

### Command Line Example:
```bash
python data_collection_csv.py -i example.csv -c "name,age" -o young_people.csv
```

### API Example:
```python
processor = CSVProcessor('example.csv')
result = processor.filter_columns(['name', 'profession'], 'professionals.csv')
```

## Optimizations for Large Files

- Files > 100MB: program loads only a sample for preview but saves all data
- Uses pandas.read_csv with `usecols` parameter for efficiency
- Multi-threaded processing prevents interface freezing
- Progress bar shows operation status
- Automatic column width adjustment for better readability

## Error Handling

The program handles:
- Invalid CSV files
- Corrupted data
- Missing columns
- Memory issues
- Read/write errors
- File access problems

All errors are displayed in user-friendly messages.

## Advanced Examples

### Batch Processing Script
```python
from data_collection_csv import CSVProcessor
import os

# Process multiple files
input_dir = 'data_files'
output_dir = 'filtered_files'

for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f'filtered_{filename}')
        
        processor = CSVProcessor(input_path)
        processor.filter_columns(['id', 'name', 'value'], output_path)
```

### Integration with Data Pipeline
```python
from data_collection_csv import CSVProcessor

def process_customer_data(input_file, output_file):
    processor = CSVProcessor(input_file)
    
    # Get only customer-related columns
    customer_columns = ['customer_id', 'name', 'email', 'phone']
    
    result = processor.filter_columns(customer_columns, output_file)
    
    return {
        'success': True,
        'rows_processed': result['rows'],
        'output_size': result['output_size_mb']
    }
```
