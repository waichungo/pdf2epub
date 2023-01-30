from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.layout import LAParams, LTTextBox, LTFigure, LTTextLine, LTChar, LTImage, LTPage

from pdfminer.image import ImageWriter
from pdfminer.converter import PDFPageAggregator
import time
import io

path = r'D:\documents\Cracking the Coding Interview 189 Programming Questions and Solutions by Gayle Laakmann McDowell (z-lib.org).pdf'
# path = r'C:\Users\James\Downloads\Documents\Frontend Unicorn ( etc.) (z-lib.org).pdf'


class TextStyle:
    fontFamily = ""
    fontSize = 12
    fontWeight = 500
    color=""

# from PyPDF2 import PdfReader

# def extract_information(pdf_path):
#     currPage=0
#     with open("parsed.txt","w") as file:
#         with open(pdf_path, 'rb') as f:
#             pdf = PdfReader(f)
#             information = pdf.metadata
#             number_of_pages = len(pdf.pages)

#             for page in pdf.pages:
#                 parts.clear()
#                 currPage+=1
#                 page.extract_text(visitor_text=visitor_body)
#                 text_body = "".join(parts)
#                 print(text_body)
#                 try:
#                     file.write(f"\nPage {currPage}:\n\n")
#                     file.write(text_body)

#                     file.write("\n")
#                 except Exception as ex:
#                     print("error ocurred")
#                     print(ex)
#                 print("\n")


#     txt = f"""
#     Information about {pdf_path}:

#     Author: {information.author}
#     Creator: {information.creator}
#     Producer: {information.producer}
#     Subject: {information.subject}
#     Title: {information.title}
#     Number of pages: {number_of_pages}
#     """

#     print(txt)
#     return information

# parts = []


# def visitor_body(text, cm, tm, fontDict, fontSize):
#     y = tm[5]
#     if y > 50 and y < 720:
#         parts.append(text)


# if __name__ == '__main__':
#     path = r'D:\documents\Cracking the Coding Interview 189 Programming Questions and Solutions by Gayle Laakmann McDowell (z-lib.org).pdf'
#     extract_information(path)

# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument

# def parse(filename, maxlevel):
#     with open(filename, 'rb') as fp:
#         with open("outlines.txt", 'w') as tocF:
#             parser = PDFParser(fp)
#             doc = PDFDocument(parser=parser)
#             parser.set_document(doc)


#             outlines = doc.get_outlines()
#             for (level, title, dest, a, se) in outlines:
#                 if dest is not None:
#                     print("found dest")
#                 if level <= maxlevel:
#                     pref="\t"*(level-1) if level > 1  else ""
#                     data=pref+title+"\n"
#                     print(data)
#                     tocF.write(data)


# if __name__ == '__main__':
#     import sys
#     # print ('Usage: %s xxx.pdf level' % )
#     # sys.exit(2)

#     parse(path, 8)
def get_page_text(page):
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    retstr = io.StringIO()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    interpreter.process_page(page)
    text = retstr.getvalue()
    device.close()
    retstr.close
    return text


def get_page_text2(page):
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    interpreter.process_page(page)
    layout = device.get_result()
    for lobj in layout:
        if isinstance(lobj, LTTextBox):
            x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()

            print('At %r is text: %s' % ((x, y), text))
    return text


def get_page_text3(page: LTPage):
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    interpreter.process_page(page)
    layout = device.get_result()
    content = ""
    for obj in layout:
        if isinstance(obj, LTTextBox):
            for o in obj._objs:
                if isinstance(o, LTTextLine):

                    text = o.get_text()
                    content += text
                    if text.strip():
                        for c in o._objs:
                            if isinstance(c, LTChar):
                                print("fontname %s" % c.fontname)
        # if it's a container, recurse
        elif isinstance(obj, LTFigure):
            for o in obj._objs:
                if isinstance(o, LTImage):
                    iw = ImageWriter('./images')
                    iw.export_image(o)

            # content+=get_page_text3(obj._objs)
            pass
        else:
            pass
    return content


def convert_pdf_to_txt(path):

    fp = open(path, 'rb')

    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    pages = PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                              password=password,
                              caching=caching,
                              check_extractable=True)
    start = time.time()
    for i, page in enumerate(pages):
        page_no = i+1
        text = get_page_text3(page)
        if i > 20:
            break
    fp.close()

    return text


convert_pdf_to_txt(path)
