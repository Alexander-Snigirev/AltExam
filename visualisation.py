import networkx as nx
import os
import matplotlib.pyplot as plt
from config import config

step_counter = 0

def ensure_viz_dir():
    """Создаёт папку viz, если она не существует."""
    if not os.path.exists(config.VIZ_DIR):
        os.makedirs(config.VIZ_DIR)

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
    filename = os.path.join(config.VIZ_DIR, f"step_{step_counter:03d}_{stage}.png")
    plt.savefig(filename, format='png', bbox_inches='tight')
    plt.close()
    
    step_counter += 1