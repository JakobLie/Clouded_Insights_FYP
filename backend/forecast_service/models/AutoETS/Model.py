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

class AutoETSModel:
    """Holt-Winters - Already works perfectly!"""
    
    def __init__(self):
        self.model_name = "AutoETS"
        self.models = {}  # {series_name: model_params}
        self.series_names = []
        self.is_fitted = False
    
    def train(self, data: Dict[str, List], **kwargs):
        dates = data['months']
        self.series_names = [k for k in data.keys() if k != 'months']
        
        print(f"Training AutoETS for {len(self.series_names)} series...")
        
        for series_name in self.series_names:
            series_data = data[series_name]
            
            # Fit Holt-Winters model
            model = ExponentialSmoothing(
                series_data,
                seasonal_periods=kwargs.get('seasonal_periods', 12),
                trend=kwargs.get('trend', 'add'),
                seasonal=kwargs.get('seasonal', 'add')
            )
            fitted_model = model.fit()
            
            # Store parameters in JSON-serializable format
            self.models[series_name] = {
                'params': {
                    'smoothing_level': float(fitted_model.params['smoothing_level']),
                    'smoothing_trend': float(fitted_model.params.get('smoothing_trend', 0)),
                    'smoothing_seasonal': float(fitted_model.params.get('smoothing_seasonal', 0))
                },
                'level': float(fitted_model.level[-1]) if hasattr(fitted_model, 'level') else None,
                'trend': float(fitted_model.trend[-1]) if hasattr(fitted_model, 'trend') else None,
                'season': fitted_model.season[-kwargs.get('seasonal_periods', 12):].tolist() 
                         if hasattr(fitted_model, 'season') else None,
                'seasonal_periods': kwargs.get('seasonal_periods', 12),
                'trend_type': kwargs.get('trend', 'add'),
                'seasonal_type': kwargs.get('seasonal', 'add')
            }
            
            print(f"  ✓ {series_name}")
        
        self.is_fitted = True
    
    def predict(self, series_name: str, steps: int, **kwargs) -> np.ndarray:
        """Predict single series - Already works!"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
        
        if series_name not in self.models:
            raise ValueError(f"Series '{series_name}' not found in trained models")
        
        model_data = self.models[series_name]
        
        # Simple forecast using stored states
        level = model_data['level']
        trend = model_data['trend']
        season = model_data['season']
        seasonal_periods = model_data['seasonal_periods']
        
        forecasts = []
        for i in range(steps):
            seasonal_component = season[i % seasonal_periods] if season else 0
            forecast = level + (i + 1) * trend + seasonal_component
            forecasts.append(forecast)
        
        return np.array(forecasts)
    
    def save(self, filepath: str) -> None:
        """Save ALL models to ONE JSON file - Already works!"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({
                'model_name': self.model_name,
                'models': self.models,  # All series models
                'series_names': self.series_names
            }, f, indent=2)
        
        print(f"✓ Saved {len(self.models)} AutoETS models to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load ALL models from ONE JSON file - Already works!"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.models = data['models']
            self.series_names = data['series_names']
            self.is_fitted = True
        
        print(f"✓ Loaded {len(self.models)} AutoETS models from {filepath}")
