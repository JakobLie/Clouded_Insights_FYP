from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import json
from typing import Dict, Any, List, Tuple
from pathlib import Path


class ForecastModel(ABC):
    """Base class for all forecasting models"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.is_fitted = False
        self.series_names = []
    
    @abstractmethod
    def train(self, data: Dict[str, List], **kwargs) -> None:
        """Train the model on multiple time series"""
        pass
    
    @abstractmethod
    def predict(self, series_name: str, steps: int, **kwargs) -> np.ndarray:
        """Generate forecasts for a specific series"""
        pass
    
    @abstractmethod
    def save(self, filepath: str) -> None:
        """Save model weights/parameters"""
        pass
    
    @abstractmethod
    def load(self, filepath: str) -> None:
        """Load model weights/parameters"""
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return model metadata"""
        return {
            'model_name': self.model_name,
            'is_fitted': self.is_fitted,
            'series_names': self.series_names
        }