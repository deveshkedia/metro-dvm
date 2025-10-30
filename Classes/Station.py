class Station:
    def __init__(self, name, lines):
        self.name = name
        self.lines = set(lines)  # A station can be on multiple lines
        self.connections = []  # List of adjacent stations
        
    def add_connection(self, station):
        if station not in self.connections:
            self.connections.append(station)
    
    def __repr__(self):
        return f"Station({self.name}, {self.lines})"