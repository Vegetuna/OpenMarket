import pandas as pd
import os
import glob

# Define path to data_header relative to this notebook
# Notebook is in: .../Test_code/OpenMarket/251209_NonVip/
# data_header is in: .../Test_code/data_header/
data_header_path = "../../data_header"

# Output directory is the current directory
output_dir = "."

# Check if data_header exists
if os.path.exists(data_header_path):
    # Get all subdirectories in data_header
    subdirs = [d for d in os.listdir(data_header_path) if os.path.isdir(os.path.join(data_header_path, d))]
    subdirs.sort()
    
    print(f"Found {len(subdirs)} folders to process.")

    for folder in subdirs:
        folder_path = os.path.join(data_header_path, folder)
        
        # Get all csv files in the folder
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        
        if not csv_files:
            print(f"Skipping {folder}: No CSV files found.")
            continue
            
        print(f"\nProcessing {folder}...")
        
        dfs = []
        for file in csv_files:
            try:
                # Read CSV
                df = pd.read_csv(file)
                dfs.append(df)
            except Exception as e:
                print(f"  Error reading {os.path.basename(file)}: {e}")
        
        if dfs:
            # Concatenate all dataframes vertically
            merged_df = pd.concat(dfs, ignore_index=True)
            
            # Determine output filename
            # Logic: '01.회원정보_헤드' -> 'Merged_회원정보.csv'
            
            # Remove the number prefix (e.g. "01.") if present
            name_part = folder
            if '.' in name_part:
                parts = name_part.split('.', 1)
                if parts[0].isdigit():
                    name_part = parts[1]
            
            # Remove "_헤드" suffix if present
            name_part = name_part.replace("_헤드", "")
            
            output_filename = f"Merged_{name_part}.csv"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save to CSV
            merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            print(f"  Merged {len(dfs)} files into '{output_filename}' ({len(merged_df)} rows)")
else:
    print(f"Directory not found: {data_header_path}")
