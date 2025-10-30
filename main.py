# Metro System
import csv
import uuid
import os
from collections import defaultdict, deque
from typing import List, Tuple, Optional
from Classes.Metro import MetroSystem
from Classes.Station import Station
from Classes.Line import Line
from Classes.Ticket import Ticket

def main():
    metro = MetroSystem()
    # Create default metro if no data exists
    if not os.path.exists('stations.csv'):
        print("Creating default metro system...")
        metro.create_default_metro()
    
    while True:
        print("\n" + "="*60)
        print("METRO TICKET PURCHASING SYSTEM")
        print("="*60)
        print("1. View Stations")
        print("2. Purchase Ticket")
        print("3. View Purchased Tickets")
        print("4. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            metro.display_stations()
        
        elif choice == "2":
            origin = input("Enter origin station: ").strip()
            destination = input("Enter destination station: ").strip()
            
            if origin and destination:
                metro.purchase_ticket(origin, destination)
            else:
                print("\n❌ Please enter both origin and destination")
        
        elif choice == "3":
            metro.view_tickets()
        
        elif choice == "4":
            print("\n👋 Thank you for using Metro System!")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

