import pandas as pd
import os

def remove_duplicates(input_csv, output_csv):
    """
    Opens a CSV file, removes duplicate rows based on the 'Datetime' column,
    and saves the cleaned data to a new CSV file.
    
    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to the output CSV file where cleaned data will be saved.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Remove duplicates based on the 'Datetime' column
    df_cleaned = df.drop_duplicates(subset='Datetime')
    
    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_csv, index=False)

    return len(df_cleaned)

def process_folder(folder_path):
    """
    Processes all CSV files in the given folder, removes duplicates, and logs the results.
    
    Args:
        folder_path (str): Path to the folder containing CSV files.
    """
    # Ensure the folder exists
    if not os.path.isdir(folder_path):
        print(f"The folder path {folder_path} is not valid.")
        return

    log_data = []

    # Process each CSV file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            input_csv = os.path.join(folder_path, file_name)
            output_csv = os.path.join(folder_path, f"cleaned_{file_name}")

            # Remove duplicates and get the final length
            final_length = remove_duplicates(input_csv, output_csv)

            # Log the result
            log_data.append({'File Name': file_name, 'Final Length': final_length})

    # Convert log data to a DataFrame
    log_df = pd.DataFrame(log_data)

    # Sort the log DataFrame based on 'Final Length' in ascending order
    log_df_sorted = log_df.sort_values(by='Final Length', ascending=True)

    # Save the sorted log data to a CSV file
    log_df_sorted.to_csv(os.path.join(folder_path, 'log.csv'), index=False)

    print("Processing complete. Log file saved as 'log.csv', sorted by final length.")

# Example usage
folder_path = input("Enter the path to the folder: ")
process_folder(folder_path)
