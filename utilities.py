# import needed packages 
import openai
import os 
from datetime import datetime
# Set up OpenAI API key.
#api_key = "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"
api_key = 'API_Key'
openai.api_key = api_key


#--------------------------------- Task 1:  interpret contractual clauses.---------------------------------------

def interpret_contract_clause(clause_text, openai_engine='gpt-3.5-turbo'):
    """
    Analyzes and Interprets a contract clause for potential pitfalls, non-standard terms, or unfavorable conditions.

    Args:
        clause_text (str): The text of the contract clause to be analyzed.
        openai_engine (str): The OpenAI engine to use for analysis. Options are 'gpt-3.5-turbo', 'text-davinci-003', or 'text-davinci-002'.

    Returns:
        str: The analysis of the contract clause.

    Raises:
        ValueError: If an unsupported OpenAI engine is provided.
    """

    # Define the prompt
    prompt = f"Please interpret the following contract clause and identify any potential pitfalls, non-standard terms, or unfavorable conditions:\n\n{clause_text}\n\nInterpretation:\n\nAnalysis:"

    if openai_engine == 'gpt-3.5-turbo':
        # Create a chat conversation for gpt-3.5-turbo
        conversation = [
            {"role": "system", "content": "You are a contract analysis assistant."},
            {"role": "user", "content": prompt},
        ]

        # Generate analysis using gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
        )

        # Extract and return the analysis
        analysis = response['choices'][0]['message']['content'].strip()
        return analysis

    elif openai_engine in ['text-davinci-003', 'text-davinci-002']:
        # Generate analysis using text-davinci-003 or text-davinci-002
        response = openai.Completion.create(
            engine=openai_engine,
            prompt=prompt,
            max_tokens=150,     # Limit the length of the response
            n=1,                # Generate a single completion
            stop=None,          # Allow the model to complete the entire analysis
            temperature=0.7,    # Control the randomness of the output
        )

        # Extract and return the analysis
        analysis = response.choices[0].text.strip()
        return analysis

    else:
        # Raise an error for unsupported engine names
        raise ValueError("Unsupported OpenAI engine. Please use 'gpt-3.5-turbo', 'text-davinci-003', or 'text-davinci-002'.")





#-------------------------------------- Task 2: Clause Suggestion & Drafting.---------------------------------------


def suggest_contract_clauses(standard_terms, previous_data, current_context):
    """
    Generate suggestions for contract clauses or modifications based on standard terms, previous negotiation data, and current context.

    Args:
        standard_terms (str): The standard contract terms of the company.
        previous_data (str): Relevant data from previous negotiations.
        current_context (dict): Information about the current negotiation context, including:
            - 'contract_type': The type of contract.
            - 'your_company': Your company's name or identifier.
            - 'counterparty': The name or identifier of the counterpart.
            - 'concerns_goals': Specific concerns or goals for this negotiation.

    Returns:
        list of str: A list of suggested contract clauses or modifications.

    Raises:
        openai.error.OpenAIError: If there is an issue with the OpenAI API request.
    """

    # Define a clear and informative conversation for chat-based API
    conversation = [
        {"role": "system", "content": "You are an AI contract assistant."},
        {"role": "user", "content": f"Based on our standard terms and previous negotiations, please suggest clauses or modifications for our {current_context['contract_type']} contract between {current_context['your_company']} and {current_context['counterparty']}. Our main goals are to protect our interests while ensuring fairness to the counterpart. Here are some key terms from our standard terms:\n\n{standard_terms}\n\nPrevious Negotiation Data:\n{previous_data}\n\nSpecific Concerns/Goals for this Negotiation: {current_context['concerns_goals']}\n\nSuggested Clauses:"},
    ]

    try:
        # Make an API call to GPT-3.5 Turbo with the conversation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=150,      # Limit the length of the response
            n=5,                 # Generate multiple suggestions for flexibility
            stop=None,           # Allow the model to complete the entire analysis
            temperature=0.7,     # Control the randomness of the output
        )

        # Extract and parse suggestions
        suggestions = [choice['message']['content'].strip() for choice in response['choices']]

        # Evaluate, customize, and incorporate suggestions into your contract draft

        return suggestions

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors, e.g., connection issues, rate limits, etc.
        raise e



#-------------------------------------- Task 3: Real-time Negotiation Assistance.---------------------------------------

