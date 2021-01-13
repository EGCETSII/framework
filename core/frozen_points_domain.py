from typing import Sequence
#Este modulo añade soporte a clases abstractas
from abc import ABC, abstractmethod

#Esto es la definición de la clase Relación
class Relation:

    #Esto es un constructor en python
    #Cuando colocamos el nombre de la clase entre comillas es la forma de usar tipado fuerte en python. 
    #De cara a crear un framework de caja blanca, necesitamos orientación a objetos y tipado de objectos
    #Esto está disponible en python desde la versión 3.8 en adelante
    def __init__(self, parent: 'Feature', children: Sequence['Feature'], card_min: int, card_max: int):
        self.parent = parent
        self.children = children
        self.card_min = card_min
        self.card_max = card_max

    #Este método añade un elemento a la colección de hijos de una relación
    def add_child(self, feature: 'Feature'):
        self.children.append(feature)

    #Este método verifica la cardinalidad de la relación y el número de hijos para devolver true si es mandatory
    def is_mandatory(self) -> bool:
        return (len(self.children) == 1 and self.card_max == 1 and self.card_min == 1)

    #Este método verifica la cardinalidad de la relación y el número de hijos para devolver true si es optional
    def is_optional(self) -> bool:
        return (len(self.children) == 1 and self.card_max == 1 and self.card_min == 0)

    #Este método verifica la cardinalidad de la relación y el número de hijos para devolver true si es or
    def is_or(self) -> bool:
        return (len(self.children) > 1 and self.card_max == len(self.children) and self.card_min == 1)

    #Este método verifica la cardinalidad de la relación y el número de hijos para devolver true si es alternative
    def is_alternative(self) -> bool:
        return (len(self.children) > 1 and self.card_max == 1 and self.card_min ==  1)

    #Este método to string en python
    def __str__(self):
        res = self.parent.name + '[' + str(self.card_min) + ',' + str(self.card_max) + ']'
        for _child in self.children:
            res += _child.name + ' '
        return res

#Esto es la definición de la clase Feature
class Feature:

    #Este es el método constructor. Aqui definimos que queremos que cada característica tenga un nombre y un conjunto de relaciones. 
    def __init__(self, name: str, relations: Sequence['Relation']):
        self.name = name
        self.relations = relations

    #Este es un metodo auxiliar para añadir una relación a una característica
    def add_relation(self, relation: 'Relation'):
        self.relations.append(relation)

    #Este método nos devuelve el conjunto de relaciones de una característica
    def get_relations(self):
        return self.relations

    #Este método to string en python
    def __str__(self):
        return self.name

#Esta clase representa a un modelo de características
class FeatureModel():

    #En el constructor solo encontramos una feature raiz
    def __init__(self, root: Feature):
        self.root = root

    #Este método devuelve el conjunto de relaciones existentes en el modelo
    def get_relations(self, feature=None):
        relations = []
        if not feature:
            feature = self.root
        for relation in feature.relations:
            relations.append(relation)
            for _feature in relation.children:
                relations.extend(self.get_relations(_feature))
        return relations

    #Este método devuelve el conjunto de features de un modelo
    def get_features(self):
        features = []
        features.append(self.root)
        for relation in self.get_relations():
            features.extend(relation.children)
        return features

    #Este método devuelve la feature identificandola por el nombre (TODO: Implementar con __equals__)
    def get_feature_by_name(self, str) -> Feature:
        features = self.get_features
        for feat in features:
            if feat.name == str:
                return feat
        raise ElementNotFoundException

    #Este método to string en python
    def __str__(self) -> str:
        res = 'root: ' + self.root.name + '\r\n'
        for i, relation in enumerate(self.get_relations()):
            res += f'relation {i}: {relation}\r\n'
        return(res)

#This is an abstract Operation. To define abstract methos we rely on ABC module of the core python distribution
class Operation(ABC):

    #This abstract method, executes an operation given a feature model
    @abstractmethod
    def execute(self, model: FeatureModel):
        pass
