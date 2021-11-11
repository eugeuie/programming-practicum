import json
import os
import networkx as nx
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
# import matplotlib.pyplot as plt

data = None
actors_graph = None
combo_box = None
actors = None
BACON = 'Kevin Bacon'

def build_graph():
    global actors_graph
    actors_graph = nx.Graph()
    actors_graph.add_nodes_from([actor['name'] for actor in data])

    for actor in data:
        for film in actor['films']:
            for other_actor in data:
                if other_actor['name'] != actor['name']:
                    for other_film in other_actor['films']:
                        if other_film == film:
                            actors_graph.add_edge(actor['name'], other_actor['name'], title=film['title'], year=film['year'])

    # edge_titles = ['{} ({})'.format(edge[2]['title'], edge[2]['year']) for edge in actors_graph.edges(data=True)]
    # labels = dict(zip(actors_graph.edges, edge_titles))

    # plt.figure(figsize=(16, 16))
    # sl = nx.spring_layout(actors_graph, k=4, seed=1)
    # nx.draw(actors_graph, with_labels=True, pos=sl, node_size=20000)
    # nx.draw_networkx_edge_labels(actors_graph, pos=sl, edge_labels=labels)
    # plt.show()

def select_data_file():
    global data
    global combo_box
    global actors
    inputfilename = askopenfilename()
    with open(os.path.join('data', inputfilename), 'r') as f:
        data = json.loads(f.read())
    actors = [actor['name'] for actor in data]
    actors.remove(BACON)
    combo_box = ttk.Combobox(window, values=actors)
    combo_box.pack()
    build_graph()

def get_path():
    global actors
    actor = actors[combo_box.current()]
    path = nx.shortest_path(actors_graph, actor, BACON)
    answer = 'Path from {} to {}:\n'.format(actor, BACON)
    for i in range(len(path) - 1):
        film = actors_graph.get_edge_data(path[i], path[i + 1])
        answer += '{} was in {} ({}) with {}\n'.format(path[i], film['title'], film['year'], path[i + 1])
    answer += "{}'s Bacon number is {}\n".format(path[0], len(path) - 1)
    messagebox.showinfo(title='Answer', message=answer)

window = tk.Tk()
window.geometry('300x280')
window.title('Bacon Numbers')

select_file_button = tk.Button(window, text='Select Data File', command=select_data_file)
select_file_button.pack()

load_data_button = tk.Button(window, text='Get Bacon Number', command=get_path)
load_data_button.pack()

window.mainloop()
