import fitz
import os
import re

def _postprocess_result(all_text :str):
    space_determine_title_threshold = 3

    print('='* 100)
    final_result = ['']
    types = ['']

    lines = all_text.split("\n")
    l = ""
    n = ""
    for i, s in enumerate(lines):
        if i >= 1:
            l = lines[i - 1]
        if i < len(lines) - 1:
            n = lines[i + 1]
        guess = "normal-line"
        t = ""
        trim = s.replace(" ", "").lower()

        if len(s) == 0:
            guess = "new-line"
        elif re.findall(r'^\s*?第.{1,3}章\s+.+', s):
            guess = "title"
            level = 1
        elif trim == "abstract" or trim == "摘要":
            guess = "title"
            level = 1
        elif re.findall(r'^[一二三四五六七八九十]+\s+.+', s):
            guess = "title"
            level = 2
        elif re.findall(r'^[一二三四五六七八九十]+、\s+.+', s):
            guess = "title"
            level = 2
        # if re.findall(r'^\s*?\d\.?\s+?.+', s):
        #     guess = "title"
        #     level = 1
        elif re.findall(r'^\s*?[IVX]+.?\s+.+', s):
            guess = "title"
            level = 1

        elif re.findall(r'^\s*?第.*?节', s):
            guess = "title"
            level = 2
        elif re.findall(r'^\s*?\d\.', s):
            guess = "title"
            level = 2

        elif re.findall(r'^\s*?\d\.\d.', s):
            guess = "title"
            level = 3
        elif re.findall(r'^\s*?\d\.\d.\d.', s):
            guess = "title"
            level = 3

        elif re.findall(r'^（[一二三四五六七八九十]+）', s):
            guess = "title"
            level = 3

        elif re.findall(r'[A-Z|a-z]+\s$', s) or re.findall(r',\s$', s):
            pass

        elif l.replace(" ", "") == '' and re.findall(r'^\d+$', s):
            guess = "page"
        elif s[-1] == '。' or s[-1] == '.' or s[-1] == ' ' or '....' in s:
            guess = "new-line"

        # if l == '' and re.findall(r'^\d+', s):
        #     s = re.sub(r'^\d+', "", s)

        if "title" in guess:
            if '，' in s:
                # maybe in contents
                guess = "normal-line"

        if (guess == "title" or guess == "new-line") and len(s) < 10 and len(s) and s[-1] != '.':
            if trim != "":
                guess = "table"

        if guess == "title":
            t = '\n{} {}\n'.format('#' * level, s)
        elif guess == "new-line":
            t = '{}\n'.format(s)
        elif guess == "page":
            if final_result[-1].replace(" ", '') == "\n":
                final_result.pop()
                types.pop()
                if len(types) > 0:
                    types[-1] = "append"
        elif guess == "normal-line":
            t = s
        elif guess == "table":
            t = s + "|"

        if guess != "table" and types[-1] == "table":
            t = "\n" + t +"\n"

        if len(types) > 0 and types[-1] == "append":
            if len(final_result[-1]) and final_result[-1][-1] == '\n':
                final_result[-1] = final_result[-1][:len(final_result[-1]) - 1]
                # print('remove new line')
            final_result[-1] += t
            types[-1] = t
        else:
            final_result.append(t)
            types.append(t)
    return ''.join(final_result)

class PDFLoader:
    def __init__(self):
        self.doc = None
        self.doc_path = ""
        self.document_loaded = False

    def load_document(self, doc_path:str=""):

        if not os.path.isfile(doc_path):
            print(f"{doc_path} does not exist or is not a valid file")
            return "InvalidArgs"
        if self.document_loaded:
            print("already loaded")
            return "Success"
        self.doc = fitz.open(doc_path)
    
        if not self.doc:
            print(f"load {doc_path} failed")
            return "InvalidArgs"

        self.document_loaded = True
        self.doc_path = doc_path
        return "Success"
            
    def unload_document(self):
        if not self.document_loaded:
            print("no document loaded")
            return "Success"
        self.doc.close()
        self.document_loaded = False
        self.doc_path = ""
        return "Success"

    def extract_doc_content(self):
        doc = {}
        doc['source_path'] = self.doc_path
        doc['doc_type'] = 'PDF'
        doc['doc_content'] = []
        doc['page_count'] = len(self.doc)

        for i in range(len(self.doc)):
            page = self.doc[i]
            text = page.get_text()
            doc['doc_content'].append({'page_num': i+1, 'page_content': _postprocess_result(text)})
        
        return doc

        
    
if __name__ == '__main__':

    filepath = "../../pdfapi/attention.pdf"
    filepath = "../../pdf文档及问题/【1】商量发布会演示脚本.pdf"
    loader = PDFLoader()

    loader.load_document(filepath)
    document = loader.extract_doc_content()
    loader.unload_document()

    print(document)
