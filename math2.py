import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame()
# Try reading the CSV file with a specific encoding and skip bad lines
try:
    df = pd.read_csv('/Users/arana/Downloads/YAM Speed Characterization.xlsx', encoding='ISO-8859-1', on_bad_lines='skip', delimiter=';')  # Change delimiter if needed
except Exception as e:
    print(f"Error reading the CSV file: {e}")

# Check if the necessary columns exist in the DataFrame
required_columns = ['Inc. Rate (nt/cycle)', 'Del. Rate (%)', 'Stdev inc_rate', 'Stdev del_rate']

if all(col in df.columns for col in required_columns):
    # Plotting the scatter plot with error bars
    plt.errorbar(df['Inc. Rate (nt/cycle)'], df['Del. Rate (%)'],
                 xerr=df['Stdev inc_rate'], yerr=df['Stdev del_rate'],
                 fmt='o', capsize=5, linestyle='None', color='blue')

    # Add labels and title
    plt.xlabel('Inc. Rate (nt/cycle)')
    plt.ylabel('Del. Rate (%)')
    plt.title('Scatter Plot of Inc. Rate vs Del. Rate with Standard Deviation')

    # Show the plot
    plt.show()
else:
    print("One or more required columns are missing.")
