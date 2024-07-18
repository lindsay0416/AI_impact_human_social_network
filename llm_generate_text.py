# This function is using API from gpt, need to pay
class GenerateText:
     # Function to post data to the /generate_text API and receive the generated text
    @staticmethod
    def get_generated_text(openai, prompt):
        generated_text = ""
        try:
            # Generate text using the OpenAI ChatCompletion endpoint
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Large Language Model (LLM) designed to adapt to the user's unique way of speaking. \
                     Your task is to simulate comments and responses based on the provided topic, ensuring they align with the user's profile."},
                    {"role": "user", "content": prompt}
                ]
            )
            # Extract the generated text and remove newlines and extra white spaces
            generated_text = response.choices[0].message.content.strip().replace("\n\n", " ").replace("\n", " ")
        except Exception as e:
            print(f"An error occurred: {e}")

        return generated_text, prompt