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

#splitCSVfileInTxts("documents-2017-07-24.csv","/Users/jrobledo/Desktop/corpus")
#clusters, paths = readMalletFile("demomallet")
clusters, paths = readMalletFile("/Users/jrobledo/Dropbox/Arquitectura/resultHLDA")
with open('clustertree.json', 'w') as f:
    print(json.dump(paths,f))
with open('clusterwords.json', 'w') as g:
    print(json.dump(clusters, g))