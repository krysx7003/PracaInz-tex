import os

import cv2
import numpy as np
from noise import pnoise2


class ImageGenerator:
    def wrinkle_img(self, input_dir: str, file_name: str):
        scale = 500.0
        octaves = 3
        persistence = 0.5
        lacunarity = 2.0

        os.makedirs(self.WRINKLE_DIR, exist_ok=True)

        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(self.WRINKLE_DIR, file_name)

        wrinkles = np.zeros((self.A4_HEIGHT, self.A4_WIDTH))

        for i in range(self.A4_HEIGHT):
            for j in range(self.A4_WIDTH):
                wrinkles[i][j] = pnoise2(
                    i / scale,
                    j / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=self.A4_WIDTH,
                    repeaty=self.A4_HEIGHT,
                    base=self.seed,
                )

        normalized_wrinkles = (wrinkles - wrinkles.min()) / (
            wrinkles.max() - wrinkles.min()
        )

        original_image = cv2.imread(input_path)

        scale_intensity = 50
        disp_x = (normalized_wrinkles - 0.5) * scale_intensity
        disp_y = (normalized_wrinkles - 0.5) * scale_intensity

        x, y = np.meshgrid(np.arange(self.A4_WIDTH), np.arange(self.A4_HEIGHT))

        map_x = (x + disp_x).astype(np.float32)
        map_y = (y + disp_y).astype(np.float32)

        wrinkled_image = cv2.remap(original_image, map_x, map_y, cv2.INTER_LINEAR)
        cv2.imwrite(output_path, wrinkled_image)
