import json
import re
import os

def load_schema():
    with open("../input/parameters.json") as file:
        params = json.load(file)
    return params

def extract_response(text):
    # Find the "response" keyword in the text
    response_keyword = '"response":'
    response_index = text.find(response_keyword)

    if response_index != -1:
        # Extract everything after "response" keyword
        response_text = text[response_index + len(response_keyword):]

        # Optional: Clean up the text
        response_text = response_text.strip()

        # Stop at the next closing curly brace (or the end of the JSON structure)
        end_index = response_text.find('}')
        if end_index != -1:
            response_text = response_text[:end_index]

        # Remove any leading/trailing quotes or spaces
        response_text = response_text.strip(' "\'')
        
        return response_text
    else:
        print("No 'response' keyword found in the text")
        return None

def load_result_from_file():
    with open("../saved/results.json", "r") as file:
        results = json.load(file)
        results = results.get("simulation")
    return results

def extract_last_step_posts(results, params):
    last_step_index = params.get("timestep") - 1  # last timestep index

    all_posts = []
    for round_data in results:
        # Get the last step of the current round
        last_step = round_data['result'][last_step_index]

        # Extract user_data
        user_data = last_step['user_data']

        # Collect all posts from the last step
        for user in user_data:
            all_posts.extend(user['posts'])

    return all_posts

def remove_opinion_and_phrases(text):
    # Remove the "opinion" and "phrases" parts from the text if present
    text = re.sub(r'"opinion":.*?(\,|$)', '', text)  # Remove "opinion" and following comma if present
    text = re.sub(r'"phrases":.*?(\}|$)', '', text)  # Remove "phrases" and following curly brace if present
    return text.strip(' ,')

if __name__ == "__main__":
    # Load parameters and results
    params = load_schema()
    results = load_result_from_file()

    # Extract posts from the last step of all rounds
    posts = extract_last_step_posts(results, params)

    # Ensure the output directory exists
    output_dir = "extracted_text"
    os.makedirs(output_dir, exist_ok=True)

    # Path to the output files
    output_file_with_opinion = os.path.join(output_dir, "simulation_response_with_opinion.txt")
    output_file_only_response = os.path.join(output_dir, "simulation_response_only.txt")

    # Open text files to write the responses
    with open(output_file_with_opinion, "w") as file_with_opinion:
        with open(output_file_only_response, "w") as file_only_response:
            # Collect and write only the response text
            for post in posts:
                # Extract the text after the "response" keyword
                response = extract_response(post)
                if response:
                    # Write to the file with opinion and phrases
                    file_with_opinion.write(response + "\n\n")
                    
                    # Clean response by removing "opinion" and "phrases"
                    clean_response = remove_opinion_and_phrases(response)
                    
                    # Write to the file with only the response text
                    file_only_response.write(clean_response + "\n\n")

    print(f"Responses have been written to {output_file_with_opinion} and {output_file_only_response}")
