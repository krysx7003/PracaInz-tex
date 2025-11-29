import os

import cv2
import numpy as np
from noise import pnoise2


class ImageGenerator:
    def shadow_img(self, input_dir: str, file_name: str):
        scale = 1000.0
        octaves = 2
        persistence = 5.0
        lacunarity = 0.5

        os.makedirs(self.SHADOW_DIR, exist_ok=True)

        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(self.SHADOW_DIR, file_name)

        shadow = np.zeros((self.A4_HEIGHT, self.A4_WIDTH))

        for i in range(self.A4_HEIGHT):
            for j in range(self.A4_WIDTH):
                shadow[i][j] = pnoise2(
                    i / scale,
                    j / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=self.A4_WIDTH,
                    repeaty=self.A4_HEIGHT,
                    base=self.seed,
                )

        normalized_shadow = (shadow - shadow.min()) / (shadow.max() - shadow.min())

        shadow_dark = normalized_shadow * 0.9

        original_image = cv2.imread(input_path)

        shadow_rgb = cv2.cvtColor(shadow_dark.astype(np.float32), cv2.COLOR_GRAY2BGR)
        image_with_shadow = original_image.astype(np.float32) * shadow_rgb
        image_with_shadow = np.clip(image_with_shadow, 0, 255).astype(np.uint8)

        cv2.imwrite(output_path, image_with_shadow)
