#!/usr/bin/env python3
"""
Example usage of CSV Column Selector as a Python module
"""

from data_collection_csv import CSVProcessor

def main():
    """Demonstrate different ways to use CSVProcessor"""
    
    print("CSV Column Selector - Example Usage")
    print("=" * 50)
    
    # Example 1: Basic usage
    print("\n1. Basic Usage:")
    try:
        processor = CSVProcessor('example.csv')
        
        # Show available columns
        columns = processor.get_columns()
        print(f"Available columns: {columns}")
        
        # Filter to include only name-related columns
        result = processor.filter_columns(
            selected_columns=['name', 'surname', 'age'],
            output_file='filtered_example.csv',
            show_progress=True
        )
        
        print(f"\nOperation completed:")
        print(f"- Rows processed: {result['rows']:,}")
        print(f"- Input size: {result['input_size_mb']:.2f} MB")
        print(f"- Output size: {result['output_size_mb']:.2f} MB")
        print(f"- Columns: {result['selected_columns']} of {result['total_columns']}")
        
    except Exception as e:
        print(f"Error in basic usage: {e}")
    
    # Example 2: Error handling
    print("\n2. Error Handling:")
    try:
        processor = CSVProcessor('example.csv')
        
        # Try to filter non-existent columns
        processor.filter_columns(['nonexistent_column'], 'output.csv')
        
    except Exception as e:
        print(f"Expected error caught: {e}")
    
    # Example 3: Programmatic column selection
    print("\n3. Programmatic Column Selection:")
    try:
        processor = CSVProcessor('example.csv')
        columns = processor.get_columns()
        
        # Select columns that contain certain keywords
        contact_columns = [col for col in columns if any(keyword in col.lower() 
                          for keyword in ['name', 'surname', 'number'])]
        
        print(f"Contact-related columns: {contact_columns}")
        
        if contact_columns:
            result = processor.filter_columns(
                selected_columns=contact_columns,
                output_file='contacts.csv',
                show_progress=False
            )
            print(f"Contact file created with {result['rows']} rows")
        
    except Exception as e:
        print(f"Error in programmatic selection: {e}")
    
    # Example 4: Batch processing simulation
    print("\n4. Batch Processing Simulation:")
    try:
        # Simulate processing the same file with different column sets
        processor = CSVProcessor('example.csv')
        
        column_sets = {
            'personal_info': ['name', 'surname', 'age'],
            'contact_info': ['name', 'surname', 'number'],
            'location_info': ['name', 'city'],
            'work_info': ['name', 'proffesion']  # Note: typo in original CSV
        }
        
        results = {}
        for set_name, columns in column_sets.items():
            try:
                result = processor.filter_columns(
                    selected_columns=columns,
                    output_file=f'{set_name}.csv',
                    show_progress=False
                )
                results[set_name] = result
                print(f"Created {set_name}.csv with {result['rows']} rows")
            except Exception as e:
                print(f"Error creating {set_name}: {e}")
        
        # Summary
        if results:
            print(f"\nBatch processing summary:")
            total_output_size = sum(r['output_size_mb'] for r in results.values())
            print(f"- Files created: {len(results)}")
            print(f"- Total output size: {total_output_size:.2f} MB")
    
    except Exception as e:
        print(f"Error in batch processing: {e}")


if __name__ == "__main__":
    main()
