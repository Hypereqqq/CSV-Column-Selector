#!/usr/bin/env python3
"""
Advanced examples for CSV Column Selector
"""

from data_collection_csv import CSVProcessor
import os
from pathlib import Path

def example_1_basic_filtering():
    """Basic filtering example"""
    print("=== Basic Filtering ===")
    
    processor = CSVProcessor('example.csv')
    
    # Filter to get only personal information
    result = processor.filter_columns(
        selected_columns=['name', 'surname', 'age'],
        output_file='basic_filtered.csv'
    )
    
    print(f"Filtered {result['rows']} rows with {result['selected_columns']} columns")
    return result

def example_2_conditional_filtering():
    """Conditional column selection based on criteria"""
    print("\n=== Conditional Filtering ===")
    
    processor = CSVProcessor('example.csv')
    columns = processor.get_columns()
    
    # Select columns that don't contain numbers in names
    text_columns = [col for col in columns if not any(char.isdigit() for char in col)]
    print(f"Text columns: {text_columns}")
    
    result = processor.filter_columns(
        selected_columns=text_columns,
        output_file='text_only.csv'
    )
    
    return result

def example_3_data_validation():
    """Validate data before processing"""
    print("\n=== Data Validation ===")
    
    processor = CSVProcessor('example.csv')
    
    # Load sample to check data quality
    sample_df = processor.load_csv(nrows=5)
    print(f"Sample data shape: {sample_df.shape}")
    print(f"Data types:\n{sample_df.dtypes}")
    
    # Get numeric columns
    numeric_columns = []
    for col in sample_df.columns:
        try:
            sample_df[col].astype(float)
            numeric_columns.append(col)
        except:
            pass
    
    print(f"Numeric columns: {numeric_columns}")
    
    if numeric_columns:
        result = processor.filter_columns(
            selected_columns=numeric_columns,
            output_file='numeric_data.csv'
        )
        return result

def example_4_batch_processing():
    """Process multiple column sets"""
    print("\n=== Batch Processing ===")
    
    processor = CSVProcessor('example.csv')
    
    # Define different data views
    data_views = {
        'demographics': ['name', 'surname', 'age'],
        'contact_info': ['name', 'surname', 'number'],
        'geographic': ['name', 'city'],
        'professional': ['name', 'proffesion']  # Note: keeping original typo
    }
    
    results = {}
    for view_name, columns in data_views.items():
        try:
            result = processor.filter_columns(
                selected_columns=columns,
                output_file=f'view_{view_name}.csv',
                show_progress=False
            )
            results[view_name] = result
            print(f"Created {view_name} view: {result['rows']} rows, {result['selected_columns']} columns")
        except Exception as e:
            print(f"Error creating {view_name}: {e}")
    
    return results

def example_5_column_analysis():
    """Analyze columns before filtering"""
    print("\n=== Column Analysis ===")
    
    processor = CSVProcessor('example.csv')
    
    # Load data for analysis
    df = processor.load_csv()
    
    print("Column analysis:")
    for col in df.columns:
        unique_count = df[col].nunique()
        null_count = df[col].isnull().sum()
        data_type = df[col].dtype
        
        print(f"  {col}: {unique_count} unique values, {null_count} nulls, type: {data_type}")
    
    # Select columns with high uniqueness (good for identification)
    high_unique_columns = []
    for col in df.columns:
        if df[col].nunique() / len(df) > 0.8:  # More than 80% unique
            high_unique_columns.append(col)
    
    print(f"High uniqueness columns: {high_unique_columns}")
    
    if high_unique_columns:
        result = processor.filter_columns(
            selected_columns=high_unique_columns,
            output_file='unique_identifiers.csv'
        )
        return result

def example_6_error_handling():
    """Demonstrate comprehensive error handling"""
    print("\n=== Error Handling ===")
    
    # Test various error conditions
    test_cases = [
        ('nonexistent_file.csv', ['name'], 'Should fail - file not found'),
        ('example.csv', ['invalid_column'], 'Should fail - column not found'),
        ('example.csv', [], 'Should fail - no columns selected'),
    ]
    
    for input_file, columns, description in test_cases:
        print(f"\nTesting: {description}")
        try:
            processor = CSVProcessor(input_file)
            result = processor.filter_columns(columns, 'test_output.csv')
            print(f"Unexpected success: {result}")
        except Exception as e:
            print(f"Expected error: {e}")

def cleanup_files():
    """Clean up generated files"""
    print("\n=== Cleanup ===")
    
    generated_files = [
        'basic_filtered.csv', 'text_only.csv', 'numeric_data.csv',
        'view_demographics.csv', 'view_contact_info.csv', 'view_geographic.csv', 'view_professional.csv',
        'unique_identifiers.csv', 'test_output.csv'
    ]
    
    for filename in generated_files:
        file_path = Path(filename)
        if file_path.exists():
            file_path.unlink()
            print(f"Removed: {filename}")

def main():
    """Run all examples"""
    print("CSV Column Selector - Advanced Examples")
    print("=" * 50)
    
    try:
        example_1_basic_filtering()
        example_2_conditional_filtering()
        example_3_data_validation()
        example_4_batch_processing()
        example_5_column_analysis()
        example_6_error_handling()
        
        print("\n" + "=" * 50)
        print("All examples completed!")
        
        # Ask user if they want to clean up
        cleanup_choice = input("\nClean up generated files? (y/n): ")
        if cleanup_choice.lower() in ['y', 'yes']:
            cleanup_files()
        
    except Exception as e:
        print(f"Error running examples: {e}")

if __name__ == "__main__":
    main()
