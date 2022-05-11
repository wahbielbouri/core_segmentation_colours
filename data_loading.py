import os
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from pydicom import dcmread
from pydicom.data import get_testdata_file

from formatting import Formatter

@dataclass
class pixelBuffer:
        buffer: list
        index: int = -1

        def __post_init__(self):
            self.buffer = []

        def add_data(self, pixel_item):
            self.buffer.append(pixel_item)

        def __iter__(self):
            return self

        def __next__(self):
            self.index += 1
            return self.buffer[self.index]

        def __len__(self):
            return len(self.buffer)


class dataLoader(Formatter):

    def __init__(self, dir, num_images):
        super().__init__()
        self.dir = dir
        self.num_images = num_images
        self.pixel_buffer = pixelBuffer(buffer=[])

    def load_in_images(self):

        file_list = os.listdir(self.dir)
        num_files_in_dir = len([filename for filename in file_list if os.path.isfile(os.path.join(self.dir,filename))])
        limit = self.num_images if self.num_images <= num_files_in_dir else num_files_in_dir

        img_count = 0
        for filename in file_list:
            ds = dcmread(os.path.join(self.dir, filename))
            self.pixel_buffer.add_data(ds.pixel_array)

            img_count+=1
            if img_count >= limit:
                break

    def format_images(self):
        self.pixel_buffer.buffer = np.vstack([self.format(array) for array in self.pixel_buffer.buffer])

    def train_test_split(self, split_ratio=0.7):
        train_x, test_x = train_test_split(self.pixel_buffer.buffer, train_size=split_ratio, shuffle=True)
        return train_x, test_x

if __name__ == "__main__":

    dir = r"C:/Users/rashe/Downloads/segmentation_test_data"
    dl = dataLoader(dir, 3)
    dataset = dl.load_in_images()
