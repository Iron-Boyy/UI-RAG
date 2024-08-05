import sqlite3
import os
import logging
import json5
from typing import List, Dict

import hashlib

def generate_md5_string(input_string):
    # 创建一个 md5 哈希对象
    hash_object = hashlib.md5()
    # 提供要哈希的数据（需要是字节类型）
    hash_object.update(input_string.encode('utf-8'))
    # 获取十六进制格式的哈希值
    md5_hash = hash_object.hexdigest()
    return md5_hash


class DocumentDatabase():
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.init()

    def init(self):
        if not os.path.exists(self.db_path):
            logging.info(">>>>>>>>> database not found, creating new one...")
        else:
            logging.info(">>>>>>>>> database found! use it directly...")
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()
        self.creat_table()
    
    def creat_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ChunkMapping 
                            (id  INTEGER PRIMARY KEY AUTOINCREMENT, 
                            vec_index INTEGER,
                            chunk_content  TEXT, 
                            chapter  TEXT, 
                            page  INTEGER)''')
    
    def add(self, vec_index: int, chunk_content:str, chapter: str, page: int, commit=True) -> None:
        '''
            添加文档
        '''
        INSERT_CMD = f'''INSERT INTO ChunkMapping (vec_index, chunk_content, chapter, page) VALUES (?, ?, ?, ? )'''   

        self.cursor.execute(INSERT_CMD,(vec_index,chunk_content, chapter, page))
        if commit:
            self.connect.commit()
    
    def commit(self) -> None:
        self.connect.commit()

    
    def add_one_passage(self, passage:List[Dict] ) -> None:
        for _passgae in passage:
            self.add(_passgae['vec_id'],_passgae['content'], _passgae['chapter'], _passgae['page'],commit=False)
        self.connect.commit()

        print("{} contents added".format(len(passage)))
    
    
    def search_with_vec_index(self, chunk_id: int, return_info: list = ['*']):
        self.cursor.execute(f"SELECT {','.join(return_info)} FROM ChunkMapping WHERE vec_index=?", (chunk_id,))
        table_info = [description[0] for description in self.cursor.description]

        result = self.cursor.fetchall()

        if result:
            return table_info,result
        else:
            return None
    
    def get_total_contents(self):
        self.cursor.execute(f"SELECT chunk_content FROM ChunkMapping")
        result = self.cursor.fetchall()
        return result

    
    def __del__(self):
        self.cursor.close()
        self.connect.close()



class FileDatabase():

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

        self.init()
    def init(self):
        if not os.path.exists(self.db_path):
            logging.info(">>>>>>>>> database not found, creating new one...")
        else:
            logging.info(">>>>>>>>> database found! use it directly...")
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()
        self.creat_table()
    
    def creat_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS FileInfo 
                            (id  INTEGER PRIMARY KEY AUTOINCREMENT, 
                            kbname  TEXT, 
                            filename  TEXT, 
                            md5  TEXT, 
                            filesize  INTEGER, 
                            deleted  INTEGER)''' )
    
    def add(self, kbname:str, filename:str, md5:str, filesize:str, deleted:int = 0, commit=True) -> None:
        INSERT_CMD = f'''INSERT INTO FileInfo (kbname, filename, md5, filesize, deleted) VALUES (?, ?, ?, ?,? )'''   
        self.cursor.execute(INSERT_CMD,(kbname, filename, md5, filesize,deleted))
        if commit:
            self.connect.commit()
    
    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def view(self, md5):
        self.cursor.execute("SELECT * FROM FileInfo WHERE md5=?", (md5,))
        table_info = [description[0] for description in self.cursor.description]

        result = self.cursor.fetchall()
        if result:
            return table_info,result
        else:
            return None

    
    def search_with_name(self, filename: str, return_info: list = ['*']):
        self.cursor.execute(f"SELECT {','.join(return_info)} FROM FileInfo WHERE filename=?", (filename,))
        table_info = [description[0] for description in self.cursor.description]

        result = self.cursor.fetchall()
        if result:
            return table_info,result
        else:
            return None
    

    def search_with_md5(self, md5: str, return_info: list = ['*']):
        self.cursor.execute(f"SELECT {','.join(return_info)} FROM FileInfo WHERE md5='{md5}'")
        table_info = [description[0] for description in self.cursor.description]

        result = self.cursor.fetchall()
        if result:
            return table_info,result
        else:
            return None
        
    def delete_with_name(self, filename: str, commit=True) -> None:
        DELETE_CMD = f'''DELETE FROM FileInfo WHERE filename=?'''   
        self.cursor.execute(DELETE_CMD, (filename,))
        if commit:
            self.connect.commit()
    




if __name__ == '__main__':




    passage = [
        {
            "content": "这是一个测试1",
            "chapter": "测试1",
            "page": 1,
            "vec_id": 1
        },
        {
            "content": "这是一个测试2",
            "chapter": "测试2",
            "page": 2,
            "vec_id": 2
        }
    ]

    db = DocumentDatabase("test.db")

    db.add_one_passage(passage)

    text = "重回镜像之维：生成式AI浪...a的技术逻辑与媒介生态迭代_陈文泰.pdf"
    md5_s = generate_md5_string(text)   
