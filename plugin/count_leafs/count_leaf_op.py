from core.frozen_points_domain import Operation
from core.frozen_points_domain import FeatureModel

class CountLeafs(Operation):

    def execute(self, model: FeatureModel) -> 'Operation':
        result = 0
        for feat in model.get_features():
            if len(feat.get_relations())==0:
                result= result +1
        return result
