"""
cli.py - Enhanced Command-Line Interface (Version 2)
Provides a clean, interactive UI, animated progress, and robust error handling.
"""

import sys
import time
from tanker_core import WaterTanker, VALID_DENOMINATIONS

# Ensure UTF-8 output handling on Windows consoles without crash
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def print_banner():
    """Prints a clean, styled banner."""
    print("\n" + "=" * 54)
    print("      [~] SWAPI WATER TANKER DISPENSER [~]       ")
    print("          Automated Pure Water Station           ")
    print("=" * 54)


def print_receipt(litres: int, remaining: int):
    """Prints a formatted transaction receipt."""
    print("\n" + "-" * 42)
    print("            RECEIPT / SUMMARY            ")
    print("-" * 42)
    print(f"  Water Dispensed : {litres} Litre(s)")
    print(f"  Total Amount    : Rs. {litres}")
    print(f"  Tank Remaining  : {remaining} Litres")
    print("-" * 42)
    print("  Thank you for choosing Swapi Water Tanker!")
    print("-" * 42 + "\n")


def render_progress_bar(current: int, total: int, bar_length: int = 24):
    """Renders a dynamic inline terminal progress bar."""
    fraction = current / total
    filled_len = int(round(bar_length * fraction))
    bar = "=" * filled_len + "-" * (bar_length - filled_len)
    percent = fraction * 100
    sys.stdout.write(f"\r  Dispensing: [{bar}] {current}/{total} L ({percent:5.1f}%)")
    sys.stdout.flush()


def dispense_water_cli(tanker: WaterTanker, amount: int, step_delay: float = 0.25):
    """Executes dispensing with an animated CLI progress bar."""
    print(f"\n[+] Starting dispensing of {amount} Litre(s)...")
    print("    Please place your container under the nozzle.")
    time.sleep(0.5)

    for current_litre, total_litres, _ in tanker.dispense_stream(amount, step_delay=step_delay):
        render_progress_bar(current_litre, total_litres)

    print("\n[OK] Dispensing complete!")
    print_receipt(amount, tanker.current_water)


def get_validated_amount(tanker: WaterTanker, allow_custom: bool = False) -> int:
    """
    Robust input loop that handles invalid integers, out-of-range values,
    and user cancellations without crashing.
    """
    valid_list_str = ", ".join(map(str, VALID_DENOMINATIONS))

    while True:
        try:
            if allow_custom:
                prompt_text = f"Enter amount in Litres (Available: {tanker.current_water}L, 'q' to cancel): "
            else:
                prompt_text = f"Enter standard amount [{valid_list_str}] (or 'q' to cancel): "

            user_input = input(prompt_text).strip()

            if user_input.lower() in ("q", "quit", "cancel", "exit"):
                return 0

            is_valid, amount, error_msg = tanker.validate_amount(user_input, allow_custom=allow_custom)
            if not is_valid:
                print(f"[!] Error: {error_msg}\n")
                continue

            return amount

        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            return 0


def display_tanker_status(tanker: WaterTanker):
    """Displays current storage status."""
    pct = (tanker.current_water / tanker.capacity) * 100
    print("\n" + "~" * 40)
    print("          TANKER STATUS MONITOR         ")
    print("~" * 40)
    print(f"  Capacity:         {tanker.capacity} Litres")
    print(f"  Current Level:    {tanker.current_water} Litres ({pct:.1f}%)")
    print(f"  Total Dispensed:  {tanker.total_dispensed} Litres")
    print(f"  Transactions:     {len(tanker.transaction_history)}")
    print("~" * 40 + "\n")


def run_interactive_cli(tanker: WaterTanker = None, default_delay: float = 0.25):
    """Main interactive terminal interface."""
    if tanker is None:
        tanker = WaterTanker()

    while True:
        print_banner()
        print("  1. Quick Dispense (Standard Coins: 1, 2, 5, 10, 15, 20)")
        print("  2. Custom Litre Dispense")
        print("  3. Check Tanker Level / Refill Tank")
        print("  4. Launch Desktop GUI (Window)")
        print("  5. Exit")
        print("-" * 54)

        try:
            choice = input("Select an option [1-5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if choice == "1":
            print(f"\nAccepted standard denominations: {VALID_DENOMINATIONS}")
            amount = get_validated_amount(tanker, allow_custom=False)
            if amount > 0:
                dispense_water_cli(tanker, amount, step_delay=default_delay)

        elif choice == "2":
            amount = get_validated_amount(tanker, allow_custom=True)
            if amount > 0:
                dispense_water_cli(tanker, amount, step_delay=default_delay)

        elif choice == "3":
            display_tanker_status(tanker)
            try:
                action = input("Refill tanker to 100%? (y/n): ").strip().lower()
                if action in ("y", "yes"):
                    added = tanker.refill()
                    print(f"[OK] Successfully refilled {added} Litres. Tank is now 100% full.")
            except (KeyboardInterrupt, EOFError):
                pass

        elif choice == "4":
            print("\n[+] Launching Desktop GUI...")
            try:
                import gui
                gui.launch_gui(tanker)
            except Exception as e:
                print(f"[!] Error launching GUI: {e}")

        elif choice in ("5", "q", "quit", "exit"):
            print("\nThank you for using Swapi Water Tanker. Goodbye!\n")
            break

        else:
            print("\n[!] Invalid selection. Please enter a number from 1 to 5.")

        time.sleep(0.3)


if __name__ == "__main__":
    run_interactive_cli()
