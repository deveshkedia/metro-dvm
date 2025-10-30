import os
import csv
from collections import defaultdict, deque
from .Station import Station
from .Line import Line
from .Ticket import Ticket

class MetroSystem:
    def __init__(self):
        self.lines = {}
        self.stations = {}  # name -> Station
        self.tickets = []
        self.load_from_csv()
    
    def add_line(self, line):
        self.lines[line.line_id] = line
        for station in line.stations:
            if station.name not in self.stations:
                self.stations[station.name] = station
            else:
                # If station already exists (transfer station), add the line
                self.stations[station.name].lines.add(line.line_id)
    
    def load_from_csv(self):
        """Load stations and lines from CSV files"""
        # Load stations with their lines
        if os.path.exists('stations.csv'):
            station_lines_map = defaultdict(list)
            with open('stations.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    station_lines_map[row['name']].append(row['line_id'])
            
            for name, lines in station_lines_map.items():
                station = Station(name, lines)
                self.stations[name] = station
        
        # Load lines
        if os.path.exists('lines.csv'):
            with open('lines.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    line = Line(row['line_id'], row['color'])
                    # Add stations to line
                    if row['line_id'] in station_lines_map or True:
                        for name, station in self.stations.items():
                            if row['line_id'] in station.lines:
                                line.add_station(station)
                    self.lines[row['line_id']] = line
        
        # Load connections
        if os.path.exists('connections.csv'):
            with open('connections.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    station1 = self.stations.get(row['station1'])
                    station2 = self.stations.get(row['station2'])
                    if station1 and station2:
                        station1.add_connection(station2)
                        station2.add_connection(station1)
        
        # Load tickets (after graph is ready so we can rebuild paths)
        if os.path.exists('tickets.csv'):
            with open('tickets.csv', 'r') as f:
                try:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if not row:
                            continue
                        origin = row.get('origin')
                        destination = row.get('destination')
                        username = row.get('username') or None
                        # Rebuild path using current network (ensures Station objects)
                        path = self.find_shortest_path(origin, destination) if origin and destination else None
                        try:
                            price = float(row.get('price', '0') or 0)
                        except ValueError:
                            price = 0.0
                        ticket = Ticket(origin, destination, path or [], price, username=username)
                        self.tickets.append(ticket)
                except csv.Error:
                    # If file is empty or malformed, skip loading
                    pass
    
    def save_to_csv(self):
        """Save all data to CSV files"""
        # Save stations
        with open('stations.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'line_id'])
            for station in self.stations.values():
                for line_id in station.lines:
                    writer.writerow([station.name, line_id])
        
        # Save lines
        with open('lines.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['line_id', 'color'])
            for line in self.lines.values():
                writer.writerow([line.line_id, line.color])
        
        # Save connections
        with open('connections.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['station1', 'station2'])
            written = set()
            for station in self.stations.values():
                for conn in station.connections:
                    pair = tuple(sorted([station.name, conn.name]))
                    if pair not in written:
                        writer.writerow(list(pair))
                        written.add(pair)
        
        # Save tickets
        with open('tickets.csv', 'w', newline='') as f:
            if self.tickets:
                writer = csv.DictWriter(f, fieldnames=self.tickets[0].to_dict().keys())
                writer.writeheader()
                for ticket in self.tickets:
                    writer.writerow(ticket.to_dict())
    
    def find_shortest_path(self, origin_name, destination_name):
        """Find shortest path using BFS"""
        if origin_name not in self.stations or destination_name not in self.stations:
            return None
        
        origin = self.stations[origin_name]
        destination = self.stations[destination_name]
        
        queue = deque([(origin, [origin])])
        visited = {origin}
        
        while queue:
            current, path = queue.popleft()
            
            if current == destination:
                return path
            
            for neighbor in current.connections:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def calculate_price(self, path):
        """Calculate ticket price based on number of stations (INR)"""
        if len(path) <= 1:
            return 10.0  # Base fare ₹10
        stations_crossed = len(path) - 1
        # Price: ₹10 base + ₹5 per station
        return 10.0 + (stations_crossed * 5.0)
    
    def purchase_ticket(self, origin, destination, username=None):
        """Purchase a ticket for the given route"""
        path = self.find_shortest_path(origin, destination)
        
        if not path:
            print(f"\n❌ No route found from {origin} to {destination}")
            return None
        
        price = self.calculate_price(path)
        ticket = Ticket(origin, destination, path, price, username=username)
        self.tickets.append(ticket)
        self.save_to_csv()
        
        print(f"\n✅ Ticket purchased successfully!")
        ticket.display()
        return ticket
    
    def display_stations(self):
        """Display all stations grouped by line"""
        print("\n" + "="*60)
        print("METRO STATIONS")
        print("="*60)
        
        for line_id, line in self.lines.items():
            print(f"\n{line.color.upper()} LINE ({line_id}):")
            print("-" * 40)
            for i, station in enumerate(line.stations, 1):
                transfer_marker = " [TRANSFER]" if len(station.lines) > 1 else ""
                print(f"  {i}. {station.name}{transfer_marker}")
        
        print("\n" + "="*60 + "\n")
    
    def view_tickets(self, username: str = None):
        """Display purchased tickets, optionally filtered by username"""
        filtered = self.tickets
        if username:
            filtered = [t for t in self.tickets if (t.username or '') == username]
        if not filtered:
            print("\n❌ No tickets purchased yet." if not username else f"\n❌ No tickets found for user: {username}.")
            return
        
        print("\n" + "="*60)
        print("PURCHASED TICKETS" + (" — " + username if username else ""))
        print("="*60)
        
        for ticket in filtered:
            ticket.display()
    
