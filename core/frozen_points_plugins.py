from types import FunctionType, ModuleType
from typing import List

# Este modulo nos permite obligar ciertas listas con tipos
from collections import UserList
# Estos modulos nos permiten explorar las clases existentes en distintos plugins 'a la java reflexion' 
from importlib import import_module
from pkgutil import iter_modules
import inspect

# Importamos las clases del core que vamos a necesitar (blackbox)
from core.frozen_points_domain import Operation
from core.frozen_points_domain import FeatureModel

# Definimos las posibles rutas a los plugins
PLUGIN_PATHS = [
    'plugin',
]

# Definimos una coleccion para almacenar los objetos de tipo operacion. 
# Es interesante que las colecciones tipadas funcionan como clases y pueden tener métodos
class Operations(UserList):  # pylint: disable=too-many-ancestors
    data: List[Operation]

    def search_by_name(self, name: str) -> Operation:
        candidates = filter(lambda op: op.__name__ == name, self.data)
        try:
            operation = next(candidates, None)
        except StopIteration:
            raise OperationNotFound
        return operation

# Definimos una clase que represente a un plugin dentro del framwork. 
# Notese que también contiene los modulos y las operaciones que haya en la instalación de python
class Plugin:
    def __init__(self, module: ModuleType) -> None:
        self.module: ModuleType = module
        self.operations: Operations = Operations()

    @property
    def name(self):
        return self.module.__name__.split('.')[-1]
    
    # Esta clase añade las operaciones de un modulo
    def append_operation(self, operation: Operation) -> None:
        self.operations.append(operation)

    def use_operation(self, name: str, src: FeatureModel) -> Operation:
        operation = self.operations.search_by_name(name)
        return operation().execute(model=src)

# Definimos una lista de plugins y algunos métodos importantes
class Plugins(UserList):  # pylint: disable=too-many-ancestors
    data: List[Plugin]

    # buscamos los plugins que se llamen como queremos
    def get_plugin_by_name(self, name: str):
        for plugin in self.data:
            if plugin.name == name:
                return plugin
        raise PluginNotFound

    # devolvemos la lista de plugins            
    def get_plugin_names(self) -> List[str]:
        return [plugin.name for plugin in self.data]

    #devolvemos las operacione sde un plugin
    def get_operations_by_plugin_name(self, plugin_name: str) -> Operations:
        try:
            plugin = self.get_plugin_by_name(plugin_name)
            return plugin.operations
        except PluginNotFound:
            return Operations()

#Esta es una clase especial que nos va a permitir enumerar y ejecutar las operaciones que tengamos dentro de los plugins
class DiscoverMetamodels:
    
    #Cuando creamos la clase, esta inicializa la lista de modulos existentes y llama al discover para buscar plugins y modulos 
    def __init__(self):
        self.module_paths: List[ModuleType] = list()
        for path in PLUGIN_PATHS:
            try:
                module: ModuleType = import_module(path)
                self.module_paths.append(module)
            except ModuleNotFoundError:
                print('ModuleNotFoundError %s', path)
        self.plugins: Plugins = self.discover()

    #Este metodo busca las clases existentes en los módulos encontrados
    def search_classes(self, module):
        classes = []
        for _, file_name, ispkg in iter_modules( module.__path__, module.__name__ + '.' ):
            if ispkg:
                classes += self.search_classes(import_module(file_name))
            else:
                _file = import_module(file_name)
                classes += inspect.getmembers(_file, inspect.isclass)
        return classes

    # Este método se encarga de buscar los plugins modulos y clases existentes en el path indicado como variable global
    def discover(self) -> dict:
        plugins = Plugins()
        for pkg in self.module_paths:
            for _, plugin_name, ispkg in iter_modules(pkg.__path__, pkg.__name__ + '.'):
                if not ispkg:
                    continue
                module = import_module(plugin_name)
                plugin = Plugin(module=module)
                classes = self.search_classes(module)
                for _, _class in classes:
                    if not _class.__module__.startswith(module.__package__):
                        continue  # Exclude modules not in current package
                    #!! Fijaos como añadimos a la colección de operaciones cuando la clase operaciones hereda de la clase abstracta !!
                    inherit = _class.mro()
                    if Operation in inherit:
                        plugin.append_operation(_class)   
                plugins.append(plugin)
        return plugins