import matplotlib.pyplot as plt
from gensim.summarization.bm25 import BM25
import json
from tqdm import tqdm
from collections import Counter
from gensim import corpora
from gensim.summarization import bm25  #  gensim==3.8.3



def simple_tok(sent: str):
    return sent.split()


def search_BM25(corpus, QUERY, section_true):
    tok_corpus = [simple_tok(s) for s in corpus]
    bm25 = BM25(tok_corpus)

    # TODO Special symbol processing
    query = QUERY.split()
    scores = bm25.get_scores(query)
    # print("score:", scores)

    best_docs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:70]
    for i, b in enumerate(best_docs):
        # print(f"rank {i + 1}: {keys[b]}\t-----------------\t{corpus[b][:100]}")
        if keys[b] == section_true:
            return i + 1


""" corpus build """
# PATH = "data/data_search/section_doc.json"
# PATH = "data/data_search/section_doc_body.json"
# PATH = "data/data_search/section_doc_body_text.json"
PATH = "data/data_search/section_doc_subtitle.json"
# PATH = "data/data_search/section_doc_title.json"
with open(PATH) as f:
    section_doc = json.load(f)

# corpus = ["The little fox ran home",
#           "dogs are the best ",
#           "Yet another doc ",
#           "I see a little fox with another small fox",
#           "last doc without animals"]

corpus = [doc for key, doc in section_doc.items()]
keys = [key for key, doc in section_doc.items()]

""" query build """
# rank 2: Zoom Help Center :: Account & Admin :: Frequently Asked Questions
# QUERY = "How do I change from monthly to annual or annual to monthly payments?"

# rank 6: Zoom Help Center :: Meetings & Webinars :: Settings & Controls
# QUERY = "Where can I find the meeting passcode as the host or alternative host?"

# rank 1: Zoom Help Center :: Account & Admin :: Tax
# QUERY = "**What is a tax identification number?**"

# rank 6: Zoom Help Center :: Account & Admin :: Admin Management
# QUERY = "Reporting on Tracking Fields"

# rank 1: Zoom Help Center :: Audio, Video, Sharing :: Screen Sharing
# QUERY = "Sharing screens at the same time"


PATH_DOCS_PROCESSED = "/Users/king/File/Proj/Cicada_NLP/data/docs_05_31.processed.json"
with open(PATH_DOCS_PROCESSED) as f:
    data = json.load(f)

res = []
for item in tqdm(data):
    if "tags" not in item.keys() or "web_question" not in item.keys():
        continue

    web_question = item["web_question"]

    tags = item["tags"]
    section_true = ' :: '.join(tags)

    rank = search_BM25(corpus, web_question, section_true)
    res.append(rank)

rank_count = Counter(res)
print(rank_count)
plt.hist(res, 65)
plt.xticks(range(0,66,5))
plt.show()
print("Top1:{}, Top5:{}.".format(rank_count[1]/len(res), sum([rank_count[i] for i in range(1,6)])/len(res)))





