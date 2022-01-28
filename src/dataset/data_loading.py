"""
Reference: https://github.com/milesial/Pytorch-UNet
"""

import imghdr
import logging
import math
from os import listdir
from os.path import splitext
from pathlib import Path

from imgaug import augmenters as iaa
from imgaug import HeatmapsOnImage

import numpy as np
import torch
import cv2
from torch.utils import data
from torch.utils.data import Dataset

from dataset.dataset_interface import DatasetInterface


class BasicDataset(Dataset):
    def __init__(self, dataset_path: Path, scale: float = 1.0, enable_augmentation: bool = True):
        self.dataset_interface = DatasetInterface(dataset_path)
        self.enable_augmentation = enable_augmentation

        assert 0 < scale <= 1, 'Scale must be between 0 and 1'
        self.scale = scale

        if len(self.dataset_interface) == 0:
            raise RuntimeError(f'Dataset {dataset_path} contains no images, make sure you put your images there')

        logging.info(f'Creating dataset with {len(self.dataset_interface)} examples')

        self.seq = iaa.Sequential([
            iaa.Fliplr(0.5),  # horizontal flips
            iaa.Crop(percent=(0, 0.1)),  # random crops
            # Small gaussian blur with random sigma between 0 and 0.5.
            # But we only blur about 50% of all images.
            iaa.Sometimes(
                0.5,
                iaa.GaussianBlur(sigma=(0, 0.5))
            ),
            # Strengthen or weaken the contrast in each image.
            iaa.LinearContrast((0.75, 1.5)),
            # Add gaussian noise.
            # For 50% of all images, we sample the noise once per pixel.
            # For the other 50% of all images, we sample the noise per pixel AND
            # channel. This can change the color (not only brightness) of the
            # pixels.
            iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
            # Make some images brighter and some darker.
            # In 20% of all cases, we sample the multiplier once per channel,
            # which can end up changing the color of the images.
            iaa.Multiply((0.8, 1.2), per_channel=0.2),
            # Apply affine transformations to each image.
            # Scale/zoom them, translate/move them, rotate them and shear them.
            iaa.Affine(
                scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
                translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
                rotate=(-25, 25),
                shear=(-8, 8)
            )
        ], random_order=True)  # apply augmenters in random order

    def __len__(self):
        return len(self.dataset_interface)

    def augment(self, rs_rgb, rs_depth, zv_depth):
        depths = np.concatenate((rs_depth, zv_depth), axis=2)

        heatmaps = HeatmapsOnImage(depths, min_value=np.min(depths),
                                   max_value=np.max(depths),
                                   shape=rs_rgb.shape)

        augmented = self.seq(image=rs_rgb, heatmaps=heatmaps)
        aug_rs_rgb = augmented[0]
        aug_heatmaps = augmented[1].get_arr()

        aug_rs_depth = aug_heatmaps[..., 0]
        aug_zv_depth = aug_heatmaps[..., 1]

        return aug_rs_rgb, aug_rs_depth, aug_zv_depth

    @classmethod
    def resize(cls, img: np.array, scale: float):
        h, w = img.shape[:2]
        newW, newH = int(scale * w), int(scale * h)

        assert newW > 0 and newH > 0, 'Scale is too small, resized images would have no pixel'
        return cv2.resize(img, (newW, newH), cv2.INTER_LINEAR)

    @classmethod
    def preprocess(cls, img: np.array, scale: float):
        # scale images
        # pil_img = pil_img.resize((newW, newH), resample=Image.BICUBIC)
        img_ndarray = cls.resize(img, scale)

        # normalize images
        if len(img_ndarray.shape) == 2:
            img_ndarray = np.expand_dims(img_ndarray, axis=2)

        img_ndarray = img_ndarray.transpose((2, 0, 1))  # move WxHxC -> CxWxH
        # img_ndarray = img_ndarray / 255                 # [0, 255] -> [0, 1]
        return img_ndarray

    @classmethod
    def preprocess_set(cls, rs_rgb, rs_depth, zv_depth, scale):
        rs_depth = np.expand_dims(rs_depth.astype(np.float32), axis=2)
        zv_depth = np.expand_dims(zv_depth, axis=2)

        assert rs_rgb.shape[:2] == zv_depth.shape[:2], \
            f'Image and mask should be the same size, but are {rs_rgb.shape[:2]} and {zv_depth[:2]}'

        # map nan to numbers
        rs_depth = np.nan_to_num(rs_depth)
        zv_depth = np.nan_to_num(zv_depth)

        processed_rs_rgb = cls.preprocess(rs_rgb, scale)
        processed_rs_depth = cls.preprocess(rs_depth, scale)

        input = np.concatenate((processed_rs_rgb / 255, processed_rs_depth), axis=0)
        label = cls.preprocess(zv_depth, scale)

        return {
            'image': torch.as_tensor(input.copy()).float().contiguous(),
            'mask': torch.as_tensor(label.copy()).float().contiguous()
        }

    def __getitem__(self, idx):
        rs_rgb, rs_depth, _, zv_depth = self.dataset_interface[idx]

        if self.enable_augmentation:
            rs_rgb, rs_depth, zv_depth = self.augment(rs_rgb, rs_depth, zv_depth)

        return self.preprocess_set(rs_rgb, rs_depth, zv_depth, self.scale)
