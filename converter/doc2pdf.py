# doc2pdf.py

# This is open source code, released under the New BSD License -
# see https://michalzalecki.com/converting-docx-to-pdf-using-python/

# This program uses libreoffice and soffice executable file of the libreoffice library.
# libreoffice for Ubuntu or Cent OS
# soffice for Mac OS

import sys
import subprocess
import re

def docx_to_pdf(source, timeout=None):
    args = [libreoffice_exec(), '--headless', '--convert-to', 'pdf', source]

    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    filename = re.search('-> (.*?) using filter', process.stdout.decode())

    if filename is None:
        raise LibreOfficeError(process.stdout.decode())
    else:
        return filename.group(1)

def doc_to_pdf(source, timeout=None):
    return docx_to_pdf(source, timeout=None)

def libreoffice_exec():
    # TODO: Provide support for more platforms
    if sys.platform == 'darwin':
        return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    return 'libreoffice'
    
def usage():

    return "Usage: python doc2pdf.py --headless --convert-to pdf test.doc\n"

class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


def main():
    print('Converted to ' + docx_to_pdf(sys.argv[1]))

if __name__ == '__main__':
    main()

