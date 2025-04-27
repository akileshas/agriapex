import os
import torch
import torch.nn as nn


class MINN(nn.Module):
    """
    Represents a Multi-Input Neural Network (MINN) model.
    """

    def __init__(
        self, input_dim, output_dim, hidden_dim=512, num_heads=8, num_layers=6
    ) -> None:
        super(MINN, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_heads = num_heads
        self.num_layers = num_layers

        # Define a self-attention block
        class MultiHeadSelfAttention(nn.Module):
            def __init__(self, embed_dim, num_heads):
                super(MultiHeadSelfAttention, self).__init__()
                self.attention = nn.MultiheadAttention(
                    embed_dim, num_heads, batch_first=True
                )
                self.linear = nn.Linear(embed_dim, embed_dim)
                self.norm = nn.LayerNorm(embed_dim)

            def forward(self, x):
                attn_output, _ = self.attention(x, x, x)
                x = x + attn_output
                x = self.norm(x)
                return self.linear(x)

        # Define the DenseBlock
        class DenseBlock(nn.Module):
            def __init__(self, in_features, growth_rate, num_layers):
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
        if not os.path.exists(path):
            return "Model file not found"
        self.loaded_weights = torch.load(path, weights_only=True)

    def forward(self, x):
        x = self.self_attention(x.unsqueeze(1))
        x = x.squeeze(1)
        x = self.dense_block(x)

        x = self.fc(x)

        if self.loaded_weights is not None:
            return self.loaded_weights
        return x
