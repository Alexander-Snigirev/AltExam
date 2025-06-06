from .reading_graph import reading_console, reading_file
from visualization.visualization import draw_graph


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
                # Замена текущего входного ребра на меньшее
                min_edges[edge[1]] = (edge[0], edges_dict[edge])
        else:
            # Инициализация вершины входным ребром
            min_edges[edge[1]] = (edge[0], edges_dict[edge])
            
            
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
    super_vertex = str(n + 1)                                            # Создание новой супервершины
    new_vertexes, new_edges_set, new_edges_dict, returnal_edges  = (Vertexes - cycle) | {super_vertex}, set(), {}, {}
    for u,v in edges_set:                                           # Обновление вершин и ребер для нового графа с супервершиной, а также инициализация returnal_edges
        if u not in cycle and v in cycle:
            edge = (u, super_vertex)
            if edge in new_edges_set and new_edges_dict[edge] < edges_dict[(u,v)] - min_edges[v][1]:
                continue                                            # При наличии нескольких ребер из одной вершины в супервершину - выбирается минимальное из них
            new_edges_dict[edge] = edges_dict[(u,v)] - min_edges[v][1]
            #new_edges_dict[edge] = edges_dict[(u,v)] + min_edges[min_edges[v][0]][1]
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
    #if cycle_edge is None
    super_vertex = str(int(super_vertex)-1)
    if cycle_edge is None:
        cycle_edge = (super_vertex, min_edges[super_vertex][0])
    answer.remove(cycle_edge )                                           # Удаление из списка одного ребра для устранения цикла

    # Визуализация: Граф с разжатой супервершиной, MST — красное, удалённое ребро — чёрное
    draw_graph(Vertexes, edges_dict, root, mst_edges=answer, stage=f"recursion_{recursion_level}_expanded_mst")
    return answer            

def run(input_mode):
    if input_mode == "file":
        n,root,vertexes,edges_dict,edges_set = reading_file()
    elif input_mode == "console":
        n,root,vertexes,edges_dict,edges_set = reading_console()
    
    mst = LiuEdmondsAlgorithm(vertexes.copy(), edges_set.copy(), root, edges_dict.copy(), n)
    if len(mst) == n-1:
        print(mst)
    else:
        print(f'Error. Impossible to create MST from root: {root}')


