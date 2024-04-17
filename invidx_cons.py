import json
import os
import re
import sys
import xml.etree.ElementTree as ET
class SimpleTokenizer:
    @staticmethod
    def tokenize(content):
        # Split the content string into tokens based on spaces
        tokens = content.strip().split(" ")
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
            tokens[i] = tokens[i].translate(str.maketrans('', '' , ' \n-[]0() ,;:+∗”?$`.\/'))
        return tokens

class BPETokenizer:
    def __init__(self, num_merge_operations):
        self.num_merge_operations = num_merge_operations
        self.vocabulary = {}

    def learn(self, training_data):
        # Tokenize training data and initialize vocabulary
        for text in training_data:
            tokens = self.tokenize(text)
            self.update_vocabulary(tokens)

        # Perform BPE merge operations
        for _ in range(self.num_merge_operations):
            merges = self.find_merge_pairs()
            if not merges:
                break
            self.apply_merges(merges)

    def tokenize(self, text):
        # Implement tokenization logic here
        tokens = text.strip().split(" ")
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
            tokens[i] = tokens[i].translate(str.maketrans('', '' , ' \n-[]0() ,;:+∗”?$`.\/'))
        return [token + "_" for token in tokens]

    def update_vocabulary(self, tokens):
        # Update vocabulary based on tokens
        for token in tokens:
            self.vocabulary[token] = self.vocabulary.get(token, 0) + 1

    def find_merge_pairs(self):
        merges = {}
        return merges

    def apply_merges(self, merges):
        for original1, original2 in merges.items():
            merged = original1 + original2
            self.vocabulary[merged] = self.vocabulary.get(original1, 0) + self.vocabulary.get(original2, 0)
            del self.vocabulary[original1]
            del self.vocabulary[original2]

    def tokenize_all(self, texts):
        tokenized_texts = []
        for text in texts:
            tokens = self.tokenize(text)
            tokenized_texts.extend(tokens)
        return tokenized_texts

    def get_vocabulary(self):
        return self.vocabulary


class InvertedIndexBuilder:
    def __init__(self, tokenizer_type):
        self.tokenizer_type = tokenizer_type
        self.inverted_index = {}
        self.index = {}

    def build_inverted_index(self, coll_path):
        doc_ids = []
        content = []
        for root, _, files in os.walk(coll_path+"/f1"):
            for file in files:
                    file_path = os.path.join(root, file)
                    self.get_doc_ids_and_content(file_path, doc_ids, content)
        # print("Total number of documents: ", len(doc_ids))

        for root, _, files in os.walk(coll_path+"/f2"):
            for file in files:
                    file_path = os.path.join(root, file)
                    self.get_doc_ids_and_content(file_path, doc_ids, content)
        # print("Total number of documents: ", len(doc_ids))
        
        for i in range(len(doc_ids)):
            docId = doc_ids[i]
            text = content[i]
            tokenized_text = self.tokenize_data(text)
            word_count = self.count_words(tokenized_text)
            # print(word_count)
            if(word_count.__contains__('')):
                word_count.pop('')
            self.index[docId] = word_count
            for word in word_count:
                if(word not in self.inverted_index):
                    self.inverted_index[word] = {}
                self.inverted_index[word][docId] = word_count[word]

    def get_doc_ids_and_content(self, file_path, doc_ids, content):
        with open(file_path,"r") as f:
            data = f.read()
            docs = data.split("</DOC>")
            for doc in docs:
                if len(doc.strip()) == 0:
                    continue
                doc+= "</DOC>"
                doc = doc.replace("<!--(.*?)-->", "")
                docid, text = self.parseXMLstring(doc.replace("<TITLE> <\TITLE>",""))
                doc_ids.append(docid)
                content.append(text)

    def parseXMLstring(self, xmlstring):
        # print(xmlstring)
        root = ET.fromstring(xmlstring)
        docno = root.find("DOCID").text.strip()
        text = root.find("CONTENT").text.strip()
        return docno, text

    def tokenize_data(self, data):
        if self.tokenizer_type == 1:
            bpe_tokenizer = BPETokenizer(100)
            size = len(data) * 25 // 100
            bpe_tokenizer.learn(data[:size])
            tokenized_data = bpe_tokenizer.tokenize_all(data)
        else:
            tokenized_data = SimpleTokenizer.tokenize(data)

        return tokenized_data

    def count_words(self, text):
        word_count = {}
        for word in text:
            word_count[word] = word_count.get(word, 0) + 1
        return word_count

    def generate_index_files(self, index_file):
        with open(index_file + ".idx", 'w') as idx_file, open(index_file + ".dict", 'w') as dict_file:
            json.dump(self.inverted_index, idx_file,sort_keys=True)
            json.dump(self.index, dict_file,sort_keys=True)

if __name__ == "__main__":
    coll_path = sys.argv[1]
    index_file = sys.argv[2]
    tokenizer_type = sys.argv[4]
    compression_type= sys.argv[3]
    if compression_type==1:
        print("Not implemented")
    
    else:
        index_builder = InvertedIndexBuilder(tokenizer_type)
        index_builder.build_inverted_index(coll_path)
        index_builder.generate_index_files(index_file)

