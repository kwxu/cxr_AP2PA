import os
import pandas as pd
from src.utils import mkdir_p, read_file_contents_list
from collections import Counter
from PIL import Image


dataset_root = '/nfs/masi/CXR_public/CXR8'
# image_dir = os.path.join(dataset_root, 'images/images')
image_dir = '/nfs/masi/xuk9/src/cxr_vp_classifier/nih_image_dir/image'
label_csv = os.path.join(dataset_root, 'Data_Entry_2017_v2020.csv')
train_val_list = os.path.join(dataset_root, 'images/train_val_list.txt')
test_list = os.path.join(dataset_root, 'images/test_list.txt')


def process_single_cxr(in_path, out_path):
    """
    1) Resize to 256x256,
    2) Make sure all single channel gray scale
    :param in_path:
    :param out_path:
    :return:
    """
    image_data = Image.open(in_path).convert('L')
    image_data = image_data.resize((256, 256))
    print(f'Save preprocessed image to {out_path}')
    image_data.save(out_path)


def create_cyclegan_folder():
    """
    + trainA - AP in train/val set
    + trainB - PA in train/val set
    + testA - AP in test set
    + testB - PA in test set
    :return:
    """
    output_root = '/nfs/masi/xuk9/src/cxr_AP2PA/datasets/nih_cxr'

    out_dir_dict = {
        'trainA': os.path.join(output_root, 'trainA'),
        'trainB': os.path.join(output_root, 'trainB'),
        'testA': os.path.join(output_root, 'testA'),
        'testB': os.path.join(output_root, 'testB')
    }

    for dir in out_dir_dict:
        mkdir_p(out_dir_dict[dir])

    label_df = pd.read_csv(label_csv).set_index('Image Index')

    vp_all = label_df['View Position'].to_list()
    print('VP counter for all:')
    print(Counter(vp_all))

    # Get the train_val subset
    train_val_file_name_list = read_file_contents_list(train_val_list)
    print(f'Number of files: {len(train_val_file_name_list)}')
    # Get the test subset
    test_file_name_list = read_file_contents_list(test_list)
    print(f'Number of files: {len(test_file_name_list)}')

    train_val_df = label_df.loc[train_val_file_name_list]
    test_df = label_df.loc[test_file_name_list]

    split_info_dict = {
        'trainA': {
            'dir': os.path.join(output_root, 'trainA'),
            'imgs': train_val_df[train_val_df['View Position'] == 'AP'].index.values.tolist()
        },
        'trainB': {
            'dir': os.path.join(output_root, 'trainB'),
            'imgs': train_val_df[train_val_df['View Position'] == 'PA'].index.values.tolist()
        },
        'testA': {
            'dir': os.path.join(output_root, 'testA'),
            'imgs': test_df[test_df['View Position'] == 'AP'].index.values.tolist()
        },
        'testB': {
            'dir': os.path.join(output_root, 'testB'),
            'imgs': test_df[test_df['View Position'] == 'PA'].index.values.tolist()
        }
    }

    for split in split_info_dict:
        mkdir_p(split_info_dict[split]['dir'])

        iCount = 0
        split_num_image = len(split_info_dict[split]['imgs'])
        for image_file in split_info_dict[split]['imgs']:
            print(f'Process [{iCount} / {split_num_image}] of split [{split}]')
            in_file_path = os.path.join(image_dir, image_file)
            out_file_path = os.path.join(split_info_dict[split]['dir'], image_file)
            process_single_cxr(in_file_path, out_file_path)
            iCount += 1


def main():
    create_cyclegan_folder()


if __name__ == "__main__":
    main()
