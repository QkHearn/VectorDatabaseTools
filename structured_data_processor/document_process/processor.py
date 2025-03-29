import os
import json
import argparse
import time
import xlsxwriter

def full_to_half(text):
    """
    Convert full-width characters to half-width characters.
    """
    result = []
    for char in text:
        code = ord(char)
        if code == 0x3000:  # 全角空格特殊处理
            code = 0x0020
        elif 0xFF01 <= code <= 0xFF5E:  # 其他全角字符（除空格）
            code -= 0xfee0
        result.append(chr(code))
    return ''.join(result)

def remove_newlines(text):
    """
    Remove newline characters from a string.
    """
    return text.replace('\n', '').replace('\r', '')
def preprocess(text):
    return remove_newlines(full_to_half(text))
    

def process_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Convert full-width characters to half-width before loading JSON
        content = preprocess(content)
        data = json.loads(content)

        if not isinstance(data, list):
            return "Invalid JSON format: Root element should be a list."

        qa_pairs = []
        for item in data:
            if isinstance(item, dict) and 'Question' in item and 'Answer' in item:
                question = item['Question'][:512]
                answer = item['Answer'][:800]
                qa_pairs.append((question, answer))
            else:
                return "Invalid JSON format: Each item should be a dictionary with 'Question' and 'Answer' keys."

        return qa_pairs
    except Exception as e:
        return f"Error processing file: {e}"

def process_jsonl_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        qa_pairs = []
        for line in lines:
            # Convert full-width characters to half-width before loading JSON
            line = preprocess(line)
            
            data = json.loads(line.strip())
            if isinstance(data, dict) and 'Question' in data and 'Answer' in data:
                question = data['Question'][:512]
                answer = data['Answer'][:800]
                qa_pairs.append((question, answer))
            else:
                return "Invalid JSONL format: Each line should be a dictionary with 'Question' and 'Answer' keys."

        return qa_pairs
    except Exception as e:
        return f"Error processing file: {e}"

def process_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Convert full-width characters to half-width before processing
        content = preprocess(content)

        qa_pairs = content.split('<separator>')
        processed_content = []

        for pair in qa_pairs:
            qa = pair.split('<delimiter>')
            if len(qa) == 2:
                question = qa[0].strip()[:512]
                answer = qa[1].strip()[:800]
                processed_content.append((question, answer))

        return processed_content
    except Exception as e:
        return f"Error processing file: {e}"

def write_to_excel(qa_pairs, output_file):
    try:
        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet('Template')

        # Set headers
        worksheet.write(0, 0, "Template")
        worksheet.write(1, 0, 'Question')
        worksheet.write(1, 1, 'Answer')

        # Write QA pairs
        for row_num, qa in enumerate(qa_pairs, start=2):
            worksheet.write(row_num, 0, qa[0])
            worksheet.write(row_num, 1, qa[1])

        workbook.close()
        return f"Output written to {output_file}"
    except Exception as e:
        return f"Error writing to Excel file: {e}"

def main():
    parser = argparse.ArgumentParser(description="Process a text, JSON, or JSONL file and output to an Excel file.")
    parser.add_argument('-f', '--file', type=str, required=True, help="Path to the input file.")
    parser.add_argument('-o', '--output', type=str, default='output.xlsx', help="Path to the output Excel file.")
    args = parser.parse_args()
    file_path = args.file
    output_file = args.output
    if output_file == 'output.xlsx':
        output_file = f"output-{time.time()}.xlsx"
    if not os.path.isfile(file_path):
        return "The provided path is not a valid file."

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.json':
        result = process_json_file(file_path)
    elif file_extension == '.jsonl':
        result = process_jsonl_file(file_path)
    elif file_extension == '.txt':
        result = process_txt_file(file_path)
    else:
        return "File type not supported."

    if isinstance(result, list):
        return write_to_excel(result, output_file)
    else:
        return result

if __name__ == "__main__":
    print(main())