# Metro System
from Classes.Metro import MetroSystem
from data.seed import seed
import os
from Classes.User import load_users, save_users, create_user, get_user
import getpass

def _auth_flow() -> str:
    users = load_users()
    while True:
        print("\n" + "="*60)
        print("USER AUTHENTICATION")
        print("="*60)
        print("1. Sign In")
        print("2. Sign Up")
        print("3. Exit")
        print("="*60)
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice == "1":
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            user = get_user(users, username)
            if user and user.verify_password(password):
                print(f"\n✅ Signed in as {username}")
                return username
            print("\n❌ Invalid username or password.")
        elif choice == "2":
            username = input("Choose a username: ").strip()
            if not username:
                print("\n❌ Username cannot be empty.")
                continue
            if get_user(users, username):
                print("\n❌ Username already exists.")
                continue
            password = getpass.getpass("Choose a password: ")
            confirm = getpass.getpass("Confirm password: ")
            if not password:
                print("\n❌ Password cannot be empty.")
                continue
            if password != confirm:
                print("\n❌ Passwords do not match.")
                continue
            try:
                create_user(users, username, password)
                save_users(users)
                print("\n✅ Account created. You can now sign in.")
            except ValueError as e:
                print(f"\n❌ {e}")
        elif choice == "3":
            print("\n👋 Goodbye!")
            raise SystemExit(0)
        else:
            print("\n❌ Invalid choice. Please try again.")


def main():
    current_user = _auth_flow()
    metro = MetroSystem()
    # Create default metro if no data exists
    if not os.path.exists('stations.csv'):
        print("Creating default metro system...")
        seed(metro)
    
    while True:
        print("\n" + "="*60)
        print(f"METRO TICKET PURCHASING SYSTEM — Signed in as: {current_user}")
        print("="*60)
        print("1. View Stations")
        print("2. Purchase Ticket")
        print("3. View Purchased Tickets")
        print("4. Sign Out")
        print("5. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            metro.display_stations()
        
        elif choice == "2":
            origin = input("Enter origin station: ").strip()
            destination = input("Enter destination station: ").strip()
            
            if origin and destination:
                metro.purchase_ticket(origin, destination, username=current_user)
            else:
                print("\n❌ Please enter both origin and destination")
        
        elif choice == "3":
            metro.view_tickets(username=current_user)
        
        elif choice == "4":
            print("\n🔒 Signing out...")
            current_user = _auth_flow()
        
        elif choice == "5":
            print("\n👋 Thank you for using Metro System!")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

