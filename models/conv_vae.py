from .vae import VAE, Flatten, Stack
import torch.nn as nn
from typing import Optional


class Conv_VAE(VAE):
    def __init__(self, channels: int, height: int, width: int, lr: int,
                 hidden_size: int, alpha: int,
                 dataset: Optional[str] = None,
                 save_images: Optional[bool] = None,
                 save_path: Optional[str] = None):
        super().__init__(hidden_size, alpha, lr,
                         dataset, save_images, save_path)
        # Our code now will look identical to the VAE class except that the
        # encoder and the decoder have been adjusted
        assert not height % 4 and not width % 4, "Choose height and width to "\
            "be divisible by 4"
        self.channels = channels
        self.height = height
        self.width = width
        self.encoder = nn.Sequential(
            nn.Conv2d(self.channels, 8, 3, padding=1), nn.ReLU(),
            nn.BatchNorm2d(8),
            nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2),  # (7x7x64)
            Flatten(),
            nn.Linear(height*width*4, height*width),
            nn.ReLU(),
            nn.Linear(height*width, self.hidden_size),
            nn.ReLU()
        )

        self.decoder = nn.Sequential(
            nn.Linear(self.hidden_size, height*width), nn.ReLU(),
            nn.Linear(height*width, height*width*4),
            nn.ReLU(),
            Stack(64, self.height//4, self.width//4),
            nn.ConvTranspose2d(64, 16, 2, 2), nn.ReLU(),
            nn.ConvTranspose2d(16, channels, 2, 2), nn.Tanh()
        )
