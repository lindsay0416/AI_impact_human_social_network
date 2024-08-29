# Get the data from the results.json
# Collect all posts from the last step of the last round

import json
import re

def load_schema():
    with open("../input/parameters.json") as file:
        params = json.load(file)
    return params

def json_formatter(text):
    # Find the JSON-like structure within the text using regex
    match = re.search(r'\{(?:[^{}]|)*\}', text, re.DOTALL)
    if match:
        json_part = match.group()
        # Replace escape sequences and backslashes with spaces
        json_part = json_part.replace('\\n', ' ')\
                             .replace('\\t', ' ')\
                             .replace('\\"', '"')\
                             .replace('\\\\', ' ')\
                             .replace('\\', ' ')
        return json_part
    else:
        print("No JSON found in the text")
        return None

def load_result_from_file():
    with open("../saved/results.json", "r") as file:
        results = json.load(file)
        results = results.get("simulation")
    return results

def extract_last_round_posts(results, params):
    last_round_index = params.get("round") - 1  # last round index
    last_step_index = params.get("timestep") - 1  # last timestep index

    # Get the last round
    last_round = results[last_round_index]

    # Get the last step
    last_step = last_round['result'][last_step_index]

    # Extract user_data
    user_data = last_step['user_data']

    # Collect all posts from the last step of the last round
    all_posts = []
    for user in user_data:
        all_posts.extend(user['posts'])

    return all_posts

if __name__ == "__main__":
    # Load parameters and results
    params = load_schema()
    results = load_result_from_file()

    # Extract posts
    posts = extract_last_round_posts(results, params)

    # Collect and print only the response text
    # Open a text file to write the responses
    with open("simulation_response.txt", "w") as output_file:
        # Collect and write only the response text
        for post in posts:
            # Attempt to parse the JSON part of the post
            json_part = json_formatter(post)
            if json_part:
                try:
                    post_data = json.loads(json_part)
                    if 'response' in post_data:
                        response = post_data['response']
                        output_file.write(response + "\n\n")  # Write each response followed by a newline
                except json.JSONDecodeError:
                    print("Failed to decode JSON part:", json_part)

    print("Responses have been written to simulation_response.txt")
