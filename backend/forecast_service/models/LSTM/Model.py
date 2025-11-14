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



class LSTMModel(ForecastModel):
    """LSTM - Train separate model per series, store all in ONE file"""
    
    def __init__(self):
        self.model_name = "LSTM"
        self.models = {}
        self.series_names = []
        self.input_size = None
        self.output_size = None
        self.hidden_size = None
        self.num_layers = None
        self.is_fitted = False
    
    def train(self, data: Dict[str, List], 
              input_size: int = 10,
              output_size: int = 5,
              hidden_size: int = 64,
              num_layers: int = 2,
              epochs: int = 100,
              **kwargs):
        """Train separate LSTM for each series"""
        
        self.series_names = [k for k in data.keys() if k != 'date']
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        print(f"Training LSTM for {len(self.series_names)} series...")
        
        for series_name in self.series_names:
            series_data = data[series_name]
            
            # Create sequences
            X_train, y_train = self._create_sequences([series_data], input_size, output_size)
            
            # Scale
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train.reshape(-1, 1)).reshape(X_train.shape)
            y_train_scaled = scaler.transform(y_train.reshape(-1, 1)).reshape(y_train.shape)
            
            # Convert to tensors
            X_tensor = torch.FloatTensor(X_train_scaled).unsqueeze(-1)
            y_tensor = torch.FloatTensor(y_train_scaled)
            
            # Build model
            model = self._build_model(1, hidden_size, num_layers, output_size)
            
            # Train
            criterion = nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
            
            for epoch in range(epochs):
                model.train()
                optimizer.zero_grad()
                outputs = model(X_tensor)
                loss = criterion(outputs, y_tensor)
                loss.backward()
                optimizer.step()
            
            # Store
            self.models[series_name] = {
                'model': model,
                'scaler': scaler
            }
            
            print(f"  ✓ {series_name}: Final Loss={loss.item():.4f}")
        
        self.is_fitted = True
    
    def _build_model(self, input_dim, hidden_size, num_layers, output_size):
        class LSTMForecaster(nn.Module):
            def __init__(self, input_dim, hidden_size, num_layers, output_size):
                super().__init__()
                self.lstm = nn.LSTM(input_dim, hidden_size, num_layers, batch_first=True)
                self.fc = nn.Linear(hidden_size, output_size)
            
            def forward(self, x):
                lstm_out, _ = self.lstm(x)
                last_output = lstm_out[:, -1, :]
                forecast = self.fc(last_output)
                return forecast
        
        return LSTMForecaster(input_dim, hidden_size, num_layers, output_size)
    
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
            input_tensor = torch.FloatTensor(input_scaled).unsqueeze(0).unsqueeze(-1)
            
            prediction_scaled = model(input_tensor).numpy().flatten()
            prediction = scaler.inverse_transform(prediction_scaled.reshape(-1, 1)).flatten()
            
            return prediction[:steps]
    
    def save(self, filepath: str) -> None:
        """Save ALL models to ONE .pt file"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        models_state = {}
        for series_name, model_data in self.models.items():
            models_state[series_name] = {
                'model_state_dict': model_data['model'].state_dict(),
                'scaler': model_data['scaler']
            }
        
        torch.save({
            'models': models_state,
            'input_size': self.input_size,
            'output_size': self.output_size,
            'hidden_size': self.hidden_size,
            'num_layers': self.num_layers,
            'series_names': self.series_names,
            'is_fitted': self.is_fitted
        }, filepath)
        
        print(f"✓ Saved {len(self.models)} LSTM models to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load ALL models from ONE .pt file"""
        checkpoint = torch.load(filepath, weights_only=False)
        
        self.input_size = checkpoint['input_size']
        self.output_size = checkpoint['output_size']
        self.hidden_size = checkpoint['hidden_size']
        self.num_layers = checkpoint['num_layers']
        self.series_names = checkpoint['series_names']
        self.is_fitted = checkpoint['is_fitted']
        
        self.models = {}
        for series_name, model_state in checkpoint['models'].items():
            model = self._build_model(1, self.hidden_size, self.num_layers, self.output_size)
            model.load_state_dict(model_state['model_state_dict'])
            model.eval()
            
            self.models[series_name] = {
                'model': model,
                'scaler': model_state['scaler']
            }
        
        print(f"✓ Loaded {len(self.models)} LSTM models from {filepath}")