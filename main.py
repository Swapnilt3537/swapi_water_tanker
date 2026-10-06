"""
main.py - Main Entry Point for Swapi Water Tanker
Supports:
  1. Enhanced Interactive CLI (Version 2) with input error handling & clean UI
  2. Modern Desktop GUI (Tkinter) with visual water tank animations
  3. Original Basic Version (Version 1) for historical reference
"""

import sys
import time
from tanker_core import WaterTanker, VALID_DENOMINATIONS
from cli import run_interactive_cli, dispense_water_cli, print_banner

# Ensure UTF-8 output handling on Windows consoles without crash
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_basic_version():
    """
    Version 1: The original basic script with straightforward error handling.
    """
    print("\n--- Running Basic Version (Version 1) ---")
    try:
        amount = int(input("Enter the amount: "))
        if amount in VALID_DENOMINATIONS:
            print("\nWelcome to Swapi Water Tanker\n")
            print(f"You entered: {amount}")
            for litre in range(1, amount + 1):
                time.sleep(1)  # 1s per litre for practical demonstration
                print(f"{litre} litre")
            print("\nThanks for visiting Swapi Water Tanker!\n")
        else:
            print(f"\nInvalid amount! Amount should be {VALID_DENOMINATIONS}\n")
    except ValueError:
        print("\nInvalid input! Please enter an integer amount.\n")


def run_launcher():
    """Interactive launcher menu for selecting the desired mode."""
    tanker = WaterTanker()

    while True:
        print_banner()
        print("  Select Mode to Run:")
        print("  [1] Enhanced Interactive CLI (Version 2)")
        print("  [2] Desktop Graphical UI (Tkinter GUI)")
        print("  [3] Original Basic Script (Version 1)")
        print("  [4] Run Unit Tests")
        print("  [5] Exit")
        print("=" * 54)

        try:
            choice = input("Enter your choice [1-5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

        if choice == "1":
            run_interactive_cli(tanker)
        elif choice == "2":
            print("\n[+] Launching Graphical Desktop GUI...")
            from gui import launch_gui
            launch_gui(tanker)
        elif choice == "3":
            run_basic_version()
        elif choice == "4":
            import subprocess
            subprocess.run([sys.executable, "test_tanker.py"])
        elif choice in ("5", "q", "exit"):
            print("\nThank you for using Swapi Water Tanker! Goodbye.\n")
            break
        else:
            print("\n[!] Invalid choice. Please choose 1, 2, 3, 4, or 5.")


def main():
    if "--gui" in sys.argv:
        from gui import launch_gui
        launch_gui()
    elif "--cli" in sys.argv:
        run_interactive_cli()
    elif "--basic" in sys.argv:
        run_basic_version()
    else:
        run_launcher()


if __name__ == "__main__":
    main()
