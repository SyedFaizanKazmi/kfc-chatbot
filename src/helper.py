from langchain.document_loaders import PyPDFDirectoryLoader
import PyPDF2
def read_file(file_path):
    with open(file_path, 'rb') as file:
        if file_path.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            return text
        elif file_path.endswith(".txt"):
            return file.read().decode('utf-8')
        else:
            raise ValueError("Unsupported file type")
        
def text_split(extracted_data, chunk_size=500, chunk_overlap=20):
    text_chunks = []
    start = 0
    while start < len(extracted_data):
        end = min(start + chunk_size, len(extracted_data))
        text_chunks.append(extracted_data[start:end])
        start += chunk_size - chunk_overlap

    return text_chunks