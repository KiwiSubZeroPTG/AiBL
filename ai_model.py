import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def train_model(save_path="trained_model.h5"):
    # Generate synthetic training data (60% Heads bias)
    data = [1 if np.random.rand() < 0.6 else 0 for _ in range(5000)]
    
    # Create sequences for LSTM
    X = np.array([data[i:i+10] for i in range(len(data)-10)])
    y = np.array(data[10:])
    
    # Build model
    model = Sequential([
        LSTM(32, input_shape=(10, 1)),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy')
    model.fit(X.reshape(-1,10,1), y, epochs=15, verbose=0)
    model.save(save_path)
    return model

class Predictor:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.history = []
    
    def predict_next(self):
        if len(self.history) < 10:
            return np.random.choice(["Heads", "Tails"])
        
        sequence = [1 if x == "Heads" else 0 for x in self.history[-10:]]
        prediction = self.model.predict(np.array([sequence]).reshape(1,10,1))[0][0]
        return "Heads" if prediction > 0.5 else "Tails"
