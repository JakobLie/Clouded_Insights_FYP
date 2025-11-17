from ..ForecastModel import ForecastModel

import numpy as np
from typing import Dict, Any, List
from pathlib import Path
import json


class StaticModel(ForecastModel):
    """Static model - returns the last observed value for all forecast steps"""
    
    def __init__(self):
        self.model_name = "Static"
        self.series_names = []
        self.last_values = {}  # {series_name: last_observed_value}
        self.is_fitted = False
    
    def train(self, data: Dict[str, List], **kwargs) -> None:
        """Store the last value of each series"""
        self.series_names = [k for k in data.keys() if k != 'date']
        
        print(f"Training Static model for {len(self.series_names)} series...")
        
        for series_name in self.series_names:
            series_data = data[series_name]

            # Store the last observed value
            self.last_values[series_name] = series_data[-1]

            print(f"  ✓ {series_name}: last_value={self.last_values[series_name]:.4f}")
        
        self.is_fitted = True
    
    def predict(self, series_name: str, steps: int, **kwargs) -> np.ndarray:
        """Return the last observed value repeated for all forecast steps"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
        
        if series_name not in self.last_values:
            raise ValueError(f"Series '{series_name}' not found in trained models")
        
        # Return array of the last value repeated 'steps' times
        return np.full(steps, self.last_values[series_name])
    
    def save(self, filepath: str) -> None:
        """Save last values to JSON file"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        save_data = {
            'model_name': self.model_name,
            'last_values': self.last_values,
            'series_names': self.series_names,
            'is_fitted': self.is_fitted
        }
        
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"✓ Saved Static model with {len(self.last_values)} series to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load last values from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.last_values = data['last_values']
            self.series_names = data['series_names']
            self.is_fitted = data['is_fitted']
        
        print(f"✓ Loaded Static model with {len(self.last_values)} series from {filepath}")