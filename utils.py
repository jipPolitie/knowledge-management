# import dropbox

import os
import io

# pdf to text
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# images:
# import fitz


# path is relative to dropbox root
def get_pdf_from_dropbox(path, img_folder=None):
    pdf_path = path

    if img_folder is None:
        img_folder = 'images/' + path[-14:-4]

    def open_file(path):
        JIP_test_API_key = 'obfuscated, set up github secrets'
        dbx = dropbox.Dropbox(JIP_test_API_key)
        _, res = dbx.files_download(path)
        res.raise_for_status()
        return io.BytesIO(res.content)

    s_obj = open_file(pdf_path)
    return s_obj


def pdf2text(pdf_handle):
    output_string = io.StringIO()
    with pdf_handle as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        # might wanna refactor here...
        image_writer = None
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams(), imagewriter=image_writer)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        return output_string.getvalue()


def save_pdf_images(pdf_handle, img_folder):
    image_list = []

    def create_dir(name):
        try:
            os.makedirs(name)
        except OSError as error:
            # print(error)
            pass

    create_dir(img_folder)
    pdf_file = fitz.open(stream=pdf_handle, filetype='pdf')
    # iterate over PDF pages
    page_cnt = 1
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # save image
            print(img_folder)
            file_path = img_folder + '/' + str(page_cnt) + '_' + str(image_index) + '.' + image_ext
            with open(file_path, 'wb') as file_handler:
                file_handler.write(image_bytes)
            image_list.append(file_path)
        page_cnt += 1
    return image_list


article1 = get_pdf_from_dropbox(
    '/test_sprint_1/from discretion to standardization_digitalization_of_the_police_organization.pdf')
article2 = get_pdf_from_dropbox(
    '/test_sprint_1/factors_influencing_womens_attitudes_towards_computers_in_a_computer_literacy_training_program.pdf')
# print(article1)
# print(article2)
