from owlready2 import *


class Ontology:
    def __init__(self):
        self.icd_onto = self.load_ontology('icd10')
        self.professional_onto = self.load_ontology('professional_diseases')

    def find_professional_diseases(self, icd_code: str) -> list:
        professional_diseases = []
        
        for disease in list(self.professional_onto.search(type=self.professional_onto.Disease)):
            code = str(disease.DiseaseCodeICD[0]).replace('http://test.org/onto.owl#', '')
            if icd_code == code:
                print(code)
                print('FIND code', icd_code, disease.RelatedToDiseaseGropup)
                professional_diseases.append(disease)
        
        return professional_diseases

    def load_ontology(self, onto_name: str):
        onto = get_ontology(f"./knowledge_base/{onto_name}.owl")
        onto.load()
        return onto

    def find_class(self, mkb_code: str):
        classes = list(self.icd_onto.classes())
        for cl in classes:
            if str(cl) == mkb_code:
                return cl

    def get_parents(self, disease):
        diseases_list = [disease]
        parent_disease = disease

        while True:
            parent_disease = parent_disease.is_a[0]
            if parent_disease not in diseases_list and str(parent_disease) != 'owl.Thing':
                diseases_list.append(parent_disease)
            else:
                break

        return diseases_list

    def get_diseases_branch(self, disease_code) -> tuple:
        mkb_code = disease_code.replace('_', '.')
        disease = self.find_class(mkb_code)
        professional_diseases = self.find_professional_diseases(mkb_code)
        diseases_branch = self.get_parents(disease)
        return diseases_branch, professional_diseases

    def get_onto_classes(self) -> dict:
        icd_onto = self.load_ontology('icd10')
        classes = list(icd_onto.classes())
        labels = {cl.label[0]: str(cl).replace('.', '_') for cl in classes}
        return labels
