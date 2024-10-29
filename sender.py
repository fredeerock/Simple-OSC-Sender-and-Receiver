import customtkinter as ctk
from pythonosc import udp_client

# Convert data types for OSC message arguments
def convert_message(message):
    message = message.strip()
    if message.lower() in ["true", "1", "yes"]: return True
    if message.lower() in ["false", "0", "no"]: return False
    for convert in (int, float):
        try: return convert(message)
        except ValueError: pass
    return message

# GUI Application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OSC Message Sender")
        self.geometry("500x600")

        self.ip_entry, self.port_entry = self.create_entry("IP Address:", "127.0.0.1"), self.create_entry("Port:", "5006")
        self.address_entry, self.message_entry = self.create_entry("OSC Address Pattern:", "/test"), self.create_entry("Message:", "Hello")

        ctk.CTkButton(self, text="Send Message", command=self.send_message).pack(pady=20)
        self.message_text = ctk.CTkTextbox(self, height=20, width=60, font=("Courier", 12), bg_color="#2b2b2b", text_color="#d6d6d6")
        self.message_text.pack(pady=10, padx=20, fill="both", expand=True)

    def create_entry(self, label_text, default_text):
        ctk.CTkLabel(self, text=label_text).pack(pady=5)
        entry = ctk.CTkEntry(self)
        entry.insert(0, default_text)
        entry.pack(pady=5)
        return entry

    def send_message(self):
        ip, port = self.ip_entry.get(), int(self.port_entry.get())
        client, args = udp_client.SimpleUDPClient(ip, port), [convert_message(arg) for arg in self.message_entry.get().split(",")]

        client.send_message(self.address_entry.get(), args)
        self.update_sent_message(f"SENT: IP[{ip}:{port}] ADDRESS[{self.address_entry.get()}] ARGS{args}")

    def update_sent_message(self, message):
        self.message_text.insert("end", message + "\n")
        for word, color in [("SENT", "green"), ("IP", "cyan"), ("ADDRESS", "cyan"), ("ARGS", "cyan")]:
            self.highlight_text(word, color)
        self.message_text.see("end")

    def highlight_text(self, word, color):
        start = self.message_text.search(word, "1.0", "end")
        while start:
            end = f"{start}+{len(word)}c"
            self.message_text.tag_config(word, foreground=color)
            self.message_text.tag_add(word, start, end)
            start = self.message_text.search(word, end, "end")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
