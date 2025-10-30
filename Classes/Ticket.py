import uuid

class Ticket:
    def __init__(self, origin, destination, path, price, username=None):
        self.ticket_id = str(uuid.uuid4())[:8]
        self.origin = origin
        self.destination = destination
        self.path = path
        self.price = price
        self.username = username
        self.instructions = []
        self._generate_instructions()
    
    def _generate_instructions(self):
        """Generate travel instructions including line changes"""
        if not self.path:
            return
        
        # Determine the current line
        current_line = list(self.path[0].lines)[0]
        self.instructions.append(f"Start at {self.path[0].name}")
        
        for i in range(1, len(self.path)):
            station = self.path[i]
            prev_station = self.path[i - 1]
            
            # Check if there's a line change
            prev_lines = prev_station.lines
            current_lines = station.lines
            
            # Find common line, or use the first available line
            common_lines = prev_lines.intersection(current_lines)
            
            if common_lines:
                current_line = list(common_lines)[0]
            elif len(current_lines) == 1:
                new_line = list(current_lines)[0]
                if new_line != current_line:
                    self.instructions.append(f"At {prev_station.name}, transfer to {new_line} line")
                    current_line = new_line
            else:
                # Transfer station
                self.instructions.append(f"At {prev_station.name}, change lines")
            
            if i == len(self.path) - 1:
                self.instructions.append(f"Arrive at {station.name}")
            else:
                self.instructions.append(f"Go to {station.name}")
    
    def display(self):
        print(f"\n{'='*60}")
        print(f"Ticket ID: {self.ticket_id}")
        print(f"Route: {self.origin} → {self.destination}")
        print(f"Price: ₹{self.price:.0f}")
        if self.username:
            print(f"User: {self.username}")
        stations_crossed = max(len(self.path) - 1, 0)
        print(f"Stations: {stations_crossed} stations")
        print(f"\nTravel Instructions:")
        for i, instruction in enumerate(self.instructions, 1):
            print(f"  {i}. {instruction}")
        print(f"{'='*60}\n")
    
    def to_dict(self):
        path_str = " -> ".join([s.name for s in self.path]) if self.path else ""
        return {
            'ticket_id': self.ticket_id,
            'origin': self.origin,
            'destination': self.destination,
            'path': path_str,
            'price': self.price,
            'username': self.username or ''
        }