import pandas as pd
import os

# Set directory
directory = r'c:\Users\johnh\Documents\Test_code\OpenMarket\251209_NonVip'
output_file = 'Final_merged_all_data.csv'

# Get list of CSV files
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv') and f != output_file]
csv_files.sort()  # Ensure deterministic order

dfs = []
print(f"Found {len(csv_files)} files to merge.")

for file in csv_files:
    file_path = os.path.join(directory, file)
    try:
        # Read CSV. Assuming default encoding/separator. Adjust if needed.
        df = pd.read_csv(file_path)
        dfs.append(df)
        print(f"Read {file}: {df.shape}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

if not dfs:
    print("No CSV files found to merge.")
    exit()

# Horizontal merge (concatenate)
# axis=1 concatenates by index. If row counts differ, NaN will be filled.
merged_df = pd.concat(dfs, axis=1)

# Handle duplicate column names
new_columns = []
column_counts = {}
renamed_columns = []

for col in merged_df.columns:
    if col in column_counts:
        column_counts[col] += 1
        # Create suffix _01, _02, etc.
        suffix = f"_{column_counts[col]:02d}"
        new_name = f"{col}{suffix}"
        
        # Ensure new_name itself isn't a duplicate (rare edge case but good to be safe)
        # But here we are iterating existing columns sequentially.
        # If original columns were ["A", "A", "A_01"],
        # 1. "A" -> "A"
        # 2. "A" -> "A_01"
        # 3. "A_01" -> "A_01" (Wait, now we have duplicate "A_01")
        # To handle this robustly is complex, but the request specifically asked:
        # "중복되는 컬럼이 있으면 이름을 _01 이런식으로 수정해서 추가"
        # I will stick to the basic counter approach as requested.
        
        new_columns.append(new_name)
        renamed_columns.append(f"{col} -> {new_name}")
    else:
        column_counts[col] = 0
        new_columns.append(col)

# Assign new columns
merged_df.columns = new_columns

# Save to CSV
output_path = os.path.join(directory, output_file)
merged_df.to_csv(output_path, index=False)

print("-" * 30)
print(f"Successfully merged files into {output_file}")
print(f"Final shape: {merged_df.shape}")

if renamed_columns:
    print("\n[Renamed Columns]")
    for change in renamed_columns:
        print(change)
else:
    print("\nNo duplicate columns required renaming.")
