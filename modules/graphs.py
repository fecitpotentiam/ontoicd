import os.path
from textwrap import wrap

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.pyplot import margins

from modules.onto import *


class GraphBuilder:
    def __init__(self, ontology):
        self.ontology = ontology

    @staticmethod
    def split_label(disease_name: str) -> str:
        splitted_string = wrap(disease_name, 30)
        return '\n'.join(splitted_string)

    def get_label(self, disease) -> str:
        label = f'{disease.label[0]} ({str(disease).replace("icd10.", "")}'

        label = self.split_label(label)

        return label + ')'

    def draw_graph(self, disease_code: str):
        G = nx.Graph()
        filename = f'./static/img/{disease_code}.png'

        if not os.path.isfile(filename):
            diseases_branch, professional_diseases = self.ontology.get_diseases_branch(disease_code)
            nodes = [self.get_label(disease) for disease in diseases_branch]
            color_map = {}

            for i in range(len(nodes)):
                G.add_node(nodes[i])
                if i != 0:
                    color_map[nodes[i]] = '#00b4d9'
                else:
                    color_map[nodes[i]] = 'green'

                try:
                    G.add_edge(nodes[i], nodes[i + 1])

                except IndexError:
                    pass

            if professional_diseases:
                for i, disease in enumerate(professional_diseases):
                    disease_name = self.split_label(str(disease)[1:])
                    G.add_node(disease_name)

                    color_map[disease_name] = 'yellow'

                    G.add_edge(disease_name, nodes[0])

            values = [color_map.get(node, 0.25) for node in G.nodes()]

            plt.figure(3, figsize=(20, 10))
            margins(0.4, 0.4)
            nx.draw(G, with_labels=True, node_color=values, node_size=1000)
            plt.savefig(filename)
            plt.close()
