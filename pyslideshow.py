from tkinter import Tk, Canvas
from PIL import Image, ImageDraw, ImageFont, ImageTk
import matplotlib.pyplot as plt
import re
import io


def render_text_with_latex(text, font_path, font_size=20):
    """
    Renderöi tekstiä ja LaTeX-kaavoja yhdistelmänä kuvaan, jolloin kaavat näkyvät oikeassa kohdassa tekstin sisällä.
    
    :param text: Syöteteksti, jossa LaTeX-kaavat merkitty $...$.
    :param font_path: Polku TrueType-fonttitiedostoon.
    :param font_size: Fonttikoko tavalliselle tekstille.
    :return: Pillow Image -objekti.
    """
    custom_font = ImageFont.truetype(font_path, font_size)
    parts = re.split(r"(\$.*?\$)", text)
    rendered_parts = []

    for part in parts:
        if part.startswith("$") and part.endswith("$"):
            fig, ax = plt.subplots(dpi=100)
            ax.text(0.5, 0.5, part, fontsize=font_size, ha="center", va="center")
            ax.axis("off")
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", transparent=True)
            buf.seek(0)
            plt.close(fig)
            rendered_parts.append(Image.open(buf))
        else:
            temp_img = Image.new("RGBA", (800, font_size + 10), (255, 255, 255, 0))
            draw = ImageDraw.Draw(temp_img)
            text_bbox = draw.textbbox((0, 0), part, font=custom_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            draw.text((0, 0), part, font=custom_font, fill="black")
            rendered_parts.append(temp_img.crop((0, 0, text_width, text_height)))

    total_width = sum(img.width for img in rendered_parts)
    max_height = max(img.height for img in rendered_parts)
    combined_image = Image.new("RGBA", (total_width, max_height), "white")

    x_offset = 0
    for img in rendered_parts:
        combined_image.paste(img, (x_offset, (max_height - img.height) // 2), img)
        x_offset += img.width

    return combined_image


class SlideshowApp:
    def __init__(self, root, slides, font_path):
        """
        Alustaa slideshow-ohjelman.

        :param root: Tkinter-juuri-ikkuna.
        :param slides: Lista diojen teksteistä.
        :param font_path: Polku TrueType-fonttitiedostoon.
        """
        self.root = root
        self.slides = slides
        self.current_slide = 0
        self.font_path = font_path

        self.canvas = Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.update_slide()

        root.bind("<Left>", self.prev_slide)
        root.bind("<Right>", self.next_slide)

    def update_slide(self):
        """
        Päivittää dian sisällön.
        """
        self.canvas.delete("all")
        current_text = self.slides[self.current_slide]
        slide_image = render_text_with_latex(current_text, self.font_path)
        self.tk_image = ImageTk.PhotoImage(slide_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def prev_slide(self, event=None):
        """
        Siirtyy edelliseen diaan.
        """
        if self.current_slide > 0:
            self.current_slide -= 1
            self.update_slide()

    def next_slide(self, event=None):
        """
        Siirtyy seuraavaan diaan.
        """
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.update_slide()


if __name__ == "__main__":
    # Luo Tkinter-ikkuna
    root = Tk()
    root.title("Slideshow-opetusohjelma")

    # Määritä diat
    slides = [
        "Tervetuloa esitykseen! Tämä on ensimmäinen dia.\nKaava: $E = mc^2$",
        "Pythagoraan lause:\n$a^2 + b^2 = c^2$\n\nTodistus:\n1. Piirrä kolmio.\n2. Näytä neliöiden pinta-alat.",
        "Kolmas dia: Kiitos! Tämä oli esitys.\nToinen kaava: $\\int_0^1 x^2 \\, dx = \\frac{1}{3}$",
    ]

    # Polku fonttitiedostoon
    font_path = "/home/jaakko/Lataukset/Serif/cmunorm.ttf"

    # Käynnistä slideshow
    app = SlideshowApp(root, slides, font_path)
    root.mainloop()
