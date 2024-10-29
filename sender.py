import customtkinter as ctk
from pythonosc import udp_client
import threading
import random
import time

# Convert data types for OSC message arguments
def convert_message(message):
    message = message.strip()
    if message.lower() in ["true", "yes"]: return True
    if message.lower() in ["false", "no"]: return False
    for convert in (int, float):
        try: return convert(message)
        except ValueError: pass
    return message

# Generate a random message
def generate_random_message():
    return str(random.randint(0, 100))

# GUI Application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OSC Message Sender")
        self.geometry("500x600")

        self.ip_entry, self.port_entry = self.create_entry("IP Address:", "127.0.0.1"), self.create_entry("Port:", "5006")
        self.address_entry, self.message_entry = self.create_entry("Address:", "/test"), self.create_entry("Message:", "Hello")

        ctk.CTkButton(self, text="Send Message", command=self.send_message).pack(pady=20)
        self.message_text = ctk.CTkTextbox(self, height=20, width=60, font=("Courier", 12), bg_color="#2b2b2b", text_color="#d6d6d6")
        self.message_text.pack(pady=10, padx=20, fill="both", expand=True)

        self.sending_random = False
        self.toggle_button = ctk.CTkButton(self, text="Start Sending Random Integers", command=self.toggle_random_messages)
        self.toggle_button.pack(pady=20)

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
        self.message_text.see("end")

    def toggle_random_messages(self):
        if self.sending_random:
            self.sending_random = False
            self.toggle_button.configure(text="Start Sending Random Integers")
        else:
            self.sending_random = True
            self.toggle_button.configure(text="Stop Sending Random Integers")
            threading.Thread(target=self.send_random_messages).start()

    def send_random_messages(self):
        while self.sending_random:
            random_message = generate_random_message()
            self.message_entry.delete(0, "end")
            self.message_entry.insert(0, random_message)
            self.send_message()
            time.sleep(2)  # Send a message every 2 seconds

# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
