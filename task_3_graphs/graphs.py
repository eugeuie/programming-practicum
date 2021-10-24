import json
import networkx as nx

with open('data/data_fixed.json', 'r') as f:
    data = json.loads(f.read())

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

BACON = 'Kevin Bacon'
for actor in actors_graph.nodes:
    if actor != BACON:
        path = nx.shortest_path(actors_graph, actor, BACON)
        print('Path from {} to {}:'.format(actor, BACON))
        for i in range(len(path) - 1):
            film = actors_graph.get_edge_data(path[i], path[i + 1])
            print('{} was in {} ({}) with {}'.format(path[i], film['title'], film['year'], path[i + 1]))
        print("{}'s Bacon number is {}\n".format(path[0], len(path) - 1))
