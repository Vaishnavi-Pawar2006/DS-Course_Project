# data_loader.py

import csv
from pathlib import Path
from dataclasses import dataclass

@dataclass
class PacketInfo:
    """Stores information about a single network packet."""
    src_ip: str
    dest_ip: str
    protocol: str
    payload: str
    length: int

def load_packets_from_csv(filename: Path, limit: int = 1000) -> list[PacketInfo]:
    """Loads packet data from a CSV file with robust error handling."""
    packets = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            try:
                next(reader)
            except StopIteration:
                return []
            for row in reader:
                if len(packets) >= limit:
                    break
                if len(row) != 9:
                    continue
                try:
                    (_, src_ip, dest_ip, protocol, _, _, length_str, payload, _) = row
                    if payload == "NaN":
                        payload = ""
                    packets.append(PacketInfo(
                        src_ip=src_ip, dest_ip=dest_ip, protocol=protocol,
                        payload=payload, length=int(length_str)
                    ))
                except ValueError:
                    continue
    except FileNotFoundError:
        print(f"Error: Unable to open file at '{filename}'.")
    return packets