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
    
    G.add_nodes_from(vertexes)
    
    for (u, v), weight in edges_dict.items():
        G.add_edge(u, v, weight=weight)
    
    
    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if mst_edges and (u, v) in mst_edges:
            edge_colors.append('r')  
            edge_widths.append(2.5)  
        elif min_edges and (u, v) in [(min_edges[to][0], to) for to in min_edges]:
            edge_colors.append('r')  
            edge_widths.append(2.5)  
        elif cycle is not None and min_edges and (u, v) in [(min_edges[to][0], to) for to in cycle if to in min_edges]:
            edge_colors.append('b')  
            edge_widths.append(1.0)  
        else:
            edge_colors.append('k')  
            edge_widths.append(1.0)  
    
    
    node_colors = ['y' if v == root else 'b' if cycle is not None and v in cycle else 'lightblue' for v in G.nodes()]
    
    
    plt.figure(figsize=(10, 8))  
    pos = nx.spring_layout(G, seed=100, k=0.25)  
    
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600)
    
    
    edge_styles = []
    for u, v in G.edges():
        
        if G.has_edge(v, u):
            edge_styles.append('arc3,rad=0.2')  
        else:
            edge_styles.append('arc3,rad=0')  
    
    
    for (u, v), style, color, width in zip(G.edges(), edge_styles, edge_colors, edge_widths):
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)], edge_color=color, width=width,
            arrows=True, connectionstyle=style, arrowsize=15
        )
    
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    for (u, v), weight in edge_labels.items():
        if G.has_edge(v, u):
            x = pos[v][0]+(pos[u][0]-pos[v][0])*0.1
            y = pos[v][1]+(pos[u][1]-pos[v][1])*0.1
        else:
            x = (pos[u][0] + pos[v][0]) / 2
            y = (pos[u][1] + pos[v][1]) / 2
        
        
        plt.text(x, y, weight, fontsize=8, ha='center', va='center', 
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    nx.draw_networkx_labels(G, pos, font_size=12)
    

    filename = os.path.join(config.VIZ_DIR, f"step_{step_counter:03d}_{stage}.png")
    plt.savefig(filename, format='png', bbox_inches='tight')
    plt.close()
    
    step_counter += 1
