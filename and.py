import os
import json

folder_path = "all/原始"
output_file = "all/all.json"
unique_data = {}

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                note_id = item.get("note_id")
                if note_id not in unique_data:
                    unique_data[note_id] = item

# Write unique data to output file
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(list(unique_data.values()), outfile, ensure_ascii=False, indent=2)
