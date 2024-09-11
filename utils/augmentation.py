#############################################################################
# augmentations.py 
# Nicolas Brochec
# TOKYO UNIVERSITY OF THE ARTS
# 東京藝術大学音楽音響創造科
# ERC Reach
# GNU General Public License v3.0
#############################################################################
# Code description:
# Implement data augmentation methods
#############################################################################

import torch
from audiomentations import PitchShift, AddColorNoise, Shift, PolarityInversion, Gain, HighPassFilter, LowPassFilter, Mp3Compression, ClippingDistortion, BitCrush, AirAbsorption
import torch.nn.functional as F
import numpy as np
import librosa

'''
Principally using torch_audiomentations because:
1. Augmentations are applied inside the training loop.
2. torch_audiomentations enables GPU computation to generate augmentated data.
'''

class ApplyAugmentations:
    def __init__(self, augmentations, sample_rate, device):
        """
        Initializes the augmentation class with the list of augmentations to apply.

        Parameters
        ----------
        augmentations : list
            List of names of augmentations to apply.
        """
        self.augmentations = augmentations
        self.sr = sample_rate
        self.device = device

    def apply(self, data):
        """
        Applies the selected augmentations to the given data.
        """
        data = data.cpu().squeeze(1).detach().numpy()

        original_size = data.shape[1]
        augmented_data_list = []

        augmentations_dict = {
            'pitchshift': self.pitch_shift,
            'lb_pitchshift': self.lb_pitch_shift,
            'timeshift': self.shift,
            'addnoise': self.add_noise,
            'polarityinversion': self.polarity_inversion,
            'gain': self.gain,
            'hpf': self.highpassfilter,
            'lpf': self.lowpassfilter,
            'clipping': self.clippingdisto,
            'bitcrush': self.bitcrush,
            'airabso': self.airabso
        }

        for augmentation in self.augmentations:
            if augmentation == 'all':
                aug_data = [
                    augmentations_dict['pitchshift'](data),
                    augmentations_dict['lb_pitchshift'](data),
                    augmentations_dict['timeshift'](data),
                    augmentations_dict['addnoise'](data),
                    augmentations_dict['polarityinversion'](data),
                    augmentations_dict['gain'](data),
                    augmentations_dict['hpf'](data),
                    augmentations_dict['lpf'](data),
                    augmentations_dict['clipping'](data),
                    augmentations_dict['bitcrush'](data),
                    augmentations_dict['airabso'](data)
                ]
                augmented_data_list.extend(aug_data)
                continue 

            aug_data = augmentations_dict.get(augmentation, lambda x: x)(data)
            aug_data = self.pad_or_trim(aug_data, original_size)
            augmented_data_list.append(aug_data)

        augmented_data_list = [torch.tensor(d).unsqueeze(1) for d in augmented_data_list] 
        augmented_data = torch.cat(augmented_data_list, dim=0).to(self.device)

        return augmented_data

    def pad_or_trim(self, data, original_size):
        current_size = data.shape[1]
        
        if current_size > original_size:
            data = data[..., :original_size]
        elif current_size < original_size:
            padding = (0, original_size - current_size)
            data = np.pad(data, pad_width=padding, mode='constant', constant_values=0)
        
        return data

    def pitch_shift(self, data):
        transform = PitchShift(min_semitones=-12.0, max_semitones=12.0, p=1)
        return transform(data, sample_rate= self.sr)
    
    def lb_pitch_shift(self, data):
        ra = np.random.randint(-24, 24, dtype=int)
        data = librosa.effects.pitch_shift(data, sr=self.sr, bins_per_octave=24, n_steps=ra)
        return data

    def shift(self, data):
        transform = Shift(rollover=True, p=1)
        return transform(data, sample_rate= self.sr)

    def add_noise(self, data):
        transform = AddColorNoise(p=1)
        return transform(data, sample_rate=self.sr)
    
    def polarity_inversion(self, data):
        transform = PolarityInversion(p=1)
        return transform(data, sample_rate= self.sr)
    
    def gain(self, data):
        transform = Gain(p=1)
        return transform(data, sample_rate= self.sr)
    
    def highpassfilter(self, data):
        transform = HighPassFilter(p=1)
        return transform(data, sample_rate=self.sr)
    
    def lowpassfilter(self, data):
        transform = LowPassFilter(p=1)
        return transform(data, sample_rate=self.sr)
    
    def clippingdisto(self, data):
        transform = ClippingDistortion(p=1)
        return transform(data, sample_rate=self.sr)
    
    def bitcrush(self, data):
        transform = BitCrush(p=1)
        return transform(data, sample_rate=self.sr)
    
    def airabso(self, data):
        transform = AirAbsorption(p=1)
        return transform(data, sample_rate=self.sr)
    
    def get_aug_nbr(self):
        aug_nbr = len(self.augmentations)
        if self.augmentations == ['all']:
            aug_nbr = 11
        return aug_nbr