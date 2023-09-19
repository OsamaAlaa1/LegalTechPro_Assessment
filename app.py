# Import needed functions and libraries
from utilities import *
from flask import Flask, request, render_template, jsonify, send_file
import openai
from pydantic import BaseModel
import langchain
import json 
import os

# Create a Flask app instance
app = Flask(__name__)


# Define route for the home page
@app.route("/")
@app.route("/home")
@app.route("/index.html")
def home():
    """
    Route for the home page.

    Returns:
        str: The rendered home page template.
    """
    return render_template("home.html")

# Define route for uploading clauses
@app.route("/upload_clauses", methods=["POST"])
def upload_clauses():
    """
    Route for uploading contract clauses.

    Returns:
        str: A message indicating the success or failure of the file upload.
    """
    if request.method == "POST":
        try:
            uploaded_file = request.files["file"]
            if not uploaded_file:
                return 'No file provided in the request.', 400

            upload_dir = os.path.join(app.root_path, "test_files")
            file_path = handle_file_upload(uploaded_file, upload_dir, "01_clauses")

            if not file_path:
                return 'File upload failed.', 500

            with open(file_path, 'r') as file:
                clauses = file.readlines()

            result_dir = os.path.join(app.root_path, "result_files")
            analysis_results = [interpret_contract_clause(clause) for clause in clauses]
            result_content = ""
            for id, result in enumerate(analysis_results):
                result_content += f'>> Interpretation and Analysis For the Clause \" {clauses[id]}\" :\n\n{result}\n\n-----------------------------------------------------------------------------------\n\n'
            
            result_filename = generate_result_file(result_dir, "01_clauses_analysis", result_content)

            return 'File uploaded successfully!'
        except Exception as e:
            return str(e), 500

# Define route for uploading contract information
@app.route('/upload_info', methods=['POST'])
def upload_info():
    """
    Route for uploading contract information.

    Returns:
        str: A message indicating the success or failure of the file upload.
    """
    if request.method == "POST":
        try:
            uploaded_file = request.files["file"]
            if not uploaded_file:
                return 'No file provided in the request.', 400

            upload_dir = os.path.join(app.root_path, "test_files")
            file_path = handle_file_upload(uploaded_file, upload_dir, "02_contract_info")

            if not file_path:
                return 'File upload failed.', 500

            with open(file_path, 'r') as file:
                data = json.load(file)

            standard_terms = data.get("standard_terms", "")
            previous_data = data.get("previous_data", "")
            current_context = data.get("current_context", "")
            suggestions = suggest_contract_clauses(standard_terms, previous_data, current_context)

            result_dir = os.path.join(app.root_path, "result_files")
            result_content = "Based on Terms, Previous Data, and Context the Contract Clause Suggestions: \n"
            for i, suggestion in enumerate(suggestions, start=1):
                result_content += f"{i}. {suggestion}\n"
            
            result_filename = generate_result_file(result_dir, "02_clauses_suggestions", result_content)

            return 'File uploaded and saved successfully!'
        except Exception as e:
            return str(e), 500

# Handle user messages and query OpenAI for clause analysis
@app.route('/analyze_clause', methods=['POST'])
def analyze_clause():
    """
    Route for analyzing contract clauses.

    Returns:
        JSON: A JSON response containing the analysis result.
    """
    try:
        if request.method == 'POST':
            user_message = request.form['userMessage']
            analysis = interpret_contract_clause(user_message)
            return jsonify({'response': analysis})
    except Exception as e:
        return jsonify({'error': 'An error occurred during analysis'})

# ... (continue defining routes for other tasks)

# ... (previous code)

# Define route for uploading historical negotiation data
@app.route("/upload_history", methods=["POST"])
def upload_history():
    """
    Route for uploading historical negotiation data.

    Returns:
        str: A message indicating the success or failure of the file upload.
    """
    if request.method == "POST":
        try:
            uploaded_file = request.files["file"]
            if not uploaded_file:
                return 'No file provided in the request.', 400

            upload_dir = os.path.join(app.root_path, "test_files")
            file_path = handle_file_upload(uploaded_file, upload_dir, "04_historical_data")

            if not file_path:
                return 'File upload failed.', 500

            with open(file_path, 'r') as file:
                history = "".join(file.readlines())

            result_dir = os.path.join(app.root_path, "result_files")
            history_results = analyze_past_negotiations(history)
            result_content = f'>> Analysis of the historical negotiation data:\n\n{history_results}\n\n-----------------------------------------------------------------------------------\n\n'
            
            result_filename = generate_result_file(result_dir, "04_historical_analysis", result_content)

            return 'File uploaded successfully!'
        except Exception as e:
            return str(e), 500

