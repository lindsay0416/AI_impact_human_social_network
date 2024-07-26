from llama_local_api import LlamaApi
import logging
import json

logger = logging.getLogger("ds_tool")
logging.basicConfig(level="INFO")

def generate_user_profile(prompt, json_file_path):
    print("Prompt used for generating profile:", prompt)
    
    # Fetch the response from Llama API
    response = LlamaApi.llama_generate_messages(prompt)

    # Write the response to a text file
    with open("user_profile.txt", "w") as text_file:
        text_file.write(response)  # Writing response directly to a text file
        logger.info("Generated user profiles saved to user_profile.txt")
    
    save_to_json("user_profile.txt", json_file_path)
    return response

def save_to_json(file_path, json_file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract JSON formatted data from content
    # Assuming the JSON data starts from the first '{' and ends at the last '}'
    json_data_start = content.find('{')
    json_data_end = content.rfind('}') + 1
    json_content = content[json_data_start:json_data_end]

    print("Extracted JSON content:")
    print(json_content)

    try:
        # Load the JSON data
        data = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return

    # Save the JSON data to json_file_path
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data has been successfully extracted and saved to {json_file_path}.")

def main():
    prompt = (
        "Generate user profile as a 50-word unique description.\n"
        "Ages of these users follow Gaussian distribution, gender is half and half.\n"
        "Listed your response by user id starts with 'N' in JSON format.\n"
        "Based on this example:\n"
        "\"N1\": {\n"
        "    \"name\": \"Emily\",\n"
        "    \"age\": 32,\n"
        "    \"gender\": \"female\",\n"
        "    \"description\": \"a passionate artist who loves expressing herself through paintings. "
        "She finds inspiration in nature and often exhibits her artwork in local galleries.\"\n"
        "}"
    )
    print(prompt)
    json_file_path = "user_profile.json"
    response = generate_user_profile(prompt, json_file_path)
    print(response)

if __name__ == '__main__':
    main()
