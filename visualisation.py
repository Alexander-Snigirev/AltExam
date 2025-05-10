import networkx as nx
import os
import matplotlib.pyplot as plt
from config import config
import numpy as np

step_counter = 0

def ensure_viz_dir():
    """Создаёт папку viz, если она не существует."""
    if not os.path.exists(config.VIZ_DIR):
        os.makedirs(config.VIZ_DIR)

def draw_graph(vertexes: set, edges_dict: dict, root: int, 
               min_edges: dict = None, cycle: set = None, 
               mst_edges: set = None, stage: str = "graph"):
    """Рисует граф и сохраняет изображение в папке viz, отображая однонаправленные дуги.
    
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
    
    # Определяем цвета и толщину рёбер
    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if mst_edges and (u, v) in mst_edges:
            edge_colors.append('r')  # Рёбра остова — красные
            edge_widths.append(2.5)  # Увеличенная толщина
        elif min_edges and (u, v) in [(min_edges[to][0], to) for to in min_edges]:
            edge_colors.append('r')  # Минимальные рёбра — красные
            edge_widths.append(2.5)  # Увеличенная толщина
        elif cycle is not None and min_edges and (u, v) in [(min_edges[to][0], to) for to in cycle if to in min_edges]:
            edge_colors.append('b')  # Рёбра цикла — синие
            edge_widths.append(1.0)  # Стандартная толщина
        else:
            edge_colors.append('k')  # Обычные рёбра — чёрные
            edge_widths.append(1.0)  # Стандартная толщина
    
    # Определяем цвета вершин
    node_colors = ['y' if v == root else 'b' if cycle is not None and v in cycle else 'lightblue' for v in G.nodes()]
    
    # Рисуем граф
    plt.figure(figsize=(10, 8))  # Увеличиваем размер изображения
    pos = nx.spring_layout(G, seed=42, k=0.5)  # Увеличиваем расстояние между вершинами с помощью k
    
    # Рисуем вершины
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600)
    
    # Рисуем рёбра с кривизной для двунаправленных дуг
    edge_styles = []
    for u, v in G.edges():
        # Если есть обратное ребро (v, u), добавляем кривизну
        if G.has_edge(v, u):
            edge_styles.append('arc3,rad=0.2')  # Положительная кривизна
        else:
            edge_styles.append('arc3,rad=0')  # Прямая стрелка
    
    # Рисуем рёбра с индивидуальной толщиной
    for (u, v), style, color, width in zip(G.edges(), edge_styles, edge_colors, edge_widths):
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)], edge_color=color, width=width,
            arrows=True, connectionstyle=style, arrowsize=15
        )
    
    # Рисуем метки рёбер с небольшим смещением для двунаправленных дуг
    edge_labels = nx.get_edge_attributes(G, 'weight')
    for (u, v), weight in edge_labels.items():
        # Если есть обратное ребро, смещаем метку
        offset = 0.1 if G.has_edge(v, u) else 0
        # Вычисляем позицию метки со смещением
        x = (pos[u][0] + pos[v][0]) / 2
        y = (pos[u][1] + pos[v][1]) / 2
        # Добавляем небольшой случайный сдвиг для избежания перекрытия
        random_offset = np.random.uniform(-0.05, 0.05) if G.has_edge(v, u) else 0
        plt.text(x + offset, y + random_offset, weight, fontsize=8, ha='center', va='center', 
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Рисуем метки вершин
    nx.draw_networkx_labels(G, pos, font_size=12)
    
    # Сохраняем изображение
    filename = os.path.join(config.VIZ_DIR, f"step_{step_counter:03d}_{stage}.png")
    plt.savefig(filename, format='png', bbox_inches='tight')
    plt.close()
    
    step_counter += 1