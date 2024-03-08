import os
import re
import pandas as pd

def list_files(directory):
    """List all .xlsx files in the given directory."""
    return [file for file in os.listdir(directory) if file.endswith('.xlsx')]

def categorize_files(file_list):
    """Categorize files into main and side stories."""
    main_stories = []
    side_stories = []
    for file in file_list:
        if re.match(r"main_\d+_", file):
            main_stories.append(file)
        elif re.match(r"act\d+.*?_", file):
            side_stories.append(file)
    return main_stories, side_stories

def read_xlsx(file_path):
    """Read .xlsx file and return a list of dataframes, each representing a table (scene)."""
    return pd.read_excel(file_path, sheet_name=None)

def extract_dialogues(dataframes):
    """Extract characters and dialogues from each scene."""
    extracted_data = []
    for df in dataframes.values():
        # Adjusting to index-based access (1 for 'B' and 2 for 'C')
        scene_data = {
            'characters': df.iloc[:, 1].tolist(),  # Column 'B'
            'dialogues': df.iloc[:, 2].tolist()    # Column 'C'
        }
        extracted_data.append(scene_data)
    return extracted_data

# Main execution
file_path = "data\\Arknights_plot"
files = list_files(file_path)
main_stories, side_stories = categorize_files(files)

all_data = {'main_stories': {}, 'side_stories': {}}
for story in main_stories:
    dfs = read_xlsx(os.path.join(file_path, story))
    all_data['main_stories'][story] = extract_dialogues(dfs)

for story in side_stories:
    dfs = read_xlsx(os.path.join(file_path, story))
    all_data['side_stories'][story] = extract_dialogues(dfs)

# Now all_data contains the extracted information from all the xlsx files
