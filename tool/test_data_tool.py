from llama_local_api import LlamaApi
import logging

logger = logging.getLogger("ds_tool")
logging.basicConfig(level="INFO")

def generate_user_profile(prompt):
    print("Prompt used for generating profile:", prompt)
    
    # Fetch the response from Llama API
    response = LlamaApi.llama_generate_messages(prompt)

    # Write the response to a text file
    with open("user_profile.txt", "w") as text_file:
        text_file.write(response)  # Writing response directly to a text file
        logger.info("Generated user profiles saved to user_profile.txt")
    
    return response

def main():
    prompt="Generate user profile as a 50-word unique description.\nAges of these users follow Gaussian distribution, gender is half and half.\nListed your response by user id strats with 'N' in JSON format.\nBased on this example:\n\"N1\": {\n     \"name\": \"Emily\",\n     \"age\": 32,\n     \"gender\": \"female\",\n     \"description\": \"a passionate artist who loves expressing herself through paintings. She finds inspiration in nature and often exhibits her artwork in local galleries.\"\n   }"
    print(prompt)
    response = generate_user_profile(prompt)
    print(response)



if __name__ == '__main__':
    main()