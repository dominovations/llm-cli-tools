# Import the libraries we need for this chatbot
import os           # This library helps us work with operating system functions (like reading environment variables)
from dotenv import load_dotenv  # This library helps us load secret keys from a .env file safely
from openai import OpenAI       # This is the official OpenAI library for talking to their API

# Load environment variables from a .env file
# This is a security best practice - we store secret API keys in a separate file
# instead of putting them directly in our code where others might see them
load_dotenv()

# Get the OpenAI API key securely from environment variables
# os.getenv() looks for a variable called "OPENAI_API_KEY" in your system or .env file
# This way, your secret API key isn't visible in your code
api_key = os.getenv("OPENAI_API_KEY")

# Create an OpenAI client object using our API key
# This client will handle all communication with OpenAI's servers
# Think of it like a phone connection to OpenAI's AI models
client = OpenAI(api_key=api_key)

# Start an infinite loop to keep the chatbot running
# This continues until the user decides to quit
while True:
    # Get input from the user and wait for them to type something
    # The prompt gives them instructions on how to exit
    prompt = input("Ask something (type 'quit' to exit): ")
    
    # Check if the user wants to exit the program
    # .lower() converts their input to lowercase so "EXIT", "quit", "Quit" all work the same
    if prompt.lower() in ["exit", "quit"]:
        break  # Exit the while loop, which ends the program

    # Make a request to OpenAI's chat completion API
    # This is different from the streaming approach - we get the full response at once
    response = client.chat.completions.create(
        model="gpt-4",  # Specify which AI model to use (GPT-4 is very capable but costs more)
        
        # Messages parameter expects a list of message objects
        # This allows for conversation context and different roles
        messages=[
            # System message: Sets the AI's personality and behavior
            # This tells the AI how it should act in the conversation
            {"role": "system", "content": "You are a helpful assistant."},
            
            # User message: The actual question or prompt from the user
            # Each message has a "role" (who said it) and "content" (what they said)
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and print the AI's response
    # response.choices[0] gets the first (and usually only) response option
    # .message.content gets the actual text content of the AI's reply
    print("AI:", response.choices[0].message.content)

# How this differs from the Mistral example:
# 1. Uses environment variables for API key security (better practice)
# 2. Uses the official OpenAI library (simpler than raw HTTP requests)
# 3. Uses the chat format with roles (system, user, assistant)
# 4. Gets the full response at once instead of streaming
# 5. No manual timing or token counting - the library handles the complexity

# To use this code, you need to:
# 1. Install required packages: pip install openai python-dotenv
# 2. Create a .env file in the same folder with: OPENAI_API_KEY=your_actual_api_key_here
# 3. Make sure you have OpenAI API credits in your account