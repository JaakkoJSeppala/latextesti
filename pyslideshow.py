import tkinter as tk

# Testidatasetti: diat ja niiden vaiheet
slides = [
    ["Tervetuloa esitykseen!", "Tämä esitys käyttää Computer Modern -fonttia.", "Aloitetaan!"],
    ["Ensimmäinen aihe", "Tässä on vähän lisää tekstiä.", "Ja vielä yksi vaihe tässä diassa."],
    ["Viimeinen dia", "Kiitos osallistumisesta!", "Nähdään seuraavassa esityksessä!"]
]

space = "<space>"

class PresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vaiheistettu esitys")
        self.root.geometry("800x600")
        self.root.configure(background="white")

        # Fontin rekisteröinti
        self.root.tk.call("font", "create", "ComputerModern", "-family", "CMU Serif", "-size", 16, "-weight", "normal")
        self.custom_font = "ComputerModern"

        # Esityksen tila
        self.current_slide = 0
        self.current_step = 0

        # Teksti-widget, johon sisältöä päivitetään
        self.text_label = tk.Label(root, text="", font=self.custom_font, background="white", wraplength=750, justify="left")
        self.text_label.pack(pady=50)

        # Ohjeet
        self.instruction_label = tk.Label(root, text="Paina välilyöntiä siirtyäksesi seuraavaan vaiheeseen.", 
                                          font=self.custom_font, background="white", fg="gray")
        self.instruction_label.pack(side="bottom", pady=20)

        # Bindataan välilyönti
        self.root.bind(space, self.next_step)

        # Näytetään ensimmäinen vaihe
        self.show_step()

    def show_step(self):
        """Näyttää nykyisen dian nykyisen vaiheen."""
        if self.current_slide < len(slides):
            current_steps = slides[self.current_slide]
            if self.current_step < len(current_steps):
                self.text_label.config(text=current_steps[self.current_step])
            else:
                # Siirry seuraavaan diaan, kun nykyinen on käyty läpi
                self.current_slide += 1
                self.current_step = 0
                self.show_step()
        else:
            # Esitys päättyy
            self.text_label.config(text="Esitys päättyi. Kiitos osallistumisesta!")
            self.root.unbind(space)  # Poistetaan välilyönnin toiminnallisuus

    def next_step(self, event=None):
        """Siirtyy seuraavaan vaiheeseen."""
        self.current_step += 1
        self.show_step()

def main():
    root = tk.Tk()
    app = PresentationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
