import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
import threading
import argparse
import sys


class CSVColumnSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CSV Column Selector")
        self.root.geometry("800x600")
        
        self.df = None
        self.csv_file_path = None
        self.selected_columns = []
        
        self.setup_gui()
    
    def setup_gui(self):
        """Configure the user interface"""
        try:
            # Main frame
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Grid configuration
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
            main_frame.rowconfigure(2, weight=1)
            
            # Set minimum window size
            self.root.minsize(1000, 700)
            
            # File selection button
            ttk.Button(main_frame, text="Select CSV File", 
                      command=self.select_csv_file).grid(row=0, column=0, columnspan=2, pady=(0, 10))
            
            # File information label
            self.file_info_label = ttk.Label(main_frame, text="No file selected")
            self.file_info_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
            
            # Frame with preview and columns
            content_frame = ttk.Frame(main_frame)
            content_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
            content_frame.columnconfigure(0, weight=1, minsize=350)  # Minimum width for columns
            content_frame.columnconfigure(1, weight=2)  # Preview gets more space
            content_frame.rowconfigure(1, weight=1)
            
            # Column selection section
            columns_label = ttk.Label(content_frame, text="Select Columns:", font=('TkDefaultFont', 10, 'bold'))
            columns_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
            
            # Frame with column selection options
            self.columns_frame = ttk.LabelFrame(content_frame, text="Column Selection", padding="5")
            self.columns_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
            self.columns_frame.columnconfigure(0, weight=1)
            self.columns_frame.rowconfigure(0, weight=1)
            
            # Scrollable frame for checkboxes
            checkbox_canvas = tk.Canvas(self.columns_frame)
            checkbox_scrollbar = ttk.Scrollbar(self.columns_frame, orient="vertical", command=checkbox_canvas.yview)
            self.checkbox_scrollable_frame = ttk.Frame(checkbox_canvas)
            
            self.checkbox_scrollable_frame.bind(
                "<Configure>",
                lambda e: checkbox_canvas.configure(scrollregion=checkbox_canvas.bbox("all"))
            )
            
            checkbox_canvas.create_window((0, 0), window=self.checkbox_scrollable_frame, anchor="nw")
            checkbox_canvas.configure(yscrollcommand=checkbox_scrollbar.set)
            
            checkbox_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            checkbox_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            
            # Buttons for select all/none
            checkbox_buttons_frame = ttk.Frame(self.columns_frame)
            checkbox_buttons_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
            
            ttk.Button(checkbox_buttons_frame, text="Select All", 
                      command=self.select_all_checkboxes).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(checkbox_buttons_frame, text="Deselect All", 
                      command=self.deselect_all_checkboxes).pack(side=tk.LEFT)
            
            # Data preview section
            preview_label = ttk.Label(content_frame, text="Data Preview (first 1000 rows):", font=('TkDefaultFont', 10, 'bold'))
            preview_label.grid(row=0, column=1, sticky=tk.W)
            
            # Preview frame
            preview_frame = ttk.LabelFrame(content_frame, text="CSV Preview", padding="5")
            preview_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
            preview_frame.columnconfigure(0, weight=1)
            preview_frame.rowconfigure(0, weight=1)
            
            # Treeview for data preview
            self.tree = ttk.Treeview(preview_frame)
            self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Scrollbars for treeview
            tree_v_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.tree.yview)
            tree_v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            self.tree.configure(yscrollcommand=tree_v_scrollbar.set)
            
            tree_h_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
            tree_h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
            self.tree.configure(xscrollcommand=tree_h_scrollbar.set)
            
            # Save button
            self.save_button = ttk.Button(main_frame, text="Save Selected Columns", 
                                         command=self.save_selected_columns, state=tk.DISABLED)
            self.save_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))
            
            # Progress bar
            self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
            self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during interface configuration: {str(e)}")
    
    def select_csv_file(self):
        """Select CSV file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if file_path:
                self.csv_file_path = file_path
                self.load_csv_file()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting file: {str(e)}")
    
    def load_csv_file(self):
        """Load CSV file in separate thread"""
        try:
            self.progress.start()
            self.file_info_label.config(text="Loading file...")
            
            # Start loading in separate thread
            thread = threading.Thread(target=self._load_csv_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"Error starting file loading: {str(e)}")
    
    def _load_csv_thread(self):
        """Load CSV in separate thread"""
        try:
            # Check file size
            file_size = os.path.getsize(self.csv_file_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # Use chunks for large files
            if file_size_mb > 100:  # If file larger than 100MB
                # Load only first 1000 rows for preview
                self.df = pd.read_csv(self.csv_file_path, nrows=1000)
                self.is_sample = True
                # Check total number of rows without loading entire file
                total_rows = sum(1 for line in open(self.csv_file_path, 'r', encoding='utf-8')) - 1  # -1 for header
                info_text = f"File: {Path(self.csv_file_path).name} ({file_size_mb:.1f}MB)\nTotal rows: {total_rows:,}\nLoaded sample: 1,000 rows"
            else:
                # Load entire file
                self.df = pd.read_csv(self.csv_file_path)
                self.is_sample = False
                info_text = f"File: {Path(self.csv_file_path).name} ({file_size_mb:.1f}MB)\nRows: {len(self.df):,}\nColumns: {len(self.df.columns)}"
            
            # Update GUI in main thread
            self.root.after(0, self._update_gui_after_load, info_text)
            
        except pd.errors.EmptyDataError:
            self.root.after(0, lambda: messagebox.showerror("Error", "CSV file is empty"))
            self.root.after(0, self.progress.stop)
        except pd.errors.ParserError as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"CSV parsing error: {str(e)}"))
            self.root.after(0, self.progress.stop)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error loading file: {str(e)}"))
            self.root.after(0, self.progress.stop)
    
    def _update_gui_after_load(self, info_text):
        """Update GUI after loading file"""
        try:
            self.progress.stop()
            self.file_info_label.config(text=info_text)
            
            # Clear previous data
            self.tree.delete(*self.tree.get_children())
            
            # Clear checkboxes if they exist
            for widget in self.checkbox_scrollable_frame.winfo_children():
                widget.destroy()
            
            # Add columns and create checkboxes
            self.column_vars = {}
            self.column_checkboxes = {}
            
            for i, col in enumerate(self.df.columns):
                # Create variable for checkbox
                var = tk.BooleanVar()
                var.trace('w', lambda name, index, mode, col=col: self.on_checkbox_change(col))
                self.column_vars[col] = var
                
                # Create checkbox
                checkbox = ttk.Checkbutton(
                    self.checkbox_scrollable_frame, 
                    text=col, 
                    variable=var
                )
                checkbox.grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
                self.column_checkboxes[col] = checkbox
            
            # Configure treeview
            self.tree["columns"] = list(self.df.columns)
            self.tree["show"] = "headings"
            
            # Configure headers with automatic width
            for col in self.df.columns:
                self.tree.heading(col, text=col)
                # Set column width based on name length and content
                col_width = max(len(col) * 8, 80)  # Minimum 80px, 8px per character
                
                # Check width of sample data
                if len(self.df) > 0:
                    sample_data = self.df[col].head(10).astype(str)
                    max_data_width = max([len(str(val)) for val in sample_data] + [len(col)]) * 8
                    col_width = min(max_data_width, 200)  # Maximum 200px
                
                self.tree.column(col, width=col_width, minwidth=80)
            
            # Add first 1000 rows to preview
            preview_data = self.df.head(1000)
            for index, row in preview_data.iterrows():
                values = [str(val) if pd.notna(val) else "" for val in row]
                self.tree.insert("", tk.END, values=values)
            
            self.save_button.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating interface: {str(e)}")
    
    def on_checkbox_change(self, column_name):
        """Handle checkbox change"""
        try:
            # Additional logic can be added here if needed
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Error handling checkbox: {str(e)}")
    
    def select_all_checkboxes(self):
        """Select all checkboxes"""
        try:
            for var in self.column_vars.values():
                var.set(True)
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting all: {str(e)}")
    
    def deselect_all_checkboxes(self):
        """Deselect all checkboxes"""
        try:
            for var in self.column_vars.values():
                var.set(False)
        except Exception as e:
            messagebox.showerror("Error", f"Error deselecting all: {str(e)}")
    
    def save_selected_columns(self):
        """Save selected columns to new file"""
        try:
            # Get selected columns from checkboxes
            selected_columns = [col for col, var in self.column_vars.items() if var.get()]
            
            if not selected_columns:
                messagebox.showwarning("Warning", "No columns selected!")
                return
            
            # Check if columns exist
            missing_columns = [col for col in selected_columns if col not in self.df.columns]
            if missing_columns:
                messagebox.showerror("Error", f"Columns not found: {missing_columns}")
                return
            
            # Ask user for output file location and name
            input_path = Path(self.csv_file_path)
            default_name = f"{input_path.stem}_selected.csv"
            
            output_path = filedialog.asksaveasfilename(
                title="Save filtered CSV as...",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=default_name,
                initialdir=str(input_path.parent)
            )
            
            if not output_path:
                return  # User cancelled
            
            # Start saving in separate thread
            self.progress.start()
            thread = threading.Thread(target=self._save_csv_thread, args=(selected_columns, Path(output_path)))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error preparing save: {str(e)}")
    
    def _save_csv_thread(self, selected_columns, output_path):
        """Save CSV in separate thread"""
        try:
            if self.is_sample:
                # If previously loaded only sample, load entire file
                df_full = pd.read_csv(self.csv_file_path, usecols=selected_columns)
                df_to_save = df_full
            else:
                # Use already loaded data
                df_to_save = self.df[selected_columns]
            
            # Save to file
            df_to_save.to_csv(output_path, index=False)
            
            # Calculate saved file size
            output_size = os.path.getsize(output_path)
            output_size_mb = output_size / (1024 * 1024)
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"File saved as: {output_path.name}\n"
                f"Size: {output_size_mb:.2f}MB\n"
                f"Columns: {len(selected_columns)} of {len(self.df.columns)}\n"
                f"Selected columns: {', '.join(selected_columns[:5])}{', ...' if len(selected_columns) > 5 else ''}\n"
                f"Rows: {len(df_to_save):,}"
            ))
            self.root.after(0, self.progress.stop)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error saving: {str(e)}"))
            self.root.after(0, self.progress.stop)
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {str(e)}")


class CSVProcessor:
    """
    Class for programmatic CSV processing without GUI
    """
    
    def __init__(self, input_file):
        """
        Initialize CSV processor
        
        Args:
            input_file (str): Path to input CSV file
        """
        self.input_file = Path(input_file)
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        self.df = None
        self.columns = None
    
    def load_csv(self, nrows=None):
        """
        Load CSV file
        
        Args:
            nrows (int, optional): Number of rows to load. If None, loads all rows.
        
        Returns:
            pandas.DataFrame: Loaded data
        """
        try:
            if nrows:
                self.df = pd.read_csv(self.input_file, nrows=nrows)
            else:
                self.df = pd.read_csv(self.input_file)
            
            self.columns = list(self.df.columns)
            return self.df
        
        except Exception as e:
            raise Exception(f"Error loading CSV file: {str(e)}")
    
    def get_columns(self):
        """
        Get list of available columns
        
        Returns:
            list: List of column names
        """
        if self.columns is None:
            # Load only first row to get column names
            sample_df = pd.read_csv(self.input_file, nrows=1)
            self.columns = list(sample_df.columns)
        
        return self.columns
    
    def filter_columns(self, selected_columns, output_file, show_progress=True):
        """
        Filter CSV to include only selected columns
        
        Args:
            selected_columns (list): List of column names to keep
            output_file (str): Path for output file
            show_progress (bool): Whether to show progress information
        
        Returns:
            dict: Information about the operation (input/output sizes, row/column counts)
        """
        try:
            output_path = Path(output_file)
            
            # Validate selected columns
            available_columns = self.get_columns()
            invalid_columns = [col for col in selected_columns if col not in available_columns]
            
            if invalid_columns:
                raise ValueError(f"Invalid column names: {invalid_columns}")
            
            if not selected_columns:
                raise ValueError("No columns selected")
            
            # Get input file size
            input_size = self.input_file.stat().st_size
            input_size_mb = input_size / (1024 * 1024)
            
            if show_progress:
                print(f"Processing file: {self.input_file.name}")
                print(f"Input file size: {input_size_mb:.2f} MB")
                print(f"Selected columns: {', '.join(selected_columns)}")
            
            # Load data with selected columns only
            df_filtered = pd.read_csv(self.input_file, usecols=selected_columns)
            
            # Save to output file
            df_filtered.to_csv(output_path, index=False)
            
            # Get output file size
            output_size = output_path.stat().st_size
            output_size_mb = output_size / (1024 * 1024)
            
            result_info = {
                'input_file': str(self.input_file),
                'output_file': str(output_path),
                'input_size_mb': input_size_mb,
                'output_size_mb': output_size_mb,
                'total_columns': len(available_columns),
                'selected_columns': len(selected_columns),
                'selected_column_names': selected_columns,
                'rows': len(df_filtered)
            }
            
            if show_progress:
                print(f"Output file: {output_path.name}")
                print(f"Output file size: {output_size_mb:.2f} MB")
                print(f"Rows processed: {len(df_filtered):,}")
                print(f"Columns: {len(selected_columns)} of {len(available_columns)}")
                print("Operation completed successfully!")
            
            return result_info
            
        except Exception as e:
            raise Exception(f"Error filtering CSV: {str(e)}")


def command_line_interface():
    """Handle command line interface"""
    parser = argparse.ArgumentParser(
        description="CSV Column Selector - Filter CSV files by selecting specific columns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Filter CSV to include only name and age columns
  python data_collection_csv.py -i data.csv -c name,age -o filtered_data.csv
  
  # Show available columns in a CSV file
  python data_collection_csv.py -i data.csv --show-columns
  
  # Filter with custom columns
  python data_collection_csv.py -i employees.csv -c "first_name,last_name,salary" -o payroll.csv
        """
    )
    
    parser.add_argument('-i', '--input', required=True, 
                       help='Input CSV file path')
    parser.add_argument('-c', '--columns', 
                       help='Comma-separated list of column names to keep (e.g., "name,age,city")')
    parser.add_argument('-o', '--output', 
                       help='Output CSV file path')
    parser.add_argument('--show-columns', action='store_true',
                       help='Show available columns in the input file and exit')
    parser.add_argument('--gui', action='store_true',
                       help='Launch graphical user interface')
    
    args = parser.parse_args()
    
    try:
        # Initialize processor
        processor = CSVProcessor(args.input)
        
        # Show columns if requested
        if args.show_columns:
            columns = processor.get_columns()
            print(f"\nAvailable columns in '{args.input}':")
            print("-" * 50)
            for i, col in enumerate(columns, 1):
                print(f"{i:3d}. {col}")
            print(f"\nTotal columns: {len(columns)}")
            return
        
        # Launch GUI if requested
        if args.gui:
            app = CSVColumnSelector()
            app.run()
            return
        
        # Check if columns and output are provided for filtering
        if not args.columns or not args.output:
            print("Error: Both --columns and --output are required for filtering.")
            print("Use --show-columns to see available columns first.")
            print("Use --gui to launch the graphical interface.")
            parser.print_help()
            return
        
        # Parse column names
        selected_columns = [col.strip() for col in args.columns.split(',')]
        
        # Filter CSV
        result = processor.filter_columns(selected_columns, args.output)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    """Main function"""
    try:
        # Check if running from command line with arguments
        if len(sys.argv) > 1:
            command_line_interface()
        else:
            # Launch GUI by default
            app = CSVColumnSelector()
            app.run()
    except Exception as e:
        print(f"Error starting application: {str(e)}")


if __name__ == "__main__":
    main()