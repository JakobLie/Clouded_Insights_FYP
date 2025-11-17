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


class NBeatsModel(ForecastModel):
    """
    N-BEATS - Train separate model per series, store all in ONE file.
    This matches the statistical models' behavior.
    """
    
    def __init__(self):
        self.model_name = "N-BEATS"
        self.models = {}  # {series_name: {'model': model, 'scaler': scaler}}
        self.series_names = []
        self.input_size = None
        self.output_size = None
        self.is_fitted = False
    
    def train(self, data: Dict[str, List], 
              input_size: int = 10, 
              output_size: int = 5,
              epochs: int = 100,
              **kwargs):
        """Train separate N-BEATS model for each series"""
        
        self.series_names = [k for k in data.keys() if k != 'months']
        self.input_size = input_size
        self.output_size = output_size
        
        print(f"Training N-BEATS for {len(self.series_names)} series...")
        
        for series_name in self.series_names:
            series_data = data[series_name]
            
            # Create sequences for this series
            X_train, y_train = self._create_sequences([series_data], input_size, output_size)
            
            # Scale data
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train.reshape(-1, 1)).reshape(X_train.shape)
            y_train_scaled = scaler.transform(y_train.reshape(-1, 1)).reshape(y_train.shape)
            
            # Convert to tensors
            X_tensor = torch.FloatTensor(X_train_scaled)
            y_tensor = torch.FloatTensor(y_train_scaled)
            
            # Build and train model for this series
            model = self._build_model(input_size, output_size)
            criterion = nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
            
            for epoch in range(epochs):
                model.train()
                optimizer.zero_grad()
                outputs = model(X_tensor)
                loss = criterion(outputs, y_tensor)
                loss.backward()
                optimizer.step()
            
            # Store model and scaler
            self.models[series_name] = {
                'model': model,
                'scaler': scaler
            }
            
            print(f"  ✓ {series_name}: Final Loss={loss.item():.4f}")
        
        self.is_fitted = True
    
    def _build_model(self, input_size, output_size):
        class SimpleNBeats(nn.Module):
            def __init__(self, input_size, output_size):
                super().__init__()
                self.fc1 = nn.Linear(input_size, 128)
                self.fc2 = nn.Linear(128, 128)
                self.fc3 = nn.Linear(128, output_size)
                self.relu = nn.ReLU()
            
            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.relu(self.fc2(x))
                x = self.fc3(x)
                return x
        
        return SimpleNBeats(input_size, output_size)
    
    def _create_sequences(self, series_list, input_size, output_size):
        X, y = [], []
        for series in series_list:
            for i in range(len(series) - input_size - output_size + 1):
                X.append(series[i:i + input_size])
                y.append(series[i + input_size:i + input_size + output_size])
        return np.array(X), np.array(y)
    
    def predict(self, series_name: str, steps: int, last_values: List[float] = None, **kwargs) -> np.ndarray:
        """Predict single series - Now uses correct model!"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
        
        if series_name not in self.models:
            raise ValueError(f"Series '{series_name}' not found. Available: {self.series_names}")
        
        if last_values is None or len(last_values) < self.input_size:
            raise ValueError(f"Need at least {self.input_size} historical values")
        
        # Get the model trained for THIS specific series
        model_data = self.models[series_name]
        model = model_data['model']
        scaler = model_data['scaler']
        
        model.eval()
        with torch.no_grad():
            input_data = np.array(last_values[-self.input_size:])
            input_scaled = scaler.transform(input_data.reshape(-1, 1)).flatten()
            input_tensor = torch.FloatTensor(input_scaled).unsqueeze(0)
            
            prediction_scaled = model(input_tensor).numpy().flatten()
            prediction = scaler.inverse_transform(prediction_scaled.reshape(-1, 1)).flatten()
            
            return prediction[:steps]
    
    def save(self, filepath: str) -> None:
        """Save ALL models to ONE .pt file"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Extract state dicts from all models
        models_state = {}
        for series_name, model_data in self.models.items():
            models_state[series_name] = {
                'model_state_dict': model_data['model'].state_dict(),
                'scaler': model_data['scaler']
            }
        
        torch.save({
            'models': models_state,  # All series models
            'input_size': self.input_size,
            'output_size': self.output_size,
            'series_names': self.series_names,
            'is_fitted': self.is_fitted
        }, filepath)
        
        print(f"✓ Saved {len(self.models)} N-BEATS models to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load ALL models from ONE .pt file"""
        checkpoint = torch.load(filepath, weights_only=False)
        
        self.input_size = checkpoint['input_size']
        self.output_size = checkpoint['output_size']
        self.series_names = checkpoint['series_names']
        self.is_fitted = checkpoint['is_fitted']
        
        # Reconstruct all models
        self.models = {}
        for series_name, model_state in checkpoint['models'].items():
            model = self._build_model(self.input_size, self.output_size)
            model.load_state_dict(model_state['model_state_dict'])
            model.eval()
            
            self.models[series_name] = {
                'model': model,
                'scaler': model_state['scaler']
            }
        
        print(f"✓ Loaded {len(self.models)} N-BEATS models from {filepath}")