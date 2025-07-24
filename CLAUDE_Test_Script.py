# Import the libraries we need for this chatbot
import os                    # This library helps us work with operating system functions (like reading environment variables)
from dotenv import load_dotenv  # This library helps us load secret keys from a .env file safely
from anthropic import Anthropic # This is the official Anthropic library for talking to Claude AI

# Load environment variables from a .env file
# This is a security best practice - we store secret API keys in a separate file
# instead of putting them directly in our code where others might see them
load_dotenv()

# Initialize the Anthropic client with our API key
# os.getenv() looks for a variable called "ANTHROPIC_API_KEY" in your system or .env file
# This client will handle all communication with Anthropic's servers (where Claude lives)
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Start an infinite loop to keep the chatbot running
# This continues until the user decides to quit
while True:
    # Get input from the user and wait for them to type something
    # The prompt clearly tells them how to exit the program
    prompt = input("Ask Claude (type 'quit' to exit): ")
    
    # Check if the user wants to exit the program
    # .lower() converts their input to lowercase so "QUIT", "quit", "Exit" all work the same
    if prompt.lower() in ["quit", "exit"]:
        break  # Exit the while loop, which ends the program

    # Make a request to Anthropic's messages API to get Claude's response
    message = client.messages.create(
        # Specify which Claude model to use - different models have different capabilities and costs
        model="claude-3-haiku-20240307",  # Haiku is fast and affordable, Sonnet is balanced, Opus is most capable
        
        # Set the maximum number of tokens (roughly words) Claude can use in its response
        # This prevents unexpectedly long responses and helps control costs
        max_tokens=500,
        
        # Temperature controls how creative/random the responses are
        # 0.0 = very focused and deterministic, 1.0 = very creative and random
        # 0.7 is a good balance for most conversations
        temperature=0.7,
        
        # Messages parameter expects a list of message objects
        # Unlike OpenAI, Claude doesn't require a system message (though you can add one)
        messages=[
            # User message: The actual question or prompt from the user
            # Each message needs a "role" (who said it) and "content" (what they said)
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and print Claude's response
    # message.content is a list that can contain different types of content (text, images, etc.)
    # [0] gets the first item in the list, .text gets the actual text content
    print("Claude:", message.content[0].text)

# Key differences between Claude, OpenAI, and Ollama:
# 
# Claude (this code):
# - Uses official Anthropic library (clean and simple)
# - No system message required (but you can add one)
# - Response format: message.content[0].text
# - Has max_tokens and temperature parameters for control
# - Generally good at following instructions and being helpful
#
# OpenAI (previous example):
# - Uses official OpenAI library
# - System message recommended for setting behavior
# - Response format: response.choices[0].message.content
# - Many model options (GPT-3.5, GPT-4, etc.)
#
# Ollama (first example):
# - Uses raw HTTP requests (more complex but more control)
# - Runs locally on your computer (no internet required after setup)
# - Streaming responses (words appear one by one)
# - Free to use once set up, but requires more technical setup

# To use this code, you need to:
# 1. Install required packages: pip install anthropic python-dotenv
# 2. Create a .env file in the same folder with: ANTHROPIC_API_KEY=your_actual_api_key_here
# 3. Sign up for an Anthropic account and get API credits
# 4. Optional: Try different models like "claude-3-sonnet-20240229" or "claude-3-opus-20240229"