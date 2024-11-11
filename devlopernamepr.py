import json
scc_files = [
    
    'c:/Users/houci/OneDrive/Bureau/New folder (2)/fakedata'
]
import json

# Define the file paths for input and output
input_file_path = 'c:/Users/houci/OneDrive/Bureau/New folder (2)/fakedata'  
output_file_path = 'c:/Users/houci/OneDrive/Bureau/New folder (2)/output_file.json'

# Load the JSON data from the input file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Process the data to get the output
output_data = []
for developer in data['developers']:
    dev_info = {
        'name': developer['name'],
        'projects': [project['project_name'] for project in developer['projects']]
    }
    output_data.append(dev_info)

# Write the output data to a new JSON file
with open(output_file_path, 'w') as file:
    json.dump(output_data, file, indent=4)

print(f"Output has been written to {output_file_path}")

            