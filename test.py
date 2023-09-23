
# import warcio
# import json

# def extract_sales_negotiation_data(warc_file_path, output_jsonl_path):
#     try:
#         with open(output_jsonl_path, 'w', encoding='utf-8') as jsonl_file:
#             with open(warc_file_path, 'rb') as warc_file:
#                 for record in warcio.ArchiveIterator(warc_file):
#                     if record.rec_type == 'response':
#                         # Extract and process the text content from 'record.content_stream()'
#                         text = record.content_stream().read().decode('utf-8', 'ignore')
                        
#                         # Example: Check if the text contains sales negotiation keywords
#                         if 'sales' in text.lower() and 'negotiation' in text.lower():
#                             # Prepare a JSONL entry and write it to the output file
#                             json_entry = {"text": text.strip()}
#                             jsonl_file.write(json.dumps(json_entry, ensure_ascii=False) + '\n')
    
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

# # Usage example
# #warc_file_path = 'commoncrawl_data\commoncrawl.warc.gz'
# #output_jsonl_path = 'sales_negotiation_data.jsonl'
# #extract_sales_negotiation_data(warc_file_path, output_jsonl_path)


# import re
# import html

# def clean_and_save_as_jsonl(input_file_path, output_jsonl_path):
#     cleaned_data = []

#     try:
#         with open(input_file_path, 'r', encoding='utf-8') as input_file:
#             for line in input_file:
#                 # Remove HTML tags
#                 line = re.sub(r'<[^>]+>', '', line)
#                 # Decode HTML entities
#                 line = html.unescape(line)
#                 # Remove extra whitespaces and newlines
#                 line = ' '.join(line.split())
#                 # Remove non-alphanumeric characters except spaces
#                 line = re.sub(r'[^a-zA-Z0-9\s]', '', line)
#                 # Convert to lowercase
#                 line = line.lower()
#                 # Remove newline characters
#                 line = line.replace('\n', '')

#                 # Append cleaned text to the list
#                 cleaned_data.append({"text": line.strip()})

#         # Save cleaned data in JSONL format
#         with open(output_jsonl_path, 'w', encoding='utf-8') as jsonl_file:
#             for entry in cleaned_data:
#                 jsonl_file.write(json.dumps(entry, ensure_ascii=False) + '\n')

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

# # Usage example
# input_file_path = 'sales_negotiation_data.jsonl'
# output_jsonl_path = 'cleaned_sales_negotiation_data.jsonl'
# #clean_and_save_as_jsonl(input_file_path, output_jsonl_path)



# def extract_sales_negotiation_data(input_jsonl_path):
#     extracted_text = []

#     try:
#         with open(input_jsonl_path, 'r', encoding='utf-8') as jsonl_file:
#             for line in jsonl_file:
#                 # Parse the JSON line and extract the "text" field
#                 data = json.loads(line)
#                 text = data.get("text", "").strip()
                
#                 if text:
#                     # Append the extracted text to the array
#                     extracted_text.append(text)

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

#     return extracted_text

# def save_text_as_jsonl(text_list, output_jsonl_path):
#     try:
#         with open(output_jsonl_path, 'w', encoding='utf-8') as jsonl_file:
#             for text in text_list:
#                 # Create a JSON object for each text entry and write it to the file
#                 json_entry = {"text": text}
#                 jsonl_file.write(json.dumps(json_entry, ensure_ascii=False) + '\n')

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

# # Usage example
# input_jsonl_path = 'cleaned_sales_negotiation_data.jsonl'
# extracted_text = extract_sales_negotiation_data(input_jsonl_path)
# output_jsonl_path = 'extracted_sales_negotiation_data.jsonl'
# save_text_as_jsonl(extracted_text, output_jsonl_path)

# # Now, 'output_jsonl_path' contains the extracted text in JSONL format suitable for fine-tuning with OpenAI

