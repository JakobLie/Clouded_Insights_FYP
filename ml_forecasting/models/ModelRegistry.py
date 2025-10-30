from .ForecastModel import ForecastModel

from .SARIMAX.Model import  SARIMAXModel
from .AutoETS.Model import AutoETSModel
from .LSTM.Model import LSTMModel
from .NBEATS.Model import NBeatsModel

from typing import Dict, Any, List, Tuple

class ModelRegistry:
    """Factory for creating and loading models"""
    
    _models = {
        'sarimax': SARIMAXModel,
        'autoets': AutoETSModel,
        'nbeats': NBeatsModel,
        'lstm': LSTMModel
    }
    
    # Instantiate empty model object, typically for training
    @classmethod
    def create(cls, model_type: str) -> ForecastModel:
        if model_type not in cls._models:
            raise ValueError(f"Unknown model: {model_type}. Available: {list(cls._models.keys())}")
        return cls._models[model_type]()
    
    # Instantiate model object with specified weights (by path)
    @classmethod
    def load_model(cls, model_type: str, filepath: str) -> ForecastModel:
        model = cls.create(model_type)
        model.load(filepath)
        return model
    
    @classmethod
    def list_models(cls) -> List[str]:
        return list(cls._models.keys())