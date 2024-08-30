# Real-Time Instrumental Playing Techniques Recognition

![Status: Not Ready](https://img.shields.io/badge/status-not%20ready-red)

## Installation

```
git clone https://github.com/nbrochec/realtimeIPTrecognition/
```

```
conda create --name IPT python=3.11.7
conda activate IPT
```

```
pip install -r requirements.txt
```

## Folder structure

```
└── 📁data
    └── 📁dataset
    └── 📁raw_data
        └── 📁test
        └── 📁train
└── 📁externals
    └── 📁pytorch_balanced_sampler
        └── __init__.py
        └── sampler.py
        └── utils.py
└── 📁models
    └── __init__.py
    └── layers.py
    └── models.py
    └── utils.py
└── 📁utils
    └── __init__.py
    └── augmentation.py
    └── utils.py
└── LICENCE
└── preprocess.py
└── README.md
└── requirements.txt
└── train.py
```

## Usage
### Dataset preparation

You can drag and drop the folder containing your training audio files into the `/data/dataset/raw_sample/train` folder, and your test audio files into the `/data/dataset/raw_sample/test` folder.

Test and train folders must share the same names for IPT classes. Such as shown below:
```
└── 📁test
    └── 📁myTestDataset
        └── 📁IPTclass_1
        └── 📁IPTclass_2
        └── ...
└── 📁train
    └── 📁myTrainingDataset
        └── 📁IPTclass_1
        └── 📁IPTclass_2
        └── ...
```

You can use multiple training datasets. They must share the same names for IPT classes as well.

```
└── 📁train
    └── 📁myTrainingDataset1
        └── 📁IPTclass_1
        └── 📁IPTclass_2
        └── ...
    └── 📁myTrainingDataset2
        └── 📁IPTclass_1
        └── 📁IPTclass_2
        └── ...
    └── ...
```

### Preprocess your datasets
To preprocess your datasets, use the following command:
```
python preprocess.py --name project_name
```

A CSV file will be saved in the `/data/dataset/` folder with the following syntax:
```
project_name_dataset_split.csv
```

### Training
There are many different configurations for training your model. The only required argument is the name of your project such as shown below:
```
python train.py --name project_name
```

| Argument            | Description                                                         | Possible Values                |
|---------------------|---------------------------------------------------------------------|--------------------------------|
| `--config`          | Name of the model's architecture.                                  | `v1`, `v2`, `one-residual`, `two-residual`, `transformer`|
| `--device`          | Device to use for training.                                        | `cpu`, `cuda`, `mps`           |
| `--gpu`             | GPU selection to use.                                              | `0`, `1`, ...                  |
| `--sr`              | Sampling rate to downsample the audio files.                        | 16000, 22050, 24000, |
| `--segment_overlap` | Overlap between audio segments.                                    | `True` or `False`        |
| `--fmin`            | Minimum frequency for Mel filters.                                 | Numerical value (Hz)           |
| `--lr`              | Learning rate for the optimizer.                                   | 0.001, 0.01, etc.              |
| `--epochs`          | Number of training epochs.                                         | Integer value                  |
| `--early_stopping`  | Number of epochs without improvement before early stopping.         | Integer value or `None`        |
| `--reduceLR`        | Reduce learning rate if validation plateaus.                       | `True`, `False`                |
| `--export_ts`       | Export the model as a TorchScript file (`.ts` format).              | `True`, `False`                |

Training your model will create a `runs` folder and a subfolder with the name of your project.
If you use early stopping, checkpoints of the last best model will be saved in the `/runs/project_name/checkpoints/` folder.
```
└── 📁runs
    └── 📁project_name
        └── 📁checkpoints
```

After the training, the script will automatically save the best model checkpoints in the `/runs/project_name/` folder.
If you use export_ts, the `.ts` file will also be saved in this folder.

### Running the mode in real-time

[...]

## Related research works
• Nicolas Brochec, Tsubasa Tanaka, Will Howie. [Microphone-based Data Augmentation for Automatic Recognition of Instrumental Playing Techniques](https://hal.science/hal-04642673). International Computer Music Conference (ICMC 2024), Jul 2024, Seoul, South Korea.

• Nicolas Brochec and Tsubasa Tanaka. [Toward Real-Time Recognition of Instrumental Playing Techniques for Mixed Music: A Preliminary Analysis](https://hal.science/hal-04263718). International Computer Music Conference (ICMC 2023), Oct 2023, Shenzhen, China.

• Marco Fiorini and Nicolas Brochec. [Guiding Co-Creative Musical Agents through Real-Time Flute Instrumental Playing Technique Recognition](https://hal.science/hal-04635907). Sound and Music Computing Conference (SMC 2024), Jul 2024, Porto, Portugal.

## Related Datasets
• Nicolas Brochec and Will Howie. [GFDatabase: A Database of Flute Playing Techniques](https://doi.org/10.5281/zenodo.10932398) (version 1.0.1). Zenodo, 2024.

## Acknowledgments

This project uses code from the [pytorch_balanced_sampler](https://github.com/khornlund/pytorch-balanced-sampler) repository created by Karl Hornlund.

## Funding

This work has been supported by the ERC Reach (Raising Co-creativity in Cyber-Human Musicianship) directed by Gérard Assayag.