def real_time_negotiation_assistance(user_message):
    """
    Provides real-time negotiation assistance using the OpenAI GPT-3.5 Turbo model.

    The function allows users to engage in a simulated negotiation with the AI model.
    Users can type messages, and the AI model responds with insights and suggestions.

    Args:
        user_message (str): The message from the user.

    Returns:
        str: The AI's response message.
    """
    try:
        # Send user's message to the AI model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are negotiating with a counterpart."},
                {"role": "user", "content": user_message},
            ]
        )

        ai_message = response['choices'][0]['message']['content']
        return str(ai_message)

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return f"AI: An error occurred with the OpenAI API: {e}"

#-------------------------------------- Task 4: Historical Data Analysis. ---------------------------------------

def analyze_past_negotiations(negotiation_data):
    """
    Analyze past negotiations, learning from successful compromises, stalemates, and points of contention
    to refine future negotiation strategies.

    Args:
        negotiation_data (str): Textual data containing information about past negotiations.

    Returns:
        str: Insights and recommendations for future negotiation strategies based on historical data.
    """
    # Define a prompt that combines the provided statement and historical negotiation data
    prompt = f"Analyze past negotiations, learning from successful compromises, stalemates, and points of contention to refine future negotiation strategies.\n\nHistorical Data:\n{negotiation_data}\n\nInsights:"

    try:
        # Make an API call to GPT-3.5 Turbo with the prompt
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,   # Adjust max tokens as needed
            n=1,              # Generate a single response
            stop=None,        # Allow the model to complete the entire analysis
            temperature=0.7,  # Control the randomness of the output
        )

        insights = response.choices[0].text.strip()
        return insights

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return f"An error occurred with the OpenAI API: {e}"



#-------------------------------------- Task 5: Stakeholder Communication. ---------------------------------------

def generate_negotiation_summary(negotiation_details):
    """
    Generate a concise summary post-negotiation.

    Args:
        negotiation_details (str): Textual details of the negotiation, including terms, concerns, and next steps.

    Returns:
        str: Concise summary of the negotiation, highlighting terms agreed upon, potential areas of concern, and next steps.
    """
    # Define a prompt for generating the negotiation summary
    prompt = f"Generate concise summaries post-negotiation, detailing the terms agreed upon, potential areas of concern, and next steps of the negotiation:\n\n{negotiation_details}\n\nSummary:"

    try:
        # Make an API call to GPT-3.5 Turbo with the prompt
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,   # Adjust max tokens as needed
            n=1,              # Generate a single response
            stop=None,        # Allow the model to complete the entire summary
            temperature=0.7,  # Control the randomness of the output
        )

        summary = response.choices[0].text.strip()
        return summary

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return f"An error occurred with the OpenAI API: {e}"



#-------------------------------------- Task 6: Ethical & Compliance Check. ---------------------------------------

def ensure_compliance_and_ethical_standards(negotiation_text, industry):
    """
    Incorporate a module to ensure compliance with industry regulations and ethical standards.

    Args:
        negotiation_text (str): The negotiation text to be analyzed.
        industry (str): The industry or sector for which compliance is required.

    Returns:
        str: Guidance on ensuring compliance and ethical standards.
    """
    # Define a prompt to request guidance on compliance and ethical standards
    prompt = f"Ensure compliance with industry regulations and maintain the highest ethical standards for negotiations in the {industry} industry:\n\n{negotiation_text}\n\nGuidance:"

    try:
        # Make an API call to GPT-3.5 Turbo with the prompt
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,  # Adjust max tokens as needed
            n=1,  # Generate a single response
            stop=None,  # Allow the model to complete the entire guidance
            temperature=0.7,  # Control the randomness of the output
        )

        guidance = response.choices[0].text.strip()
        return guidance

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return f"An error occurred with the OpenAI API: {e}"

#-------------------------------------- Task 7: simulate negotiation. ---------------------------------------

import random

