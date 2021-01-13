from core.frozen_points_domain import Operation
from core.frozen_points_domain import FeatureModel

class CountFeatures(Operation):
    
    def execute(self, model: FeatureModel) -> 'Operation':
        return len(model.get_features())