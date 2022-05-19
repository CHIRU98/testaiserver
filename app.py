from detailed_file import DetailFileComparator

import os
import textract

def read_file(file_path):
    extension = file_path.split('.')[-1]
    text = textract.process(file_path, extension=extension).decode('utf-8')
    return text

test_data1 = read_file("test1.pdf")
test_data2 = read_file("test2.pdf")
obj = DetailFileComparator()
obj.file_detail_comparator(test_data1,test_data2)