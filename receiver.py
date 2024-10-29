import threading
import customtkinter as ctk
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

# Handle incoming OSC messages
def message_handler(address, *args):
    # Convert the list of arguments to a string with single quotes around strings
    args_str = ", ".join(f"'{arg}'" if isinstance(arg, str) else str(arg) for arg in args)
    message = f"RECEIVED: ADDRESS[{address}] ARGS[{args_str}]"
    app.update_received_message(message)

# GUI Application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OSC Message Receiver")
        self.geometry("500x500")

        # Add a label for the port entry
        self.port_label = ctk.CTkLabel(self, text="Port:")
        self.port_label.pack(pady=5)
        
        self.port_entry = ctk.CTkEntry(self)
        self.port_entry.insert(0, "5006")
        self.port_entry.pack(pady=5)

        ctk.CTkButton(self, text="Start Server", command=self.start_server).pack(pady=20)
        self.message_text = ctk.CTkTextbox(self, height=20, width=60, font=("Courier", 12))
        self.message_text.pack(pady=10, padx=20, fill="both", expand=True)

        # Configure tags for colored text
        self.message_text.tag_config("green", foreground="green")
        self.message_text.tag_config("cyan", foreground="cyan")

        self.server = None
        self.start_server()

    def start_server(self):
        port = int(self.port_entry.get())
        self.shutdown_server()
        server_thread = threading.Thread(target=self.run_server, args=(port,))
        server_thread.daemon = True
        server_thread.start()

    def shutdown_server(self):
        if self.server:
            self.update_status_message("Shutting down existing server...")
            self.server.shutdown()
            self.server.server_close()
            self.server = None

    def update_received_message(self, message):
        self.message_text.insert("end", message + "\n")
        self.message_text.see("end")
        # Apply green color to the word "RECEIVED"
        start_index = self.message_text.search("RECEIVED", "1.0", "end")
        if start_index:
            end_index = f"{start_index}+8c"
            self.message_text.tag_add("green", start_index, end_index)
        # Apply cyan color to the words "ADDRESS" and "ARGS"
        for word in ["ADDRESS", "ARGS"]:
            start_index = self.message_text.search(word, "1.0", "end")
            while start_index:
                end_index = f"{start_index}+{len(word)}c"
                self.message_text.tag_add("cyan", start_index, end_index)
                start_index = self.message_text.search(word, end_index, "end")

    def update_status_message(self, message):
        self.message_text.insert("end", message + "\n")
        self.message_text.see("end")

    def run_server(self, port):
        # Set up the dispatcher and map OSC addresses to handler functions
        disp = Dispatcher()
        disp.map("/*", message_handler)  # Catch all OSC addresses

        # Create and start the UDP server
        server_address = "127.0.0.1"
        self.server = ThreadingOSCUDPServer((server_address, port), disp)
        self.update_status_message(f"Serving on {self.server.server_address}")
        self.server.serve_forever()

# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
