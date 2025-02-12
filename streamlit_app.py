import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_data(show_spinner=False)
def extract_pages_from_pdf(pdf_bytes):
    """
    Extracts pages from an uploaded PDF file and returns a list of PIL Image objects.
    Logs detailed information about each processed page.
    
    Args:
        pdf_bytes (bytes): PDF file content in bytes.
            Example: open('sample.pdf', 'rb').read()
    
    Returns:
        List[PIL.Image.Image]: List of images representing each PDF page.
            Example: [<PIL.Image.Image image mode=RGB size=1240x1754 at 0x...>, ...]
    """
    try:
        logger.info("Starting extraction of pages from PDF.")
        pages = convert_from_bytes(pdf_bytes)
        total_pages = len(pages)
        logger.info(f"Extracted {total_pages} page(s) from the PDF.")

        # Log details for each extracted page
        for index, page in enumerate(pages):
            logger.info(f"Page {index + 1}: size={page.size}, mode={page.mode}")
        return pages
    except Exception as e:
        logger.error("Error extracting pages from PDF", exc_info=True)
        st.error("Failed to extract pages from PDF.")
        return []

def perform_ocr_on_image(image):
    """
    Performs Optical Character Recognition (OCR) on an image to extract text.
    
    Args:
        image (PIL.Image.Image): The input image to process.
            Example: Image.open('page1.png')
    
    Returns:
        str: Extracted text from the image.
            Example: "This is the text extracted via OCR from the image."
    """
    try:
        logger.info("Starting OCR extraction for the selected page.")
        text = pytesseract.image_to_string(image)
        logger.info("OCR extraction completed successfully.")
        logger.debug(f"OCR extracted text: {text[:100]}...")  # Log first 100 characters for brevity
        return text
    except Exception as e:
        logger.error("Error during OCR extraction", exc_info=True)
        return "OCR extraction failed."

def extract_table_from_image(image):
    """
    Simulates the extraction of table data from an image.
    (Mockup API template for table extraction)
    
    Args:
        image (PIL.Image.Image): The input image from which to extract table data.
            Example: Image.open('page1.png')
    
    Returns:
        pd.DataFrame: A pandas DataFrame representing the extracted table.
            Example: pd.DataFrame({'Column1': [1,2], 'Column2': ['A','B']})
    """
    try:
        logger.info("Starting simulated table extraction from the image.")
        # For demonstration, return a dummy table
        data = {
            "Column1": [1, 2, 3],
            "Column2": ["A", "B", "C"]
        }
        df = pd.DataFrame(data)
        logger.info("Simulated table extraction completed.")
        logger.debug(f"Extracted table data:\n{df.head()}")
        return df
    except Exception as e:
        logger.error("Error during table extraction", exc_info=True)
        return pd.DataFrame()

def detect_images_in_page(image):
    """
    Simulates the detection of images within a PDF page.
    (Mockup API template for image detection)
    
    Args:
        image (PIL.Image.Image): The input page image.
            Example: Image.open('page1.png')
    
    Returns:
        List[PIL.Image.Image]: List of detected image snippets.
            Example: [<PIL.Image.Image image mode=RGB size=200x200 at 0x...>, ...]
    """
    try:
        logger.info("Starting simulated image detection in the page.")
        # For demonstration, we return the full page as the detected image.
        detected_images = [image]
        logger.info(f"Simulated image detection completed: {len(detected_images)} image(s) detected.")
        return detected_images
    except Exception as e:
        logger.error("Error during image detection", exc_info=True)
        return []

def chat_with_openai(prompt, table_data):
    """
    Simulates a chat interaction with OpenAI to manipulate table data.
    (Mockup API template for OpenAI chat)
    
    Args:
        prompt (str): The instruction for table manipulation.
            Example: "Add a computed column based on Column1."
        table_data (pd.DataFrame): The extracted table data.
            Example: pd.DataFrame({'Column1': [1,2,3], 'Column2': ['A','B','C']})
    
    Returns:
        str: Simulated response from OpenAI.
            Example: "New column 'Computed' added with values [2,4,6]."
    """
    try:
        logger.info("Simulating chat with OpenAI.")
        logger.info(f"User prompt: {prompt}")
        # Simulated response based on the prompt and table data
        response = f"Simulated response: Processed table with instruction '{prompt}'."
        logger.info("Simulated chat with OpenAI completed.")
        return response
    except Exception as e:
        logger.error("Error during chat with OpenAI", exc_info=True)
        return "Chat interaction failed."

