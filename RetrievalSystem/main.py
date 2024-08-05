from dataloader import PDFLoader
from docsplitter import split_text_internal

from runner import call_intern_summary, call_intern_qa

if __name__ == '__main__':

    response = call_intern_summary(query="我今天不想上班了！！！！")
    print(response)

    filepath = "../../pdf文档及问题/【3】用AI写研报哪家强？沙利文《2023中国大模型行研能力评测报告》商汤日日新·商量获评第一.pdf"

    # filepath = "../../pdf文档及问题\【4】商汤科技董事长兼CEO徐立：AI 2.0时代的 “新质生产力工具”.pdf"
    loader = PDFLoader()

    loader.load_document(filepath)
    document = loader.extract_doc_content()
    loader.unload_document()

    print(document.keys())

    
    total_content = ""

    for page in document['doc_content']:
        total_content += page['page_content']
    print(total_content.__len__())

    for page in document['doc_content']:
        num = page['page_num']
        content = page['page_content']

        data_list = split_text_internal(content, 2000, ver=True)

        for i, data in enumerate(data_list):
            # a trick, but effective 
            data = data.strip()
            if data.endswith('，'):
                data = data[:-1] + '...'
            #trick end
            response = call_intern_summary(data)

            if len(response) >= 1000:
                print(data)

            print(response)
            print(f"Page {num}")