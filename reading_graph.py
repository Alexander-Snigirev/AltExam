from config import config

def reading_file():
    ff = open(config.FNAME)
    inp = ff.readlines()
    n,m = list(map(int,inp[0].split()))
    
    vertexes = set()                    # словарь вершин
    edges_dict = {}                     # словарь ребер
    edges_set = set()                   # множество ребер

    for i in range(m):
        u, v, height = list(map(int, inp[i+1].split()))
        u = str(u)
        v = str(v)
        edges_dict[(u,v)] = height      # ключ - ребро, значение - его вес
        edges_set.add((u,v))
        vertexes |= {u,v}
    root = int(inp[-1])   
    print(root)
    ff.close()
    return n,root,vertexes,edges_dict,edges_set


def reading_console():
    n,m = list(map(int, input().split()))
    
    vertexes = set()                    # словарь вершин
    edges_dict = {}                     # словарь ребер
    edges_set = set()                   # множество ребер

    for i in range(m):
        u, v, height = list(map(int, input().split()))
        edges_dict[(u,v)] = height      # ключ - ребро, значение - его вес
        edges_set.add((u,v))
        vertexes |= {u,v}
    root = int(input())    
    return n,root,vertexes,edges_dict,edges_set