def generate_new_table_from_chat(chat_response, table_data):
    """
    Generates a new table by manipulating the original table based on the chat response.
    (Mockup API template for table generation)
    
    Args:
        chat_response (str): The response from the chat API.
            Example: "New column 'Computed' added with values [2,4,6]."
        table_data (pd.DataFrame): The original extracted table.
            Example: pd.DataFrame({'Column1': [1,2,3], 'Column2': ['A','B','C']})
    
    Returns:
        pd.DataFrame: A new pandas DataFrame after manipulation.
            Example: pd.DataFrame({'Column1': [1,2,3], 'Column2': ['A','B','C'], 'Computed': [2,4,6]})
    """
    try:
        logger.info("Generating new table based on chat response.")
        # For demonstration, add a new column 'Computed' by doubling 'Column1'
        if 'Column1' in table_data.columns:
            table_data['Computed'] = table_data['Column1'] * 2
            logger.info("New table generated with an additional 'Computed' column.")
        else:
            logger.warning("Column1 not found in table data; cannot generate new table.")
        logger.debug(f"New table data:\n{table_data.head()}")
        return table_data
    except Exception as e:
        logger.error("Error during new table generation", exc_info=True)
        return table_data

def main():
    """
    Main function to run the Streamlit OCR + GenAI app.
    The app allows users to:
      - Import a PDF and display its pages in the sidebar.
      - For the selected page, view OCR extracted text, a simulated extracted table, and detected images.
      - Chat with OpenAI (simulation) to manipulate the extracted table, generate a new table, and download it.
    """
    st.title("OCR + GenAI PDF Processing App with Detailed Logging")

    # --- Sidebar: Upload PDF and Select Page ---
    st.sidebar.header("Upload PDF")
    pdf_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

    if pdf_file is not None:
        logger.info("PDF file uploaded by user.")
        pdf_bytes = pdf_file.read()
        logger.info("PDF file read into bytes.")
        pages = extract_pages_from_pdf(pdf_bytes)
        total_pages = len(pages)
        if total_pages == 0:
            st.error("No pages found in the uploaded PDF.")
            return

        # Sidebar: Select page number
        page_number = st.sidebar.number_input("Select Page", min_value=1, max_value=total_pages, value=1, step=1)
        selected_page = pages[page_number - 1]
        logger.info(f"User selected page {page_number} of {total_pages}.")

        # Display current page information
        st.subheader(f"Page {page_number} of {total_pages}")

        # --- Main Section: Tabs for Text, Table, and Images ---
        tab_text, tab_table, tab_images = st.tabs(["Text", "Table", "Images"])

        with tab_text:
            st.write("**Extracted Text:**")
            extracted_text = perform_ocr_on_image(selected_page)
            st.text_area("OCR Result", extracted_text, height=300)

        with tab_table:
            st.write("**Extracted Table:**")
            table_df = extract_table_from_image(selected_page)
            st.dataframe(table_df)

            # Button to download the extracted table as CSV
            csv_data = table_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Table as CSV",
                data=csv_data,
                file_name="extracted_table.csv",
                mime="text/csv"
            )

        with tab_images:
            st.write("**Detected Images:**")
            detected_imgs = detect_images_in_page(selected_page)
            for idx, img in enumerate(detected_imgs):
                st.image(img, caption=f"Detected Image {idx + 1}", use_column_width=True)

        st.markdown("---")
        # --- Chat Section: Manipulate and Generate New Table ---
        st.header("Chat with OpenAI for Table Manipulation")
        chat_input = st.text_input("Enter instruction for table manipulation", 
                                   value="Add a computed column based on Column1")
        if st.button("Send to OpenAI"):
            # Simulate chat interaction
            chat_response = chat_with_openai(chat_input, table_df)
            st.write("**OpenAI Response:**")
            st.write(chat_response)

            # Generate new table based on the chat response
            new_table = generate_new_table_from_chat(chat_response, table_df.copy())
            st.write("**New Generated Table:**")
            st.dataframe(new_table)

            # Download button for the new table
            new_csv = new_table.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download New Table as CSV",
                data=new_csv,
                file_name="new_generated_table.csv",
                mime="text/csv"
            )
    else:
        logger.info("No PDF file uploaded yet.")
        st.info("Please upload a PDF file to begin processing.")

if __name__ == '__main__':
    main()
