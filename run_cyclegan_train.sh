#!/usr/bin/env bash

AP2PA_root=/nfs/masi/xuk9/src/cxr_AP2PA

train_model () {
    set -o xtrace
    python /nfs/masi/xuk9/src/pytorch-CycleGAN-and-pix2pix/train.py \
        --dataroot ${AP2PA_root}/datasets/nih_cxr \
        --name experiment_1 \
        --checkpoints_dir ${AP2PA_root}/result/experiment_1/checkpoints \
        --model cycle_gan \
        --input_nc 1 \
        --output_nc 1 \
        --dataset_mode unaligned \
        --direction AtoB \
        --load_size 256 \
        --crop_size 256 \
        --preprocess none \
        --no_flip \
        --verbose
    set +o xtrace
}


train_model
