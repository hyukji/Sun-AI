import torch
from torch import nn
import copy
import torch.nn.functional as F
from torch.utils.data import Dataset

class LSTM_Model(torch.nn.Module): 
    def __init__(self, input_dim, hidden_dim, output_dim, layers, target_date):
        super(LSTM_Model, self).__init__()
        self.lstm = torch.nn.LSTM(input_dim, hidden_dim, num_layers = layers, batch_first = True)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, target_date * 48, bias = True),
            nn.BatchNorm1d(target_date * 48),

            nn.Linear(target_date * 48, output_dim * target_date * 48, bias = True),
            nn.BatchNorm1d(output_dim * target_date * 48),
        )

    def forward(self, x):
        x, _status = self.lstm(x)
        x = self.fc(x[:, -1])
        return x


class Day7_Model(nn.Module):
    def __init__(self, len_features, len_quantile = 9):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(len_features, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),

            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),

            nn.Linear(128, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),

            nn.Linear(32, len_quantile)
        )

    def forward(self, x):
        x = self.fc(x)

        return x

    def _day(self):
        return "Day7"

class Day8_Model(nn.Module):
    def __init__(self, len_features, len_quantile = 9):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(len_features, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),

            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),

            nn.Linear(128, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),

            nn.Linear(32, len_quantile)
        )

    def forward(self, x):
        x = self.fc(x)

        return x
    
    def _day(self):
        return "Day8"