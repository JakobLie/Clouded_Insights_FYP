from ..ForecastModel import ForecastModel

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import json
from typing import Dict, Any, List, Tuple
from pathlib import Path
import pickle

import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class SARIMAXModel(ForecastModel):
    """SARIMAX model - stores separate model per series in ONE file"""
    
    def __init__(self):
        self.model_name = "SARIMAX"
        self.models = {}  # {series_name: fitted_model_object}
        self.series_names = []
        self.is_fitted = False
        self.training_data = {}  # Store for predictions
    
    def train(self, data: Dict[str, List], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), **kwargs):
        dates = data['months']
        self.series_names = [k for k in data.keys() if k != 'months']
        
        print(f"Training SARIMAX for {len(self.series_names)} series...")
        
        for series_name in self.series_names:
            series_data = data[series_name]
            
            # Fit SARIMAX model
            model = SARIMAX(series_data, order=order, seasonal_order=seasonal_order)
            fitted_model = model.fit(disp=False)
            
            # Store the FITTED model (not just parameters)
            self.models[series_name] = fitted_model
            # Store training data for predictions
            self.training_data[series_name] = series_data
            
            print(f"  ✓ {series_name}: AIC={fitted_model.aic:.2f}")
        
        self.is_fitted = True
    
    def predict(self, series_name: str, steps: int, **kwargs) -> np.ndarray:
        """Predict single series"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
        
        if series_name not in self.models:
            raise ValueError(f"Series '{series_name}' not found in trained models")
        
        # Use statsmodels' forecast method
        fitted_model = self.models[series_name]
        forecast = fitted_model.forecast(steps=steps)
        
        return np.array(forecast)
    
    def save(self, filepath: str) -> None:
        """Save ALL models to ONE file using pickle"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Pickle can serialize statsmodels objects
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model_name': self.model_name,
                'models': self.models,  # All fitted models
                'series_names': self.series_names,
                'training_data': self.training_data,
                'is_fitted': self.is_fitted
            }, f)
        
        print(f"✓ Saved {len(self.models)} SARIMAX models to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load ALL models from ONE file"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.models = data['models']
            self.series_names = data['series_names']
            self.training_data = data.get('training_data', {})
            self.is_fitted = data['is_fitted']
        
        print(f"✓ Loaded {len(self.models)} SARIMAX models from {filepath}")
