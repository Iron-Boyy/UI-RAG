import os
import numpy as np
import faiss
import logging

class IndexDatabase():
    def __init__(self, db_path: str, dim: int) -> None:
        
        # 使用faiss inner product index进行向量索引
    
        self.db_path = db_path
        self.dim = dim

        if not os.path.exists(db_path):
            self.create(dim)
            logging.info(">>>>>>>>> cached index not found, creating new one...")
            logging.info(">>>>>>>>> you need add vectors to the index before searching...")
        else:
            logging.info(">>>>>>>>> cached index found! use it directly...")
            self.load(db_path)

    def create(self, dim: int) -> None:
        self.INDEX = faiss.IndexFlatIP(dim)
        self.INDEX = faiss.IndexIDMap(self.INDEX)
    
    def add(self, vectors: np.ndarray, ids: np.ndarray) -> None:
        '''
            添加向量到索引中
            如果索引不存在，则创建新的索引
            如果向量维度与初始化时的维度不匹配，则抛出异常
        '''
        if isinstance(ids, list):
            ids = np.array(ids,dtype=np.int64)

        assert len(vectors) == len(ids), print("向量数量与id数量不匹配")
        #do normalization
        vectors = vectors / np.linalg.norm(vectors, axis=1, ord=2, keepdims=True)

        if not hasattr(self, 'INDEX'):
            self.create(vectors.shape[-1])

        assert vectors.shape[-1] == self.dim, print("向量维度与初始化时的维度不匹配:{} {}".format(vectors.shape[-1], self.dim))
        self.INDEX.add_with_ids(vectors, ids)
    
    def load(self, load_path: str) -> None:
        self.INDEX = faiss.read_index(load_path)

    def save(self, saved_path: str = None) -> None:
        if not saved_path:
            saved_path = self.db_path
        faiss.write_index(self.INDEX, saved_path)

    def search(self, query_vector: np.ndarray, k: int = 1) -> list:
        D, I = self.INDEX.search(query_vector, k)
        return D.tolist(), I.tolist()

    def delete(self, ids: np.ndarray) -> int:
        '''
            ids: np.ndarray
            return:
                成功删除的数量
        '''
        count = self.INDEX.remove_ids(ids)
        print(f"delete {count} items from index")
        return count

    @property
    def ids(self):
        id_map = self.INDEX.id_map
        ids = faiss.vector_to_array(id_map)
        return ids

    def __len__(self):
        return self.INDEX.ntotal
    
    def reset(self):
        del self.INDEX
        self.create(self.dim)
