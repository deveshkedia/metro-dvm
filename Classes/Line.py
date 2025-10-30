class Line:
    def __init__(self, line_id, color):
        self.line_id = line_id
        self.color = color
        self.stations = []
        self.line_count = 0
    
    def add_station(self, station):
        if station not in self.stations:
            self.stations.append(station)
            self.line_count += 1
            
    def get_adjacent_stations(self, station):
        """Get adjacent stations on the same line"""
        idx = self.stations.index(station)
        adjacent = []
        if idx > 0:
            adjacent.append(self.stations[idx - 1])
        if idx < len(self.stations) - 1:
            adjacent.append(self.stations[idx + 1])
        return adjacent