# Import the libraries we need for this chatbot
import requests  # This library helps us make HTTP requests (like talking to websites/APIs)
import time      # This library helps us measure how long things take
import json      # This library helps us work with JSON data (a common data format)

# Configuration constants - these are settings that won't change during the program
OLLAMA_URL = "http://localhost:11434/api/generate"  # The web address where Ollama is running on your computer
MODEL_NAME = "mistral:7b-instruct"                 # The specific AI model we want to use (Mistral 7 billion parameters)

# Print a welcome message to let the user know the chatbot is ready
print("🔁 Mistral is ready. Type 'quit' to exit.\n")

# Start an infinite loop - this keeps the chatbot running until the user decides to quit
while True:
    # Get input from the user - this pauses the program and waits for them to type something
    prompt = input("You: ")
    
    # Check if the user wants to quit the program
    # .lower() converts their input to lowercase so "QUIT", "quit", "Quit" all work
    if prompt.lower() in ["quit", "exit"]:
        break  # Exit the while loop, which ends the program

    # Make an HTTP POST request to the Ollama API
    # This is like sending a message to the AI asking it to respond to the user's prompt
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,      # Tell the API which AI model to use
        "prompt": prompt,         # Send the user's message
        "stream": True            # Ask for a streaming response (words come back one at a time)
    }, stream=True)               # Tell requests library to also handle streaming

    # Print the beginning of Mistral's response
    # end="" means don't add a newline, flush=True means show the text immediately
    print("Mistral: ", end="", flush=True)

    # Start timing how long the response takes
    start = time.time()  # Get the current time in seconds
    token_count = 0      # Keep track of how many text chunks we receive

    # Use a try-except block to handle any errors that might happen
    try:
        # Loop through each line of the streaming response
        # The AI sends back data in small chunks rather than all at once
        for line in response.iter_lines():
            if line:  # Only process non-empty lines
                # Convert the raw bytes to a readable string and remove extra whitespace
                decoded = line.decode("utf-8").strip()
                
                try:
                    # Try to parse the line as JSON data
                    # Each line contains information about a piece of the response
                    data = json.loads(decoded)
                    
                    # Extract the actual text chunk from the JSON
                    # .get() safely gets a value from a dictionary, returning "" if the key doesn't exist
                    chunk = data.get("response", "")
                    
                    if chunk:  # If there's actual text in this chunk
                        # Print the text chunk immediately without a newline
                        # This creates the effect of text appearing word by word
                        print(chunk, end="", flush=True)
                        token_count += 1  # Count this as another chunk received
                    
                    # Check if this is the last chunk of the response
                    # The API sends "done": true when the response is complete
                    if data.get("done", False):
                        break  # Exit the for loop since we're done receiving data
                        
                except json.JSONDecodeError:
                    # If a line isn't valid JSON, just skip it and continue
                    # This can happen with streaming responses sometimes
                    continue
                    
    except Exception as e:
        # If any other error happens during streaming, show an error message
        print(f"\n❌ Error during streaming: {e}")

    # Calculate how long the response took
    end = time.time()  # Get the current time again
    
    # Print timing statistics
    # round() rounds the decimal to 2 places, \n adds a newline for spacing
    print(f"\n⏱️ Took {round(end - start, 2)}s, {token_count} chunks streamed\n")

# Note: When the while loop ends (user typed quit), the program automatically exits