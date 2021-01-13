from core.frozen_points_domain import *
from core.frozen_points_plugins import DiscoverMetamodels

#Creamos un modelo de manera programatica
feature_b = Feature('B', [])
relation = Relation(parent=None, children=[feature_b], card_min=0, card_max=1)	
feature_a = Feature('A', [relation])	
relation.parent = feature_a
fm = FeatureModel(feature_a)

#Imprimimos ese modelo
print(fm)

# Creamos el manager y lo inicializamos
dm = DiscoverMetamodels()

#Imprimimos los plugins disponibles
print(dm.plugins.get_plugin_names())

#Buscamos el plugin que acabamos de crear
plugin=dm.plugins.get_plugin_by_name('count_leafs')

#Imprimimos las operaciones de los plugins
print(plugin.operations)

#Usamos la operacion CountLeafs
result=plugin.use_operation('CountLeafs',fm)

#Imprimimos el resultado
print("El modelo tiene " + str(result) + " Features hojas")


#Buscamos el plugin que acabamos de crear
plugin=dm.plugins.get_plugin_by_name('count_features')

#Imprimimos las operaciones de los plugins
print(plugin.operations)

#Usamos la operacion CountLeafs
result=plugin.use_operation('CountFeatures',fm)

#Imprimimos el resultado
print("El modelo tiene " + str(result) + " Features")