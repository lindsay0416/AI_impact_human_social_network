# Free use of local llama3 LLM
import ollama

class LlamaApi:
    @staticmethod
    def llama_generate_messages(prompt):

        # Initialize a list to store the messages and their timestamps
        messages_with_timestamps = []

        stream = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        complete_message = ""
        for chunk in stream:
            message_content = chunk['message']['content']
            # print(message_content, end='', flush=True)
            complete_message += message_content

        # Get the timestamp after the whole message is generated
        # timestamp = time.time_ns()
        
        # Store the complete message and its timestamp in the list
        messages_with_timestamps.append({
            # 'timestamp': timestamp,
            'message': complete_message
        })

        # Return the list of messages with their timestamps
        return complete_message
