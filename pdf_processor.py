import PyPDF2
import os
from typing import List, Dict

class PDFProcessor:
    def __init__(self, pdf_path: str):
        """Initialize the PDF processor with the path to the PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        self.pdf_path = pdf_path
        self._validate_file()
    
    def _validate_file(self):
        """Validate that the PDF file exists and is accessible."""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found at {self.pdf_path}")
        if not self.pdf_path.lower().endswith('.pdf'):
            raise ValueError("File must be a PDF")
    
    def extract_text(self, page_start: int = 1, page_end: int = 10) -> List[Dict[str, str]]:
        """Extract text from the PDF file, organizing by pages.
        
        Args:
            page_start (int): Page number to start extraction from (default: 1)
            page_end (int): Page number to end extraction at (default: 10)
            
        Returns:
            List[Dict[str, str]]: List of dictionaries containing page number and text
        """
        extracted_content = []
        
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            pages_to_extract = min(page_end, total_pages)
            
            print(f'Total pages in PDF: {total_pages}')
            print(f'Extracting pages from {page_start} to {pages_to_extract}...')
            
            for page_num in range(page_start - 1, pages_to_extract):
                print(f'Processing page {page_num + 1}...')
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Store page content with metadata
                extracted_content.append({
                    'page_number': page_num + 1,
                    'text': text.strip(),
                })
        
        return extracted_content
    
    def preprocess_text(self, extracted_content: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Preprocess the extracted text for better quality.
        
        Args:
            extracted_content (List[Dict[str, str]]): List of dictionaries with raw text
            
        Returns:
            List[Dict[str, str]]: Preprocessed text with the same structure
        """
        processed_content = []
        
        for page in extracted_content:
            text = page['text']
            
            # Basic preprocessing steps
            text = text.replace('\n\n', ' [PARAGRAPH] ')  # Mark paragraph breaks
            text = ' '.join(text.split())  # Remove extra whitespace
            
            processed_content.append({
                'page_number': page['page_number'],
                'text': text
            })
        
        return processed_content


    
    def write_to_file(self, processed_content: List[Dict[str, str]], filename: str) -> None:
        """Write the preprocessed content to a file.
        
        Args:
            processed_content (List[Dict[str, str]]): Preprocessed content
            filename (str): Name of the file to write to
        """
        if not os.path.isdir('dataset'):
            os.mkdir('dataset')
        
        with open(f'dataset/{filename}.txt', 'w') as f:
            for page in processed_content:
                f.write(f'page number: {page["page_number"]}\n text: {page["text"]}\n\n')

        return


if __name__ == '__main__':
    pdf_processor = PDFProcessor('dataset/lamarsh_baratta-introduction_to_nuclear_engineering_textbook_3rd_edition.pdf')
    extracted_content = pdf_processor.extract_text(page_start=23, page_end=62)
    processed_content = pdf_processor.preprocess_text(extracted_content)
    pdf_processor.write_to_file(processed_content, filename='ch2_processed')

