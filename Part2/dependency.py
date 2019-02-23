#!/usr/bin/env python

import re, sys, nltk, operator
from nltk.stem.wordnet import WordNetLemmatizer

from qa_engine.base import QABase
    
def find_main(graph):
    for node in graph.nodes.values():
        if node['rel'] == 'root':
            return node
    return None
    
def find_node(word, graph):
    for node in graph.nodes.values():
        if node["word"] == word:
            return node
    return None
    
def get_dependents(node, graph):
    results = []
    for item in node["deps"]:
        address = node["deps"][item][0]
        dep = graph.nodes[address]
        results.append(dep)
        results = results + get_dependents(dep, graph)
        
    return results



def find_answer(qgraph, sgraph):
    qmain = find_main(qgraph)
    qword = qmain["word"]
    
    snode = find_node(qword, sgraph)
    if snode == []:
        return "Snode null"
    for node in sgraph.nodes.values():
        #if node.get('head', None) == snode["address"]:
        if node['rel'] == "nsubj":
            
            deps = get_dependents(node, sgraph)
            deps = sorted(deps+[node], key=operator.itemgetter("address"))
            
            return " ".join(dep["word"] for dep in deps)


if __name__ == '__main__':
    driver = QABase()

    # Get the first question and its story
    q = driver.get_question("fables-01-1")
    story = driver.get_story(q["sid"])

    # get the dependency graph of the first question
    qgraph = q["dep"]
    print(q["text"])
    #print("qgraph:", qgraph)

    # The answer is in the second sentence
    # You would have to figure this out like in the chunking demo
    print(len(story["sch_dep"]))
    sgraph = story["sch_dep"][1]

    
    lmtzr = WordNetLemmatizer()
    for node in sgraph.nodes.values():
        tag = node["tag"]
        word = node["word"]
        if word is not None:
            if tag.startswith("V"):
                print(lmtzr.lemmatize(word, 'v'))
            else:
                print(lmtzr.lemmatize(word, 'n'))
    print()

    answer = find_answer(qgraph, sgraph)
    print("answer:", answer)

