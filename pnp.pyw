from sys import argv
import pypdf as pdf
from fitz import open as img_open
from PIL import Image
import io, os, re

page_format = (2480, 3508)

class PrintNPlay:
    def __init__(self):
        self.images = []
        
    def add_image(self, image, repeat=None):
        if isinstance(image, str):
            with open(image, "rb") as f:
                image = f.read()
        if isinstance(image, bytes):
            image = io.BytesIO(image)
        if repeat:
            self.images.append((image, repeat))
            return
        self.images.append(image)
            
    def add_images(self, images):
        for image in images:
            self.add_image(image)
            
    def close(self):
        for image in self.images:
            image.close()
    
    def get_pages(self):
        images = self.images
        pages = []
        page = Image.new("RGBA", page_format, (0, 0, 0, 0))
        remain_len, complete_height = page_format
        remain_len -= 20
        offset = 10
        height = 10
        next_height = 0
        image_nr = 0
        repeat = 0
        while images or repeat:
            if repeat <= 0:
                image = images.pop(0)
                if isinstance(image, tuple):
                    repeat = image[1]
                    image = Image.open(image[0])
                else:
                    repeat = 1
                    image = Image.open(image)
                image_nr += 1
            fits = False
            if remain_len >= image.size[0] + 3:
                fits = True
                next_height = max(next_height, height + image.size[1] + 3)
                remain_len -= image.size[0] + 3
            elif complete_height >= next_height + image.size[1] + 3:
                fits = True
                remain_len = page_format[0] - (image.size[0] + 3)
                remain_len -= 20
                offset = 10
                height = next_height
                next_height = max(next_height, height + image.size[1] + 3)
            if not fits:
                pages.append(page)
                page = Image.new("RGBA", page_format, (0, 0, 0, 0))
                remain_len, complete_height = page_format
                remain_len -= 20
                offset = 10
                height = 10
                next_height = 0
                fits = False
                if remain_len >= image.size[0] + 3:
                    fits = True
                    next_height = max(next_height, height + image.size[1] + 3)
                    remain_len -= image.size[0] + 3
                elif complete_height >= next_height + image.size[1] + 3:
                    fits = True
                    remain_len = page_format[0] - (image.size[0] + 3)
                    remain_len -= 20
                    offset = 10
                    height = next_height
                    next_height = max(next_height, height + image.size[1] + 3)
            if not fits:
                raise ValueError("Image Nr. {image_nr} is too big.")
            page.paste(image, (offset, height))
            repeat -= 1
            offset += image.size[0] + 3
        pages.append(page)
        _pages = [io.BytesIO() for page in pages]
        for page, _page in zip(pages, _pages):
            page.save(_page, "PNG")
        return _pages
    
    def get_pdf(self):
        pages = self.get_pages()
        pdf_file = pdf.PdfWriter()
        for page in pages:
            pdf_page = pdf.PdfReader(io.BytesIO(img_open(stream=page, filetype="PNG").convert_to_pdf())).pages[0]
            pdf_file.add_page(pdf_page)
        return pdf_file
    
    def write_pdf(self, file):
        pdf_file = self.get_pdf()
        pdf_file.write(file)
        
if __name__ == "__main__":
    if len(argv) >= 2:
        os.chdir(argv[1])
    else:
        os.chdir("images")
    if len(argv) >= 3:
        target = argv[2]
    else:
        target = "../PrintNPlayTemplate.pdf"
    pdf_writer = PrintNPlay()
    for image in os.listdir():
        if not image.endswith(("PNG", "JPEG", "PPM", "GIF", "TIFF", "BMP", "png", "jpeg", "ppm", "gif", "tiff", "bmp", "JPG", "jpg")):
            continue
        repeat = int(match[1]) if (match := re.match(r"(\d+)X", image)) else None
        pdf_writer.add_image(image, repeat)
    pdf_writer.write_pdf(target)