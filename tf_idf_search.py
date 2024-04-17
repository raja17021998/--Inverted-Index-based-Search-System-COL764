import math
import pickle
import re
import sys
import json
import modulefinder

def process_query(query_text):
    top_pattern = re.compile(r"<top>.*?</top>", re.DOTALL)
    top_matches = top_pattern.findall(query_text)

    for top_content in top_matches:
        capture_num(top_content)
        capture_title(top_content)
        capture_desc(top_content)

def capture_num(top_content):
    num_pattern = re.compile(r"<num>.*?(\d+)", re.DOTALL)
    num_match = num_pattern.search(top_content)
    if num_match:
        nums.append(num_match.group(1))

def capture_title(top_content):
    title_pattern = re.compile(r"<title>(.*?)<desc>", re.DOTALL)
    title_match = title_pattern.search(top_content)
    if title_match:
        titles.append(title_match.group(1).strip())

def capture_desc(top_content):
    desc_pattern = re.compile(r"<desc>(.*?)<narr>", re.DOTALL)
    desc_match = desc_pattern.search(top_content)
    if desc_match:
        descs.append(desc_match.group(1).strip())

def hash_constructor(nums, descs, titles, queries):
    for i in range(len(nums)):
        query_info = {
            "title": titles[i],
            "desc": descs[i]
        }
        queries[nums[i]] = query_info

def parse_query(query_path):
    file_name = "./train_data/"+ query_path
    try:
        with open(file_name, "r") as file_reader:
            query_text = file_reader.read()
            process_query(query_text)

        print("Nums size:", len(nums))
        print("Descs size:", len(descs))
        print("Title size:", len(titles))
        hash_constructor(nums, descs, titles, queries)
    except Exception as e:
        print(e)

def getPostingList(file):
    inverted_index = {}
    with open(file) as f:
        inverted_index = json.load(f)
    return inverted_index
def tokenize_data(data):
    if modulefinder.tokenizer_type == 1:
        bpe_tokenizer = modulefinder.BPETokenizer(100)
        size = len(data) * 25 // 100
        bpe_tokenizer.learn(data[:size])
        tokenized_data = bpe_tokenizer.tokenize_all(data)
    else:
        tokenized_data = modulefinder.SimpleTokenizer.tokenize(data)

    return tokenized_data

if __name__ == "__main__":
    queryFile = sys.argv[1]
    result_file = sys.argv[2]
    indexFile = sys.argv[3]
    dictFile = sys.argv[4]

    queries = {}
    nums = []
    descs = []
    titles = []
    parse_query(queryFile)
    # print(queries)
    inverted_index = getPostingList(indexFile+".idx")
    print(inverted_index)
    setOfDocs = set()
    for token in inverted_index.keys():
        postingList = inverted_index[token]
        for posting in postingList:
            setOfDocs.add(posting.doc_id)
    N = len(setOfDocs) 
    for qid in queries.keys():
        query = queries[qid]
        query_text = query["title"] + " " + query["desc"]
        query_tokens = tokenize_data(query_text)
        wordMap ={}
        top100Results = {}
        for token in query_tokens:
            wordMap[token] = wordMap.get(token, 0) + 1
        for token in wordMap.keys:
            idScoreMap = {}
            postingList = inverted_index[token]
            df = postingList.size
            idf = math.log2(1 + (N/df))
            for posting in postingList:
                f = posting.term_frequency
                tf = 1 + math.log2(f)/math.log2(2)

                doc_id = posting.doc_id
                if(idScoreMap.contains(doc_id)==False):
                    idScoreMap[doc_id] = 0.0
                tfidf = idScoreMap[doc_id] + tf*idf*wordMap[token]
                idScoreMap[doc_id] = tfidf
            sorted_idScoreMap = sorted(idScoreMap.items(), key=lambda x: x[1], reverse=True)
        top100Results[qid] = sorted_idScoreMap[:100]
        with open(result_file, "w") as file_writer:
            for qid in top100Results.keys:
                for doc_id, score in top100Results[qid]:
                    file_writer.write(qid + " "+ "0 " + doc_id + " " + str(score) + "\n")
