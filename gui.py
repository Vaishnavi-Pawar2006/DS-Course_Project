# gui.py

import tkinter as tk
from tkinter import ttk, scrolledtext
from pathlib import Path

# Import the logic from your other files
from custom_queue import CustomQueue
from data_loader import load_packets_from_csv

class PacketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Packet Processor 📦")
        self.root.geometry("700x550")
        
        self.packet_queue = CustomQueue()
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        load_frame = ttk.Frame(main_frame)
        load_frame.pack(fill=tk.X, pady=5)
        
        self.load_button = ttk.Button(load_frame, text="Load Packets from CSV", command=self.load_packets)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(load_frame, text="Welcome! Click 'Load Packets' to start.")
        self.status_label.pack(side=tk.LEFT, padx=5)

        process_frame = ttk.Frame(main_frame)
        process_frame.pack(fill=tk.X, pady=5)

        self.process_button = ttk.Button(process_frame, text="Process Next Packet", command=self.process_next_packet)
        self.process_button.pack(side=tk.LEFT, padx=5)
        self.process_button.config(state=tk.DISABLED)

        self.queue_size_label = ttk.Label(process_frame, text="Packets in queue: 0")
        self.queue_size_label.pack(side=tk.LEFT, padx=5)

        log_label = ttk.Label(main_frame, text="Processing Log:")
        log_label.pack(fill=tk.X, pady=(10, 0))

        self.log_area = scrolledtext.ScrolledText(main_frame, height=20, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_area.config(state=tk.DISABLED)

    def load_packets(self):
        self.status_label.config(text="Loading...")
        
        script_dir = Path(__file__).resolve().parent
        csv_path = script_dir / "demo_features.csv"
        
        packets = load_packets_from_csv(csv_path, 300)
        
        if not packets:
            self.status_label.config(text="Failed to load packets. Check for demo_features.csv.")
            return
            
        for pkt in packets:
            self.packet_queue.enqueue(pkt)
            
        self.update_queue_size()
        self.status_label.config(text=f"Successfully loaded {len(self.packet_queue)} packets!")
        self.process_button.config(state=tk.NORMAL)
        self.load_button.config(state=tk.DISABLED)

    def process_next_packet(self):
        if self.packet_queue.is_empty():
            self.status_label.config(text="All packets have been processed! 🎉")
            self.process_button.config(state=tk.DISABLED)
            return

        packet = self.packet_queue.dequeue()
        
        info = (
            f"DEQUEUED PACKET:\n"
            f"  Source IP:      {packet.src_ip}\n"
            f"  Destination IP: {packet.dest_ip}\n"
            f"  Protocol:       {packet.protocol}\n"
            f"  Length:         {packet.length} bytes\n"
            f"----------------------------------------\n"
        )
        
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, info)
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
        
        self.update_queue_size()
        
    def update_queue_size(self):
        size = len(self.packet_queue)
        self.queue_size_label.config(text=f"Packets in queue: {size}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketApp(root)
    root.mainloop()