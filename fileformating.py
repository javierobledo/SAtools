import csv, os, string, json
from anytree import Node, RenderTree
from collections import defaultdict

#file is the name of the CSV file, and directory the complete path of a new directory where store the new files
def splitCSVfileInTxts(file, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    translator = str.maketrans('', '', string.punctuation)
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = row['title'].translate(translator)
            # Make attention with the lower here... is it necessary?
            filecontent = row['content'].lower()
            f = open(os.path.join(directory, filename),'w')
            f.write(filecontent)
            f.close()
    return directory


def readMalletFile(mallet):
    file = open(mallet)
    clusters = {}
    paths = set()
    for linea in file:
        data = linea.strip().split()
        if len(data) > 3:
            word = data[-2]
            level = int(data[-1])
            path = tuple(map(int,data[:-3]))
            paths.add(path[::-1])
            node = path[-(level+1)]
            if node not in clusters:
                clusters[node] = []
            clusters[node].append(word)
    file.close()
    return clusters,createTree(list(paths))

def createTree(paths):
    Tree = lambda: defaultdict(Tree)
    t = Tree()
    for path in paths:
        add(t, path)
    dicts = lambda t: {k: dicts(t[k]) for k in t}
    return dicts(t)

def add( t, path ):
    for node in path:
        t = t[node]

def parentStructure(tree, parent):
    n = []
    if tree == {}:
        return []
    for node in tree.keys():
        n += [(node,parent)] + parentStructure(tree[node], node)
    return n

def processMalletHLDAOutput(filepath):
    path, filename = os.path.split(filepath)
    filename, file_extension = os.path.splitext(filename)
    clusters, paths = readMalletFile(filepath)
    tree = parentStructure(paths, None)
    with open(os.path.join(path,filename+"clustertree.csv"), 'w') as csvoutfile:
        writer = csv.DictWriter(csvoutfile, fieldnames=["name", "parent"], quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for cluster, parent in tree:
            row = {"name": str(cluster), "parent": str(parent)}
            writer.writerow(row)
    with open(os.path.join(path,filename+'clusterwords.json'), 'w') as g:
        json.dump(clusters, g)
    return os.path.join(path,filename+"clustertree.csv")+" "+os.path.join(path,filename+'clusterwords.json')

import sys

if len(sys.argv) == 3:
    if(sys.argv[1] == "malletHLDA"):
        print(processMalletHLDAOutput(sys.argv[2]))
    elif(sys.argv[1] == "CSVtoTXTs"):
        filepath = sys.argv[2]
        path, filename = os.path.split(filepath)
        print(splitCSVfileInTxts(filepath,os.path.join(path, "corpus")))

#splitCSVfileInTxts("documents-2017-07-24.csv","/Users/jrobledo/Desktop/corpus")
#processMalletHLDAOutput("/Users/jrobledo/Dropbox/Arquitectura/resultHLDA")
# with open('clustertree.json', 'w') as f:
#     print(json.dump(paths,f))
# with open('clusterwords.json', 'w') as g:
#     print(json.dump(clusters, g))
# create a list of tuples where the structure is (node, parent), i.e. [(0,None),(52,0)...]
