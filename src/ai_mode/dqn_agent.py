import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque
from typing import List, Tuple

class DQN(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super(DQN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.network(x)

class DQNAgent:
    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95  # İndirim faktörü
        self.epsilon = 1.0  # Keşif oranı
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.batch_size = 64
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # DQN ağları
        self.model = DQN(state_size, 256, action_size).to(self.device)
        self.target_model = DQN(state_size, 256, action_size).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.update_target_model()

    def update_target_model(self):
        """Hedef modeli güncelle"""
        self.target_model.load_state_dict(self.model.state_dict())

    def remember(self, state: np.ndarray, action: int, reward: float, 
                next_state: np.ndarray, done: bool):
        """Deneyimi hafızaya ekle"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state: np.ndarray, training: bool = True) -> int:
        """Duruma göre aksiyon seç"""
        if training and random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            action_values = self.model(state)
        return torch.argmax(action_values).item()

    def replay(self) -> float:
        """Hafızadan örnek alıp eğitim yap"""
        if len(self.memory) < self.batch_size:
            return 0.0

        minibatch = random.sample(self.memory, self.batch_size)
        states = torch.FloatTensor([x[0] for x in minibatch]).to(self.device)
        actions = torch.LongTensor([x[1] for x in minibatch]).to(self.device)
        rewards = torch.FloatTensor([x[2] for x in minibatch]).to(self.device)
        next_states = torch.FloatTensor([x[3] for x in minibatch]).to(self.device)
        dones = torch.FloatTensor([x[4] for x in minibatch]).to(self.device)

        # Mevcut Q değerleri
        current_q_values = self.model(states).gather(1, actions.unsqueeze(1))

        # Hedef Q değerleri
        with torch.no_grad():
            next_q_values = self.target_model(next_states).max(1)[0]
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        # Kayıp hesapla ve optimize et
        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Epsilon değerini güncelle
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        return loss.item()

    def get_state(self, snake_head: Tuple[int, int], snake_body: List[Tuple[int, int]], 
                 food_pos: Tuple[int, int], width: int, height: int) -> np.ndarray:
        """Oyun durumunu AI'nin anlayabileceği formata dönüştür"""
        state = []
        
        # Yılanın yönelimleri (4 yön)
        head_x, head_y = snake_head
        if len(snake_body) >= 2:
            # Yılanın mevcut yönünü belirle
            dx = snake_body[0][0] - snake_body[1][0]
            dy = snake_body[0][1] - snake_body[1][1]
            state.extend([
                1 if dx == 20 and dy == 0 else 0,  # Sağ
                1 if dx == -20 and dy == 0 else 0,  # Sol
                1 if dx == 0 and dy == -20 else 0,  # Yukarı
                1 if dx == 0 and dy == 20 else 0   # Aşağı
            ])
        else:
            # Başlangıç durumu için varsayılan yön (sağ)
            state.extend([1, 0, 0, 0])
        
        # Yemeğin yılan başına göre konumu
        food_x, food_y = food_pos
        state.extend([
            food_x < head_x,  # Yemek solda mı
            food_x > head_x,  # Yemek sağda mı
            food_y < head_y,  # Yemek yukarıda mı
            food_y > head_y   # Yemek aşağıda mı
        ])
        
        # Tehlike algılama (her yön için)
        for dx, dy in [(20,0), (-20,0), (0,-20), (0,20)]:  # Sağ, Sol, Yukarı, Aşağı
            next_x = head_x + dx
            next_y = head_y + dy
            
            # Duvar veya vücut parçası var mı kontrol et
            danger = (
                next_x < 0 or
                next_x >= width or
                next_y < 0 or
                next_y >= height or
                (next_x, next_y) in snake_body[:-1]
            )
            state.append(1 if danger else 0)

        return np.array(state, dtype=np.float32)

    def save(self, filepath: str):
        """Modeli kaydet"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon
        }, filepath)

    def load(self, filepath: str):
        """Modeli yükle"""
        checkpoint = torch.load(filepath)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon']
        self.update_target_model() 