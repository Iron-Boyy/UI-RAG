import os

class TXTLoader:
    def __init__(self):
        self.document_loaded = False
        self.doc_path = ""
        self.file = None

    def load_document(self, doc_path):
        if self.document_loaded:
            print("already loaded")
            return "Success"

        self.file = open(doc_path, 'r')
        if not self.file:
            print(f"load {doc_path} failed")
            return "InvalidArgs"

        self.document_loaded = True
        self.doc_path = doc_path
        return "Success"

    def unload_document(self):
        if not self.document_loaded:
            print("no document loaded")
            return "Success"
        self.file.close()
        self.document_loaded = False
        self.doc_path = ""
        return "Success"

    def extract_doc_content(self):
        if not self.document_loaded:
            print("no document loaded")
            return {}

        doc = {}
        doc['source_path'] = self.doc_path
        doc['doc_type'] = "TXT"

        content = ""
        for line in self.file:
            content += line
            content += '\n'

        doc_page = {}
        doc_page['page_num'] = 1
        doc_page['page_content'] = content
        doc['doc_content'] = [doc_page]

        return doc