# Define route for uploading negotiation details
@app.route("/upload_negotiation", methods=["POST"])
def upload_negotiation():
    """
    Route for uploading negotiation details.

    Returns:
        str: A message indicating the success or failure of the file upload.
    """
    if request.method == "POST":
        try:
            uploaded_file = request.files["file"]
            if not uploaded_file:
                return 'No file provided in the request.', 400

            upload_dir = os.path.join(app.root_path, "test_files")
            file_path = handle_file_upload(uploaded_file, upload_dir, "05_negotiation_details")

            if not file_path:
                return 'File upload failed.', 500

            with open(file_path, "r") as file:
                details = "".join(file.readlines())

            negotiation_summary = generate_negotiation_summary(details)

            result_dir = os.path.join(app.root_path, "result_files")
            result_content = f'>> Summarize Negotiation Details:\n\n{negotiation_summary}\n\n-----------------------------------------------------------------------------------\n\n'
            
            result_filename = generate_result_file(result_dir, "05_negotiation_summary", result_content)

            return 'File uploaded successfully!'
        except Exception as e:
            return str(e), 500

# Define route for performing an ethical check on negotiation text
@app.route("/ethical_check", methods=["POST"])
def ethical_check():
    """
    Route for performing an ethical check on negotiation text.

    Returns:
        str: A message indicating the success or failure of the file upload.
    """
    if request.method == "POST":
        try:
            uploaded_file = request.files["file"]
            if not uploaded_file:
                return 'No file provided in the request.', 400

            upload_dir = os.path.join(app.root_path, "test_files")
            file_path = handle_file_upload(uploaded_file, upload_dir, "06_negotiation_to_check")

            if not file_path:
                return 'File upload failed.', 500

            with open(file_path, "r") as file:
                data = json.load(file)

            negotiation_text = data['negotiation_text']
            industry = data['industry']

            guidance = ensure_compliance_and_ethical_standards(negotiation_text, industry)

            result_dir = os.path.join(app.root_path, "result_files")
            result_content = f'>> Ethical & Compliance Check:\n\n{guidance}\n\n-----------------------------------------------------------------------------------\n\n'
            
            result_filename = generate_result_file(result_dir, "06_ethical_check_results", result_content)

            return 'File uploaded successfully!'
        except Exception as e:
            return str(e), 500

# Define a dynamic route for downloading files
@app.route("/download/<file_name>")
def download_file(file_name):
    global tasks_result_file_names
    # Define a dictionary to map file_name to actual file paths
    file_paths = {
        "analysis": f"result_files/{tasks_result_file_names[0]}",
        "suggestions": f"result_files/{tasks_result_file_names[1]}",
        "history": f"result_files/{tasks_result_file_names[2]}",
        "summary": f"result_files/{tasks_result_file_names[3]}",
        "check": f"result_files/{tasks_result_file_names[4]}"
        # Add more mappings as needed
    }
    
    # Check if the requested file_name exists in the dictionary
    if file_name in file_paths:
        file_path = file_paths[file_name]
        return send_file(file_path, as_attachment=True)
    else:
        # Return an error response if the file_name is not found
        return "File not found", 404



# Run the Flask app
if __name__ == '__main__':
    app.run(port=8000, debug=True)



# if __name__ == "__main__":

#     # ------------------------------------------------------ task 1 Example usage -------------------------------------------

#     clause_text = "This agreement shall commence on the effective date and continue for a period of five (5) years unless terminated earlier."
#     analysis = interpret_contract_clause(clause_text)
#     print("Analysis:")
#     print(analysis)


#     # ------------------------------------------------------ task 2 Example usage -------------------------------------------

#     # Define the standard contract terms and previous negotiation data
#     standard_terms = """
#     1. Payment terms: Payments are due within 30 days of invoice.
#     2. Termination: Either party may terminate with 30 days' notice.
#     """

