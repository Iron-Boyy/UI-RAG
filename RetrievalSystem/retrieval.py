from database import FileDatabase, DocumentDatabase, generate_md5_string, IndexDatabase
from embedding import get_embedding, BgeEmbedding

from dataloader import PDFLoader
from docsplitter import split_text_internal
import os

from typing import List, Dict
import shutil
import tqdm
import json
from copy import deepcopy
import os

import time

from runner import call_intern_general, call_intern_summary, call_intern_qa

class DocumentRetrieval():
    def __init__(self, dim, cache_dir = "./cache", emd_path="", override_db=False) -> None:
        self.dim = dim
        self.cache_dir = cache_dir
        self.mkdir_if_not_exist(cache_dir)
        self.override_db = override_db

        self.doc_db = None
        self.file_db = None
        self.index_db = None

        self.file_db = FileDatabase(db_path=os.path.join(self.cache_dir,"file_database.db"))

        if emd_path != "":
            self.emd_model = BgeEmbedding(emd_path)
            self.get_embedding = self.emd_model.encode
        else:
            self.get_embedding = get_embedding

    def mkdir_if_not_exist(self, path):
        try:
            os.makedirs(path)
        except FileExistsError:
            print("Directory already exists")

    def init_database(self, db_name):
        if os.path.exists(os.path.join(self.cache_dir,f"{db_name}_text.db")):
            os.remove(os.path.join(self.cache_dir,f"{db_name}_text.db"))
            os.remove(os.path.join(self.cache_dir,f"{db_name}_index.db"))
        self.doc_db = DocumentDatabase(db_path=os.path.join(self.cache_dir,f"{db_name}_text.db"))
        self.index_db = IndexDatabase(db_path=os.path.join(self.cache_dir,f"{db_name}_index.db"), dim=self.dim)

    def _upload_document(self, file_path):
        loader = PDFLoader()
        ret = loader.load_document(doc_path=file_path)
        if ret != 'Success':
            raise Exception('Error loading document')
        document_loaded = loader.extract_doc_content()       
        loader.unload_document()

        return document_loaded

    def _split_document(self, document, chunk_size):
        
        chunk_list_all = []
        total_content = ""
        for page in document['doc_content']:
            page_num = page['page_num']
            page_content = page['page_content']
            total_content += page_content
            chunk_list = split_text_internal(page_content, chunk_size)

            chunk_list_all.append((page_num,chunk_list))
        
        filesize = self.cal_filesize(total_content)

        return chunk_list_all,filesize
    
    # def json2chunk(self, document):


    

    def cal_filesize(self, text):
        return len(text.encode('utf-8'))


    def add_document(self, file_path, databasename,chunk_size = 2000):


        self.init_database(databasename)
        chunk_list_all = []
        for i in range(len(file_path)):
            chunk_list = []
            for j in range(len(file_path[i]['功能'])):
                chunk = deepcopy(file_path[i])
                chunk['功能'] = file_path[i]['功能'][j]
                chunk_list.append(str(chunk))
            chunk_list_all.append((i,chunk_list))
        
        index = 0
        for (page_num, chunks) in tqdm.tqdm(chunk_list_all):
            for chunk in chunks:
                embedding = self.get_embedding(chunk)
                self.index_db.add(embedding,[index])
                self.doc_db.add(index,chunk,"",page_num,commit=False)
                index += 1
        
        self.index_db.save()
        self.doc_db.commit()
        # filename = os.path.basename(file_path)
        # md5_name = generate_md5_string(filename)

        # check_result = self.file_db.search_with_md5(md5_name)

        # if check_result is not None and self.override_db:
        #     print("File already exists, use overrider to delete the database")
        #     self.del_document(file_path)
        # elif check_result is not None:
        #     print("File already exists, return")
        #     self.init_database(md5_name)
        #     return
        
        # time.sleep(1)

        # self.init_database(md5_name)


        # document_loaded = self._upload_document(file_path)
        # chunk_list_all, filesize = self._split_document(document_loaded, chunk_size)

        # self.file_db.add(md5_name,filename, md5_name, filesize)


        # index = 0
        # for (page_num, chunks) in tqdm.tqdm(chunk_list_all):
        #     for chunk in chunks:
        #         embedding = self.get_embedding(chunk)
        #         self.index_db.add(embedding,[index])
        #         self.doc_db.add(index,chunk,"",page_num,commit=False)
        #         index += 1
        
        # self.index_db.save()
        # self.doc_db.commit()
    

    def del_document(self, file_path):
        
        filename = os.path.basename(file_path)
        md5_name = generate_md5_string(filename)
        
        if self.file_db is None:
            self.file_db = FileDatabase(db_path=os.path.join(self.cache_dir,"file_database.db"))

        result = self.file_db.search_with_name(filename, return_info=['kbname'])

        if result is None:
            print("Document not found, return")
        else:
            _, kbname = result
            kbname = [x[0] for x in kbname]
            for _kbname in kbname:

                if os.path.exists(os.path.join(self.cache_dir, f"{_kbname}_text.db")):
                    os.remove(os.path.join(self.cache_dir, f"{_kbname}_text.db"))
                if os.path.exists(os.path.join(self.cache_dir, f"{_kbname}_index.db")):
                    os.remove(os.path.join(self.cache_dir, f"{_kbname}_index.db"))
            self.file_db.delete_with_name(filename)

    def search_document(self, query, top_k = 2, threshold=None):
        base_embedding = self.get_embedding(query)
        print(base_embedding)

        query_len = base_embedding.shape[0]
        print(query_len)
        result = self.index_db.search(base_embedding, top_k)
        print(result)
        
        distances = result[0][0]
        indexes = result[1][0]
        result = [(x,y) for (x,y) in zip(distances, indexes)]
        if threshold is not None:
            result = [(x,y) for (x,y) in result if x >= threshold]

        
        retrieval_content_list = []
        retrieval_page_list = []
        retrieval_score_list = []
        
        for (distance, index) in result:
            _, chunk_info = self.doc_db.search_with_vec_index(index, return_info=['chunk_content','page'])
            if chunk_info.__len__() == 1:
                chunk_info = [x for x in chunk_info[0]]

                retrieval_content_list.append(chunk_info[0])
                retrieval_page_list.append(chunk_info[1])
                retrieval_score_list.append(distance)


        return {
            "content": retrieval_content_list,
            "page": retrieval_page_list,
            "score": retrieval_score_list
        }
    
    

    def template_with_qa(self, query, content_dict):

        content_len = content_dict['content'].__len__()
        content_list = "[no_ref]{}\n" * content_len
        content_list_completed = content_list.format(*content_dict['content'])
        max_score = max(content_dict['score'])

        prompt = '''请参考以下知识回复用户最新的问题，参考程度为：{}，在生成时注明所引用的知识的角标，前缀为[no_ref]的知识无需注明。
{}
问题：{}
'''
        return prompt.format(max_score, content_list_completed, query)



    def chat_general(self, query):

        content_dict = self.search_document(query)

        query_prompt = self.template_with_qa(query, content_dict)

        print(query_prompt)

        return call_intern_general(query_prompt)
    

    def chat_qa(self, query):

        content_dict = self.search_document(query, top_k=2)
        print(11111111111111111111111)
        print(content_dict)
        print(11111111111111111111111)

        content_list = '\n-split\n'.join(content_dict['content'])
        print(content_list)
        print(11111111111111111111111)
        response = call_intern_qa(query, content_list)

        return response


    def chat_summary(self, index = 0):
        result = self.doc_db.get_total_contents()      
        result = [x[0] for x in result]
        all_content = ''.join(result)
        content_list = split_text_internal(all_content, 2000)

        for i ,_content in enumerate(content_list):

            _content = _content.strip()
            if _content.endswith('，'):
                _content = _content[:-1] + '...'
            response = call_intern_summary(_content)
            print(response)
        return response