def simulate_negotiation(negotiation_scenarios):
    """
    Simulate a negotiation with the AI.

    This function allows the user and AI to take turns in predefined negotiation scenarios.

    Args:
        None

    Returns:
        None
    """
    user_score = 0
    ai_score = 0

    print("AI: Welcome to the advanced negotiation simulation.")
    print("AI: You can start the negotiation by typing your message.")

    while True:
        # Select a random negotiation scenario
        scenario = random.choice(negotiation_scenarios)
        print(f"Scenario: {scenario['scenario']}\n")

        user_input = input("You: ")  # User's input
        
        if user_input.lower() == "exit":
            print("AI: Exiting the negotiation simulation.")
            break

        # Randomly select user and AI goals
        user_goals = random.sample(scenario['user_goals'], k=2)
        ai_goals = random.sample(scenario['ai_goals'], k=2)

        # User's message to the AI
        conversation = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": f"My goals are: {', '.join(user_goals)}."},
        ]

        try:
            # Make an API call to GPT-3.5 Turbo with the conversation
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
            )

            ai_message = response['choices'][0]['message']['content']
            print(f"AI: {ai_message}")

            # Randomly determine negotiation outcome
            user_wins = random.choice([True, False])
            
            if user_wins:
                print("AI: You achieved your negotiation goals.")
                user_score += 1
            else:
                print("AI: I achieved my negotiation goals.")
                ai_score += 1

            print(f"Score - You: {user_score}, AI: {ai_score}\n")

        except openai.error.OpenAIError as e:
            # Handle OpenAI API errors
            print(f"AI: An error occurred with the OpenAI API: {e}")
            print("AI: Exiting the negotiation simulation.")
            break

#-------------------------------------- Task 8: simulate negotiation. ---------------------------------------
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import numpy as np



def fine_tune_ai_model(negotiation_data):
    """
    Fine-tune an AI model with negotiation data.

    Args:
        negotiation_data (list): New negotiation data with text and labels.

    Returns:
        keras.Model: Trained AI model.
    """
    # Split data into training and validation sets
    train_data, val_data = train_test_split(negotiation_data, test_size=0.2, random_state=42)

    # Tokenization and preprocessing (replace with your actual preprocessing pipeline)
    tokenizer = tf.keras.layers.TextVectorization(max_tokens=1000)
    tokenizer.adapt([entry["negotiation_text"] for entry in train_data])

    # Define the neural network model
    model = keras.Sequential([
        keras.layers.Input(shape=(1,), dtype=tf.string),
        tokenizer,
        keras.layers.Embedding(input_dim=len(tokenizer.get_vocabulary()), output_dim=64, mask_zero=True),
        keras.layers.LSTM(64),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Preprocessing and training data
    train_texts = [entry["negotiation_text"] for entry in train_data]
    train_labels = np.array([entry["label"] for entry in train_data])

    # Training the model
    model.fit(train_texts, train_labels, epochs=5, validation_split=0.2)

    return model



def collect_user_feedback(feedback):
    """
    Collect and process user feedback.

    Args:
        feedback (list): User feedback on AI-generated responses.

    Returns:
        None
    """
    # Process user feedback (replace with your actual feedback processing logic)
    for entry in feedback:
        negotiation_id = entry["negotiation_id"]
        user_feedback = entry["feedback"]
        # Update your feedback processing logic here

def update_ai_model_with_feedback(model, negotiation_data, user_feedback):
    """
    Update the AI model with new data and feedback.

    Args:
        model (keras.Model): The existing AI model.
        negotiation_data (list): New negotiation data with text and labels.
        user_feedback (list): User feedback on AI-generated responses.

    Returns:
        keras.Model: Updated AI model.
    """
    # Fine-tune the existing model with new data (negotiation_data)
    new_model = fine_tune_ai_model(negotiation_data)

    # Collect and process user feedback
    collect_user_feedback(user_feedback)

    return new_model    


# another useful functions: 

# Define a function to handle file uploads and return the saved file path
def handle_file_upload(file, upload_dir, prefix):
    """
    Handle file upload and save it to the specified directory with a unique filename.
    
    Args:
        file: The uploaded file.
        upload_dir (str): The directory where the file should be saved.
        prefix (str): The prefix to be used in the filename.

    Returns:
        str: The path to the saved file or None if upload failed.
    """
    if not file:
        return None
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.txt"
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    return file_path

# Define a function to generate result files
def generate_result_file(result_dir, prefix, content):
    """
    Generate a result file with a unique filename and save it to the specified directory.

    Args:
        result_dir (str): The directory where the result file should be saved.
        prefix (str): The prefix to be used in the filename.
        content (str): The content to be written to the result file.

    Returns:
        str: The filename of the generated result file.
    """
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    result_filename = f"{prefix}_{timestamp}.txt"
    result_file_path = os.path.join(result_dir, result_filename)
    with open(result_file_path, "w") as result_file:
        result_file.write(content)
    return result_filename