#     previous_data = """
#     - In the previous negotiation with Company X, they requested a 60-day payment term extension, which was accepted.
#     - Company Y requested an exclusive distribution clause, but it was rejected.
#     """

#     # Define the current negotiation context
#     current_context = {
#         'contract_type': 'Supply Agreement',
#         'your_company': 'Your Company Inc.',
#         'counterparty': 'Counterparty Corp.',
#         'concerns_goals': 'We aim to shorten payment terms without compromising supplier relationships.'
#     }

#     # Generate contract clause suggestions
#     suggestions = suggest_contract_clauses(standard_terms, previous_data, current_context)

#     # Print the suggestions
#     print("Contract Clause Suggestions:")
#     for i, suggestion in enumerate(suggestions, start=1):
#         print(f"{i}. {suggestion}\n")


#     # ------------------------------------------------------ task 3 Example usage -------------------------------------------
#     real_time_negotiation_assistance()


#     # ------------------------------------------------------ task 4 Example usage -------------------------------------------
#     past_negotiation_data = """
#     In the last negotiation with Company X, we successfully negotiated a 10% price reduction.
#     However, negotiations with Company Y resulted in a stalemate due to disagreements over delivery timelines.
#     """

#     insights = analyze_past_negotiations(past_negotiation_data)
#     print("Insights:")
#     print(insights)

#     # ------------------------------------------------------ task 5 Example usage -------------------------------------------

#     negotiation_details = """
#     During the negotiation, we agreed on the following terms:
#     - Price: $5,000 per unit
#     - Delivery Date: Within 30 days

#     Areas of concern:
#     - Warranty period is unclear.
#     - Payment terms need further clarification.

#     Next steps:
#     - Legal review of the contract.
#     - Finalize payment terms.

#     """

#     summary = generate_negotiation_summary(negotiation_details)
#     print("Negotiation Summary:")
#     print(summary)


#     # ------------------------------------------------------ task 6 Example usage -------------------------------------------

#     negotiation_text = """
#     We are negotiating the terms of a software licensing agreement in the healthcare IT industry.
#     """

#     industry = "healthcare"

#     guidance = ensure_compliance_and_ethical_standards(negotiation_text, industry)
#     print("Compliance and Ethical Standards Guidance:")
#     print(guidance)

#     # ------------------------------------------------------ task 7 Example usage -------------------------------------------
# # Predefined negotiation scenarios
#     negotiation_scenarios = [
#         {
#             "scenario": "Negotiating a software licensing agreement",
#             "user_goals": ["Lower cost", "Longer support period"],
#             "ai_goals": ["Higher price", "Shorter support period"],
#         },
#         {
#             "scenario": "Negotiating a sales contract",
#             "user_goals": ["Higher quantity", "Lower unit price"],
#             "ai_goals": ["Lower quantity", "Higher unit price"],
#         },
#     ]


#     simulate_negotiation(negotiation_scenarios)


#     # ------------------------------------------------------ task 8 Example usage -------------------------------------------

#     # Dummy negotiation data (to be replaced with your actual data)
#     negotiation_data = [
#         {"negotiation_text": "Sample negotiation 1.", "label": 1},
#         {"negotiation_text": "Sample negotiation 2.", "label": 0},
#         # Add more data...
#     ]

#     # Dummy user feedback (to be replaced with real feedback data)
#     user_feedback = [
#         {"negotiation_id": 1, "feedback": "AI was helpful."},
#         {"negotiation_id": 2, "feedback": "AI needs improvement."},
#         # Add more feedback...
#     ]

    
#     # Initial model training
#     initial_model = fine_tune_ai_model(negotiation_data)

        
#     # Update the model with new data and feedback (periodically)
#     updated_model = update_ai_model_with_feedback(initial_model, negotiation_data, user_feedback)

    

#     # Example usage of the AI model (generate responses)
#     def generate_ai_response(model, input_text):
#         """
#         Generate an AI response based on the input text.

#         Args:
#             model (keras.Model): The trained AI model.
#             input_text (str): The user's input text.

#         Returns:
#             str: AI-generated response.
#         """
#         # Replace with your own text generation logic
#         response = "This is a placeholder response from the AI model."
#         return response

#     # Example usage of generating AI responses
#     user_input = "What are the terms of the agreement?"
#     ai_response = generate_ai_response(updated_model, user_input)
#     print("AI Response:", ai_response)

