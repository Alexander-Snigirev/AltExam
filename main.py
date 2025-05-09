import matplotlib.pyplot as plt
import os
import sys
import networkx as nx
print(sys.executable)
print(sys.version)


step_counter = 0
# Папка для сохранения визуализаций
VIZ_DIR = "viz"

def ensure_viz_dir():
    """Создаёт папку viz, если она не существует."""
    if not os.path.exists(VIZ_DIR):
        os.makedirs(VIZ_DIR)

def draw_graph(vertexes: set, edges_dict: dict, root: int, 
               min_edges: dict = None, cycle: set = None, 
               mst_edges: set = None, stage: str = "graph"):
    """Рисует граф и сохраняет изображение в папке viz.
    
    Args:
        vertexes: Множество вершин.
        edges_dict: Словарь рёбер с весами {(u, v): weight}.
        root: Корневая вершина.
        min_edges: Словарь минимальных входящих рёбер {v: (u, weight)}.
        cycle: Множество вершин цикла (для подсветки синим).
        mst_edges: Множество рёбер остовного дерева (для подсветки красным).
        stage: Описание этапа для имени файла.
    """
    global step_counter
    ensure_viz_dir()
    
    G = nx.DiGraph()
    # Добавляем вершины
    G.add_nodes_from(vertexes)
    # Добавляем рёбра с весами
    for (u, v), weight in edges_dict.items():
        G.add_edge(u, v, weight=weight)
    
    # Определяем цвета рёбер
    edge_colors = []
    for u, v in G.edges():
        if mst_edges and (u, v) in mst_edges:
            edge_colors.append('r')  # Рёбра остова — красные
        elif min_edges and (u, v) in [(min_edges[to][0], to) for to in min_edges]:
            edge_colors.append('r')  # Минимальные рёбра — красные
        elif cycle is not None and min_edges and (u, v) in [(min_edges[to][0], to) for to in cycle if to in min_edges]:
            edge_colors.append('b')  # Рёбра цикла — синие
        else:
            edge_colors.append('k')  # Обычные рёбра — чёрные
    
    # Определяем цвета вершин
    node_colors = ['y' if v == root else 'b' if cycle is not None and v in cycle else 'lightblue' for v in G.nodes()]
    
    # Рисуем граф
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, 
            node_size=500, font_size=10, arrows=True)
    # Добавляем веса рёбер
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Сохраняем изображение
    filename = os.path.join(VIZ_DIR, f"step_{step_counter:03d}_{stage}.png")
    plt.savefig(filename, format='png', bbox_inches='tight')
    plt.close()
    
    step_counter += 1

    
    
    
    

def reading_file():
    ff = open("file")
    inp = ff.readlines()
    n,m = list(map(int,inp[0].split()))
    
    vertexes = set()                    # словарь вершин
    edges_dict = {}                     # словарь ребер
    edges_set = set()                   # множество ребер

    for i in range(m):
        u, v, height = list(map(int, inp[i+1].split()))
        edges_dict[(u,v)] = height      # ключ - ребро, значение - его вес
        edges_set.add((u,v))
        vertexes |= {u,v}
    root = int(inp[-1])    
    ff.close()
    return n,root,vertexes,edges_dict,edges_set

