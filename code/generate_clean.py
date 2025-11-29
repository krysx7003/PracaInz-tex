from PIL import Image, ImageDraw


class ImageGenerator:
    def text_to_img(self, output_path, text: str):
        output_path = output_path.replace(".txt", ".png")
        lines = text.split("\n")

        img = Image.new("RGB", (self.A4_WIDTH, self.A4_HEIGHT), color="white")
        draw = ImageDraw.Draw(img)

        y_position = self.margin

        for line in lines:
            if y_position + self.line_height < self.A4_HEIGHT - self.margin:
                draw.text((self.margin, y_position), line, fill="black", font=self.font)
                y_position += self.line_height

        img.save(output_path)