if __name__ == '__main__':


    filepath = "./asserts/【4】商汤科技董事长兼CEO徐立：AI 2.0时代的 “新质生产力工具”.pdf"
    filepath = "/mnt/afs/home/luozhihao/intent_pipeline/RetrievalSystem/Yao 等 - 2023 - ReAct Synergizing Reasoning and Acting in Languag.pdf"

    with open('/mnt/afs/home/luozhihao/intent_pipeline/RetrievalSystem/file.json') as user_file:
        file = user_file.read()
    
    file = file[1:-1].split("},\n  {")
    for i in range(len(file)):
        if i == 0 :
            file[i] = file[i].replace("\n","").replace("    ","")+"}"
        elif i == len(file)-1:
            file[i] = "{" + file[i].replace("\n","").replace("    ","")
        else:
            file[i] = "{" + file[i].replace("\n","").replace("    ","") + "}"
        file[i] = json.loads(file[i])
    


    db_sys = DocumentRetrieval(512, emd_path="/mnt/afs/home/luozhihao/intent_pipeline/RetrievalSystem/bge-small-zh-v1.5", override_db=True)

    db_sys.add_document(file, "本地操作", chunk_size=200)

    # db_sys.chat_qa("调高屏幕亮度到80%并开启夜间模式")




    while True:


        query = input()

        if query == 'q':
            break

        response = db_sys.chat_qa(query)

        print(response)