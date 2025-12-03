import os
import random

import cv2
import numpy as np


class ImageGenerator:
    def tilt_img(self, input_dir: str, file_name: str):
        os.makedirs(self.TILT_DIR, exist_ok=True)
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(self.TILT_DIR, file_name)

        original_image = cv2.imread(input_path)
        height, width = original_image.shape[:2]
        src_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

        random.seed(self.seed)
        tilt_tl: float = random.uniform(0.01, 0.2)
        tilt_tr: float = random.uniform(0.01, 0.2)
        tilt_bl: float = random.uniform(0.01, 0.2)
        tilt_br: float = random.uniform(0.01, 0.2)
        dst_points = np.float32(
            [
                [width * tilt_tl, 0],
                [width * (1 - tilt_tr), 0],
                [0, height * (1 - tilt_bl)],
                [width * (1 - tilt_br), height * (1 - tilt_br)],
            ]
        )

        matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        tilted_image = cv2.warpPerspective(original_image, matrix, (width, height))
        cv2.imwrite(output_path, tilted_image)
