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

def extract_posts_from_all_steps(results):
    all_steps_posts = {}
    
    for round_index, round_data in enumerate(results):
        steps = round_data['result']

        for step_index, step in enumerate(steps):
            step_key = f'step{step_index + 1}'
            if step_key not in all_steps_posts:
                all_steps_posts[step_key] = []

            # Extract user_data
            user_data = step['user_data']

            # Collect all posts from this step
            for user in user_data:
                all_steps_posts[step_key].extend(user['posts'])

    return all_steps_posts

def remove_opinion_and_phrases(text):
    # Remove the "opinion" and "phrases" parts from the text if present
    text = re.sub(r'"opinion":.*?(\,|$)', '', text)  # Remove "opinion" and following comma if present
    text = re.sub(r'"phrases":.*?(\}|$)', '', text)  # Remove "phrases" and following curly brace if present
    return text.strip(' ,')

if __name__ == "__main__":
    # Load parameters and results
    params = load_schema()
    results = load_result_from_file()

    # Extract posts from each step of all rounds
    all_steps_posts = extract_posts_from_all_steps(results)

    # Ensure the output directory exists
    output_dir = "extracted_text"
    os.makedirs(output_dir, exist_ok=True)

    # Process and save posts for each step
    for step_key, posts in all_steps_posts.items():
        # Define output file paths for each step
        output_file_with_opinion = os.path.join(output_dir, f"simulation_response_with_opinion_{step_key}.txt")
        output_file_only_response = os.path.join(output_dir, f"simulation_response_only_{step_key}.txt")

        # Open text files to write the responses for each step
        with open(output_file_with_opinion, "w") as file_with_opinion, \
             open(output_file_only_response, "w") as file_only_response:
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

        print(f"Responses for {step_key} have been written to {output_file_with_opinion} and {output_file_only_response}")
