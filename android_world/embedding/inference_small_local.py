from transformers import AutoTokenizer, AutoModel
import torch

class BgeEmbedding():
    def __init__(self, model_path) -> None:
    
        
        # Load model from HuggingFace Hub
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path).eval()

    def encode(self, query):

        # Tokenize sentences
        encoded_input = self.tokenizer([query], padding=True, truncation=True, return_tensors='pt')
        # for s2p(short query to long passage) retrieval task, add an instruction to query (not add instruction for passages)
        # encoded_input = tokenizer([instruction + q for q in queries], padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            # Perform pooling. In this case, cls pooling.
            sentence_embeddings = model_output[0][:, 0]
        # normalize embeddings
        sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)

        sentence_embeddings = sentence_embeddings.detach().cpu().numpy()
        
        return sentence_embeddings
