import os, re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image

import pypdfium2 as pdfium

import io

def extract_tags(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'r') as f:
        raw_content = f.read()
        return re.findall(r'(?<=- ).+', raw_content)

def find_file_in_directory(file_name, directory):
    print("starting find_file_in_directory")

    for root, dirs, files in os.walk(directory):
        if file_name in files:
            print("found file in directory")
            return os.path.join(root, file_name)
    print("did not find file in directory")
    return None


def find_files_in_directory(file_names, directory):
    print("starting find_files_in_directory")

    found_files = {}
    for root, dirs, files in os.walk(directory):
        for file_name in file_names:
            if file_name in files:
                found_files[file_name] = os.path.join(root, file_name)
    print("finished finding files in directory")
    for key, value in found_files.items():
        print(f"key: {key}, value: {value}")
    # check what files are not found
    for file_name in file_names:
        if file_name not in found_files:
            print(f"Could not find file: {file_name}")

    return found_files

def pdf_to_images(pdf_path, images):
    # Open the PDF file
    pdf = pdfium.PdfDocument(pdf_path)
    n_pages = len(pdf)
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        image = page.render(
            scale=1,
            rotation=0,
            crop=(0, 0, 0, 0)
        )
        PIL_image = image.to_pil()
        # save it to a temporary file
        PIL_image.save(f"temp{page_number}.png")

        images.append((PIL_image, f"temp{page_number}.png"))

def addimage(c, img, y_position, file_path, width=500, height=500):
    img_width, img_height = img.size
    aspect_ratio = img_height / float(img_width)
    new_width = width - 80  # Assuming 40px margin on each side
    new_height = aspect_ratio * new_width
    c.drawImage(file_path, 40, y_position - new_height, width=new_width, height=new_height)
    y_position -= (new_height + 20)

    if y_position < 40:  # New page if not enough space
        c.showPage()
        y_position = height - 30
    
    return y_position

def convert_markdown_to_pdf(md_strings, vault_path, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter

    # fetch the path of all links that are needed:
    files_to_find = []
    for md_string in md_strings:
        for line in md_string.split('\n'):
            line = line.strip()
            if '![[' in line and ']]' in line:
                # Extract filename and find file path from where ![[ends and ]] starts
                file_name_start_index = line.index('![[') + 3
                file_name_end_index = line.index(']]')
                filename = line[file_name_start_index:file_name_end_index]
                files_to_find.append(filename)
    
    found_files = find_files_in_directory(files_to_find, vault_path)

    for md_string in md_strings:
        y_position = height - 30  # Starting y position for writing text

        for line in md_string.split('\n'):
            line = line.strip()
            print("line: ", line)

            if '![[' in line and ']]' in line:
                # Extract filename and find file path from where ![[ends and ]] starts
                file_name_start_index = line.index('![[') + 3
                file_name_end_index = line.index(']]')
                filename = line[file_name_start_index:file_name_end_index]

                print("filename: ", filename)
                if filename in found_files.keys():
                    file_path = found_files[filename]
                else:
                    c.drawString(40, y_position, "Could not find file: " + filename)
                    y_position -= 20

                if file_path and file_path.endswith('.png'):
                    with Image.open(file_path) as img:
                        y_position = addimage(c, img, y_position, file_path, width, height)

                elif file_path and file_path.endswith('.pdf'):
                    images = []
                    pdf_to_images(file_path, images)
                    for img, pth in images:
                        y_position = addimage(c, img, y_position, pth, width, height)

            else:
                c.drawString(40, y_position, line)
                y_position -= 20

            if y_position < 40:  # New page if not enough space
                c.showPage()
                y_position = height - 30
            
        c.showPage()

    c.save()
    print("PDF created successfully!")