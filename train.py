import argparse, pathlib
import pandas as pd
import torch
from src.model.diffusion import Pipeline
from src.data import StableDiffusionDataset
from src import Trainer


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=pathlib.Path, required=True,
                        help='Path to the dataframe containing data for the training. ' +
                        'Data must contain columns: ["image_path", "prompt"]')
    parser.add_argument('-c', '--config', type=pathlib.Path, default=pathlib.Path('configs', 'default.yaml'),
                        help='Configuration file of the model.')
    parser.add_argument('-e', '--epochs', type=int, default=1)
    parser.add_argument('-d', '--device', type=str, default='cpu',
                        help='Device on which model and dataset will be placed on.')
    parser.add_argument('--batch-size', type=int, default=12,
                        help='Batchsize for the StableDiffusion')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    
    model = Pipeline(
        config=args.config,
        device=args.device
    )
    data = pd.read_csv(str(args.data))
    dataset = StableDiffusionDataset(
        data=data,
        tokenizer=model.tokenizer
    )
    optimizer = torch.optim.Adam(params=model.parameters(), lr=0.01)
    trainer = Trainer(
        model=model, 
        optimizer=optimizer
    )
    trainer.fit()