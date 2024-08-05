from doc_db import DocumentDatabase, FileDatabase,generate_md5_string
from faiss_db import IndexDatabase
import numpy as np


if __name__ == '__main__':


    title = "重回镜像之维：生成式AI浪...a的技术逻辑与媒介生态迭代_陈文泰.pdf"
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

    md5_string = generate_md5_string(title)
    file_db = FileDatabase(db_path="file_database.db")
    doc_db = DocumentDatabase(db_path=f"{md5_string}_text.db")
    index_db = IndexDatabase(db_path=f"{md5_string}_index.db", dim=512)

    embeddings = np.random.randn(2,512)
    indexes = [0, 1]

    index_db.add(embeddings, indexes)
    index_db.save()

    file_db.add(md5_string, title, md5_string, 100, 0)

    doc_db.add_one_passage(passage)    


