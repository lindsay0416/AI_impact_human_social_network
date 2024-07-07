import json

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def update_parameters_json(parameters_path, new_initial_message):
    try:
        with open(parameters_path, 'r', encoding='utf-8') as file:
            parameters = json.load(file)
        
        parameters['initial_message'] = new_initial_message

        with open(parameters_path, 'w', encoding='utf-8') as file:
            json.dump(parameters, file, indent=4, separators=(',', ': '))
        print(f"Updated parameters.json with new initial message.")
    except Exception as e:
        print(f"Error updating {parameters_path}: {e}")

if __name__ == '__main__':
    text_file_path = 'initial_message.txt'  # Replace with your text file path
    parameters_json_path = 'parameters.json'  # Replace with your parameters.json file path

    new_initial_message = read_text_file(text_file_path)
    if new_initial_message:
        update_parameters_json(parameters_json_path, new_initial_message)
