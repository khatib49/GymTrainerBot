import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Instead of hardcoding your API key, load it from an environment variable
api_key = os.getenv("OPENAI_API_KEY")


# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all domains (if needed)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the incoming JSON data
        user_message = request.json.get('message')

        # Check if the message is empty
        if not user_message:
            return jsonify({'response': 'Please provide a message to continue the conversation.'})

        # Send a request to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the gpt-3.5-turbo model
            messages=[
                {"role": "system", "content": "You are a helpful virtual gym trainer."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7,
        )

        # Extract the response from the OpenAI API
        bot_response = response['choices'][0]['message']['content'].strip()

        # Return the response to the frontend
        return jsonify({'response': bot_response})

    except openai.error.AuthenticationError as e:
        # Handle OpenAI authentication errors
        return jsonify({'response': 'Oops! There seems to be an issue with my system. Please try again later. '+ e }), 500

    except openai.error.OpenAIError as e:
        # Handle OpenAI-related errors
        return jsonify({'response': 'Oops! Something went wrong with the chatbot service. Please try again later.' + e}), 500

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'response': 'Oops! Something went wrong. Please try again later.' + e}), 500


if __name__ == '__main__':
    # Run the Flask server
    app.run(debug=True)
