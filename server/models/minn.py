from typing import Any, Dict, List, Tuple, Union

import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init


class MINN(nn.Module):
    """
    Represents a Multi-Input Neural Network (MINN) model.
    """

    def __init__(
        self, input_dim, output_dim, hidden_dim=512, num_heads=8, num_layers=6
    ) -> None:
        """
        Initializes the MINN model.

        Args:
            input_dim (int): The number of input features.
            output_dim (int): The number of output features.
            hidden_dim (int): The number of hidden units.
            num_heads (int): The number of attention heads.
            num_layers (int): The number of layers.
        """
        super(MINN, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_heads = num_heads
        self.num_layers = num_layers

        # Define a self-attention block
        class MultiHeadSelfAttention(nn.Module):
            """
            Represents a multi-head self-attention block.
            """

            def __init__(self, embed_dim, num_heads):
                """
                Initializes the multi-head self-attention block.
                """
                super(MultiHeadSelfAttention, self).__init__()
                self.attention = nn.MultiheadAttention(
                    embed_dim, num_heads, batch_first=True
                )
                self.linear = nn.Linear(embed_dim, embed_dim)
                self.norm = nn.LayerNorm(embed_dim)

            def forward(self, x):
                """
                Defines the forward pass of the multi-head self-attention block.
                """
                attn_output, _ = self.attention(x, x, x)
                x = x + attn_output
                x = self.norm(x)
                return self.linear(x)

        # Define the DenseBlock
        class DenseBlock(nn.Module):
            """
            Represents a dense block.
            """

            def __init__(self, in_features, growth_rate, num_layers):
                """
                Initializes the dense block.
                """
                super(DenseBlock, self).__init__()
                self.layers = nn.ModuleList()
                self.growth_rate = growth_rate
                self.in_features = in_features

                for i in range(num_layers):
                    layer = nn.Sequential(
                        nn.Linear(in_features + i * growth_rate, growth_rate),
                        nn.ReLU(),
                        nn.BatchNorm1d(growth_rate),
                    )
                    self.layers.append(layer)

            def forward(self, x):
                """
                Defines the forward pass of the dense block.
                """
                outputs = [x]
                for layer in self.layers:
                    concatenated = torch.cat(outputs, dim=1)
                    new_feature = layer(concatenated)
                    outputs.append(new_feature)
                return torch.cat(outputs, dim=1)

        # DenseBlock parameters
        dense_growth_rate: int = 128
        dense_layers: int = 4

        # Model layers
        self.self_attention = MultiHeadSelfAttention(input_dim, num_heads)
        self.dense_block = DenseBlock(input_dim, dense_growth_rate, dense_layers)

        final_dense_out = input_dim + dense_growth_rate * dense_layers
        self.fc = nn.Sequential(
            nn.Linear(final_dense_out, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

        # Initialize weights
        self.loaded_weights = False

    def load_weights(self, path) -> None:
        """
        Loads the weights into the model.
        """
        if not os.path.exists(path):
            return "Model file not found"
        self.loaded_weights = torch.load(path, weights_only=True)

    def forward(self, x):
        """
        Defines the forward pass of the MINN model.
        """
        x = self.self_attention(x.unsqueeze(1))
        x = x.squeeze(1)
        x = self.dense_block(x)

        x = self.fc(x)

        if self.loaded_weights is not None:
            return self.loaded_weights
        return x
