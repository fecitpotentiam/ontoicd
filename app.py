from flask import Flask, render_template, request
from fuzzywuzzy import process

from modules.graphs import GraphBuilder
from modules.onto import Ontology

app = Flask(__name__)
ontology = Ontology()
graph_builder = GraphBuilder(ontology)


@app.route('/')
def search_page():
    return render_template('search.html')


@app.route('/search_result', methods=['POST', 'GET'])
def show_search_result():
    if request.method == 'POST':
        query = request.form['query']
        labels = ontology.get_onto_classes()
        query = process.extract(query, labels.keys(), limit=30)
        sorted_diseases_dict = {disease[0]: labels[disease[0]] for disease in query}

        return render_template("search_result.html", diseases=sorted_diseases_dict)


@app.route('/icd/<disease>')
def show(disease):
    graph_builder.draw_graph(disease)
    return render_template("disease.html", disease=disease)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
