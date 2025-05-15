import os
import json
def submitAssignment(file_path,data):
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            try:
                assignment_list = json.load(json_file)
                if not isinstance(assignment_list, list):
                    assignment_list = []
            except json.JSONDecodeError:
                assignment_list = []
    else:
        assignment_list = []

    assignment_list.append(data)

    with open(file_path, 'w') as json_file:
        json.dump(assignment_list, json_file, indent=4)

    print(f"Assignment successfully appended to '{file_path}'")
