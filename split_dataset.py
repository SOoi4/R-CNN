# Split dataset into train / val / test folders

from pathlib import Path
import random
import os
import sys
import shutil
import argparse

# Define and parse user input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--datapath', help='Path to data folder containing image and annotation files',
                    required=True)
parser.add_argument('--train_pct', help='Ratio of images to go to train folder (example: ".7")',
                    default=0.7, type=float)
parser.add_argument('--test_pct', help='Ratio of images to go to test folder (example: ".2")',
                    default=0.2, type=float)

args = parser.parse_args()

data_path = args.datapath
train_percent = float(args.train_pct)
test_percent = float(args.test_pct)

# Check for valid entries
if not os.path.isdir(data_path):
    print('Directory specified by --datapath not found.')
    sys.exit(0)

if (train_percent + test_percent) >= 1.0:
    print('train_pct + test_pct must be less than 1.0, leaving room for validation.')
    sys.exit(0)

val_percent = 1.0 - (train_percent + test_percent)

# Define path to input dataset
input_image_path = os.path.join(data_path, 'images')
input_label_path = os.path.join(data_path, 'labels')

# Define paths to train/val/test folders
cwd = os.getcwd()
train_img_path = os.path.join(cwd, 'data/train/images')
train_lbl_path = os.path.join(cwd, 'data/train/labels')
val_img_path = os.path.join(cwd, 'data/validation/images')
val_lbl_path = os.path.join(cwd, 'data/validation/labels')
test_img_path = os.path.join(cwd, 'data/test/images')
test_lbl_path = os.path.join(cwd, 'data/test/labels')

# Create folders if they don't already exist
for dir_path in [train_img_path, train_lbl_path,
                 val_img_path, val_lbl_path,
                 test_img_path, test_lbl_path]:
    os.makedirs(dir_path, exist_ok=True)

# Get list of all images
img_file_list = [path for path in Path(input_image_path).rglob('*') if path.suffix.lower() in [".jpg", ".png", ".jpeg"]]

print(f'Total images: {len(img_file_list)}')

# Shuffle for randomness
random.shuffle(img_file_list)

# Determine counts
file_num = len(img_file_list)
train_num = int(file_num * train_percent)
test_num = int(file_num * test_percent)
val_num = file_num - (train_num + test_num)

print(f'Images → train: {train_num}, val: {val_num}, test: {test_num}')

# Helper function to copy files
def copy_files(img_paths, new_img_path, new_lbl_path):
    for img_path in img_paths:
        img_fn = img_path.name
        base_fn = img_path.stem
        txt_fn = base_fn + '.txt'
        txt_path = os.path.join(input_label_path, txt_fn)

        shutil.copy(img_path, os.path.join(new_img_path, img_fn))
        if os.path.exists(txt_path):
            shutil.copy(txt_path, os.path.join(new_lbl_path, txt_fn))

# Split files
train_files = img_file_list[:train_num]
val_files = img_file_list[train_num:train_num + val_num]
test_files = img_file_list[train_num + val_num:]

copy_files(train_files, train_img_path, train_lbl_path)
copy_files(val_files, val_img_path, val_lbl_path)
copy_files(test_files, test_img_path, test_lbl_path)

print("✅ Dataset split complete!")
