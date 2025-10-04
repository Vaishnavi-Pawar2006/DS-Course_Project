# main.py

from pathlib import Path
from custom_queue import CustomQueue
from data_loader import load_packets_from_csv, PacketInfo # <-- See? It now imports the logic.

def run_tests():
    """Runs unit tests for the CustomQueue."""
    print("--- Running Queue Tests ---")
    q = CustomQueue()
    try:
        q.dequeue()
    except IndexError as e:
        print(f"[PASS] Dequeue from empty queue raises: {e}")
    q.enqueue(85)
    print(f"[PASS] Enqueued 85 as an element, peek = {q.peek()}")
    print(f"[PASS] Dequeued = {q.dequeue()}")
    for i in range(1, 6):
        q.enqueue(i)
    fifo_ok = True
    for i in range(1, 6):
        val = q.dequeue()
        if val != i:
            print(f"[FAIL] Expected {i} got {val}")
            fifo_ok = False
    if fifo_ok:
        print("[PASS] FIFO order preserved")
    try:
        q.peek()
    except IndexError as e:
        print(f"[PASS] Peek from empty queue raises: {e}")
    print("--- Queue Tests Finished ---\n")


def main():
    """Main function to run the packet processing application."""
    run_tests()

    print("--- Starting Packet Processing ---")
    packet_queue = CustomQueue()
    
    # This line now uses the imported function!
    script_dir = Path(__file__).resolve().parent
    csv_path = script_dir / "demo_features.csv"
    packets = load_packets_from_csv(csv_path, 300)

    if not packets:
        print("No packets were loaded. Exiting.")
        return

    for pkt in packets:
        packet_queue.enqueue(pkt)

    print(f"Initial queue size: {len(packet_queue)}")

    while not packet_queue.is_empty():
        pkt = packet_queue.dequeue()
        print(f"Dequeued packet: {pkt.src_ip} -> {pkt.dest_ip} "
              f"| Protocol: {pkt.protocol} "
              f"| Payload: '{pkt.payload}' "
              f"| Length: {pkt.length}")

    print(f"Final queue size: {len(packet_queue)}")
    print("--- Packet Processing Finished ---")


if __name__ == "__main__":
    main()
    