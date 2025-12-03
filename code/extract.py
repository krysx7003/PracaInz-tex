import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


class TextExtractor:
    def load_file(self, input_path: str):
        book = epub.read_epub(input_path)
        self.book_name = input_path.split("/")[-1]
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        chapter_items = []
        for item in items:
            if "part" in item.get_name().lower():
                chapter_items.append(item)

        return chapter_items

    def parse_file(self, chapter):
        soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
        target_elements = soup.find_all(
            ["h2", "div"], class_=lambda x: x != "stanza" and x != "stanza-spacer"
        )

        filtered_elements = []
        for element in target_elements:
            if element.name == "h2":
                filtered_elements.append(element)
            elif element.name == "div" and "verse" in element.get("class", []):
                filtered_elements.append(element)

        text_elements = []
        for element in filtered_elements:
            element_text = element.get_text().strip()
            if element_text:
                text_elements.append(element_text)

        text = "\n".join(text_elements)
        return text
