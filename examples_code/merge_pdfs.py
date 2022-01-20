from pathlib import Path
from PyPDF2 import PdfFileMerger

pdfs = Path(r"pdfs")  # r"D:\OneDrive\PyCodes\MEEST_API\pdfs"

#    merger is used for merging multiple files into one and merger.append(absfile)
#    will append the files one by one until all pdfs are appended in the result file.
merger = PdfFileMerger(strict=False)

#   result.pdf is the one single output files of all the pdfs and can be accessed
#  in the path where you will save the python file.


for file in pdfs.iterdir():
    if file.suffix == ".pdf":
        path_with_file = str(file)
        print(path_with_file)
        merger.append(path_with_file,  import_bookmarks=False)

merger.write("result.pdf")
merger.close()
