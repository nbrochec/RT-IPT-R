#############################################################################
# train.py 
# Nicolas Brochec
# TOKYO UNIVERSITY OF THE ARTS
# 東京藝術大学音楽音響創造科
# ERC Reach
# GNU General Public License v3.0
#############################################################################
# Code description:
# Script to train the model
#############################################################################

import argparse, sys, math, os
import torch, torchaudio, h5py
from glob import glob
from os.path import join

from models import *
from utils import *

parser = argparse.ArgumentParser(description='train CNN model for RT-IPT-R')
parser.add_argument('--dataset_dir', type=str, help='dataset directory where h5 files are saved', default='data/processed_data/')
parser.add_argument('--epochs', type=int, help='number of train epochs', default=100)
parser.add_argument('--config', type=str, help='version of the CNN', default='v2')
parser.add_argument('--device', type=str, help='gpu device', default='cpu')
parser.add_argument('--gpu', type=int, help='gpu device number', default=0)
parser.add_argument('--augment', type=str, help='augmentations', default='pitchshift')
parser.add_argument('--early_stopping', type=bool, help='early stopping', default=False)
parser.add_argument('--reduceLR', type=bool, help='reduce LR on plateau', default=False)
parser.add_argument('--lr', type=float, help='learning rate', default=0.001)
parser.add_argument('--fmin', type=int, help='select min frequency for logmelspec analysis', default=150)

"""
Command example:
python train.py --config v1 --augment pitchshift --early_stopping True --reduceLR True 
"""

args = parser.parse_args()

if not args.dataset_dir:
    print('Error: dataset directory is required to launch training.')
    print('Please indicate the path of the dataset directory.')
    parser.print_help()
    sys.exit(1)

train_hdf5_file_path = join(args.dataset_dir, "train_data.h5")
data_loader_factory = BalancedDataLoader(train_hdf5_file_path)

balanced_loader = data_loader_factory.get_dataloader()
for batch_data, batch_labels in balanced_loader:
    print(f"Batch data shape: {batch_data.shape}")
    print(f"Batch labels shape: {batch_labels.shape}")
    print("Train data samples have been loaded.")
    break

test_hdf5_file_path = join(args.dataset_dir, "test_data.h5")
test_loader = HDF5Dataset(test_hdf5_file_path)
print("Test data samples have been loaded.")

val_hdf5_file_path = join(args.dataset_dir, "val_data.h5")
val_loader = HDF5Dataset(val_hdf5_file_path)
print("validation data samples have been loaded.")

num_labels = test_loader.get_num_classes()

model = LoadModel().get_model(args.config, num_labels).to(args.device)
summary = ModelSummary(model, num_labels, args.config)
summary.print_summary()

tester = ModelTester(model, input_shape=(1, 1, 7680), device=args.device)
output = tester.test()
if output.size(1) == num_labels:
    pass
else:
    print("Error: output dimension do not correspond to the number of classes")
    sys.exit(1)

# Training loop (to be completed with validation data)
# augmentations = args.augment.split()
# augmentation_instance = ApplyAugmentations(augmentations)

# for batch_data, batch_labels in balanced_loader:
#     # Apply augmentations
#     augmented_data = []
#     augmented_labels = []

#     for i in range(batch_data.size(0)):  # Use size(0) to get batch size
#         sample_data = batch_data[i]
#         sample_labels = batch_labels[i]
        
#         augmented_samples = augmentation_instance.apply(sample_data.unsqueeze(0))
#         num_samples = augmented_samples.size(0)

#         augmented_data.append(augmented_samples)
#         augmented_labels.extend([sample_labels] * num_samples)

#     # Concatenate augmented data and labels
#     batch_data = torch.cat(augmented_data, dim=0)
#     batch_labels = torch.tensor(augmented_labels, dtype=torch.long)