def LiuEdmondsAlgorithm(Vertexes: set[int], edges_set: set[tuple[int,int]], root: int, edges_dict: dict[tuple[int,int], int], n: int, recursion_level=0):
    # Визуализация: Исходный граф (только для первой рекурсии)
    if recursion_level == 0:
        draw_graph(Vertexes, edges_dict, root, stage="initial_graph")
    ### Шаг 1: Удаление ребер, ведущих в корень
    cp_set = edges_set.copy()
    for u,v in cp_set:
        if v == root:
            edges_dict.pop((u,v))
            edges_set.remove((u,v))
            
    # Визуализация: Граф после удаления рёбер в корень (только для первой рекурсии)
    if recursion_level == 0:
        draw_graph(Vertexes, edges_dict, root, stage="no_root_edges")
    
    # Визуализация: Текущий граф на уровне рекурсии
    draw_graph(Vertexes, edges_dict, root, stage=f"recursion_{recursion_level}_graph")

        
    ### Шаг 2: Поиск дуг с наименьшим весом для каждой вершины       
    min_edges = {}
    for edge in edges_set:
        if edge[1] in min_edges:
            if min_edges[edge[1]][1] > edges_dict[edge]:
                min_edges[edge[1]] = (edge[0], edges_dict[edge])    # Замена текущего входного ребра на меньшее
        else:
            min_edges[edge[1]] = (edge[0], edges_dict[edge])        # Инициализация вершины входным ребром
            
            
    # Визуализация: Граф с минимальными рёбрами (красные)
    draw_graph(Vertexes, edges_dict, root, min_edges=min_edges, stage=f"recursion_{recursion_level}_min_edges")
    
    
    ### Шаг 3: Проверка на циклы. Если циклов нет, то MST построено
    c_vertex = None
    for vertex in Vertexes:
        if not (c_vertex is None):
            break
        visited = set()                                             # Множество посещенных вершин
        prev_vertex = min_edges.get(vertex)                         # Обход назад по дугам                          
        while prev_vertex:                                          
            if prev_vertex[0] in visited:                           # Если вершина уже есть в посещенных, то найден цикл
                c_vertex = prev_vertex[0]
                break
            visited.add(prev_vertex[0])                             # Добавление вершины в посещенные
            prev_vertex = min_edges.get(prev_vertex[0])
    
    # Визуализация: Граф с минимальными рёбрами и циклом (синий)
    if c_vertex is not None:
        cycle = {c_vertex}
        prev_vertex = min_edges.get(c_vertex)
        while prev_vertex[0] != c_vertex:
            cycle.add(prev_vertex[0])
            prev_vertex = min_edges.get(prev_vertex[0])
        draw_graph(Vertexes, edges_dict, root, min_edges=min_edges, cycle=cycle, 
                   stage=f"recursion_{recursion_level}_cycle")
    
    if c_vertex is None:                                            # Если циклов не найдено, то дерево уже построено
        mst = [(min_edges[to][0], to) for to in min_edges.keys()]    
        draw_graph(Vertexes, edges_dict, root, mst_edges=set(mst), stage="final_mst")
        return mst
    ### Шаг 4: Построение цикла
    cycle = {c_vertex}           
    prev_vertex = min_edges.get(c_vertex)
    while prev_vertex[0] != c_vertex:                               # Сохранение вершин всего цикла
        cycle.add(prev_vertex[0])
        prev_vertex = min_edges.get(prev_vertex[0])
    ### Шаг 5: Построение нового графа, где найденный цикл стянут в супервершину   
    super_vertex = n + 1                                            # Создание новой супервершины
    new_vertexes, new_edges_set, new_edges_dict, returnal_edges  = (Vertexes - cycle) | {super_vertex}, set(), {}, {}
    for u,v in edges_set:                                           # Обновление вершин и ребер для нового графа с супервершиной, а также инициализация returnal_edges
        if u not in cycle and v in cycle:
            edge = (u, super_vertex)
            if edge in new_edges_set and new_edges_dict[edge] < edges_dict[(u,v)] - min_edges[v][0]:
                continue                                            # При наличии нескольких ребер из одной вершины в супервершину - выбирается минимальное из них
            new_edges_dict[edge] = edges_dict[(u,v)] - min_edges[v][0]
            returnal_edges[edge] = (u,v)                            # Сохранение старого ребра для дальнейшего разжатия
            new_edges_set.add(edge)
        elif u in cycle and v not in cycle:
            edge = (super_vertex, v)
            if edge in new_edges_set:
                early_edge = returnal_edges[edge][0]
                if edges_dict[(early_edge, v)] < edges_dict[(u,v)]:
                    continue
            new_edges_set.add(edge)      
            new_edges_dict[edge] = edges_dict[(u,v)]  
            returnal_edges[edge] = (u,v)
        elif u not in cycle and v not in cycle:
            edge = (u,v)    
            new_edges_set.add(edge)
            new_edges_dict[edge] = edges_dict[(u,v)]
            returnal_edges[edge] = (u,v)
    ### Шаг 6: Рекурсивный вызов для нового графа         
    new_building = LiuEdmondsAlgorithm(new_vertexes, new_edges_set, root, new_edges_dict, n+1)
    ### Шаг 7: Разжатие стянутых циклов и построение дерева
    cycle_edge = None
    for u,v in new_building:
        if v == super_vertex:
            old_edge = returnal_edges[(u, super_vertex)][1]             # Выгрузка ребра из супервершины
            cycle_edge = (min_edges[old_edge][0], old_edge)             # инициализация ребра, принадлежащего циклу
    answer = set([returnal_edges[edge] for edge in new_building])
    for v in cycle:
        u = min_edges[v][0]
        answer.add((u,v))
    # Визуализация: Граф с разжатой супервершиной, рёбра цикла — синие
    draw_graph(Vertexes, edges_dict, root, cycle=cycle, stage=f"recursion_{recursion_level}_expanded_cycle")    
    answer.remove(cycle_edge)                                           # Удаление из списка одного ребра для устранения цикла
    
    # Визуализация: Граф с разжатой супервершиной, MST — красное, удалённое ребро — чёрное
    draw_graph(Vertexes, edges_dict, root, mst_edges=answer, stage=f"recursion_{recursion_level}_expanded_mst")
    return answer            




n,root,vertexes,edges_dict,edges_set = reading_file()
   

print(*LiuEdmondsAlgorithm(vertexes.copy(), edges_set.copy(), root, edges_dict.copy(), n))


