# Metro Ticket Purchasing System

A command-line application for purchasing metro tickets with multi-line support, path finding, and transfer station handling.

## Features

- 🚇 **Multi-line Metro System**: Support for multiple metro lines with transfer stations
- 🎫 **Ticket Purchasing**: Buy tickets with unique ID generation
- 🗺️ **Shortest Path Finding**: Automatic route calculation using BFS algorithm
- 🔄 **Transfer Instructions**: Detailed step-by-step travel instructions including line changes
- 💰 **Dynamic Pricing**: Ticket price based on number of stations traveled
- 💾 **CSV Storage**: Persistent data storage for stations, lines, connections, and tickets
- 🎯 **Object-Oriented Design**: Clean OOP architecture with proper encapsulation

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Ensure Python 3.7+ is installed
3. No additional packages required

## Usage

### Running the Application

```bash
python main.py
```

### Menu Options

1. **View Stations**: Display all stations organized by line (transfer stations are marked)
2. **Purchase Ticket**: Buy a ticket between two stations
3. **View Purchased Tickets**: Display all previously purchased tickets
4. **Exit**: Close the application

### Example Usage

```
METRO TICKET PURCHASING SYSTEM
============================================================
1. View Stations
2. Purchase Ticket
3. View Purchased Tickets
4. Exit
============================================================

Enter your choice (1-4): 1
```

View stations to see available destinations:

```
METRO STATIONS
============================================================

RED LINE (Red):
----------------------------------------
  1. Central
  2. Park [TRANSFER]
  3. Museum [TRANSFER]
  4. Station Square

BLUE LINE (Blue):
----------------------------------------
  1. Airport
  2. Downtown
  3. Museum [TRANSFER]
  4. Port

GREEN LINE (Green):
----------------------------------------
  1. University
  2. Library
  3. Park [TRANSFER]
  4. Stadium
```

Purchase a ticket:

```
Enter your choice (1-4): 2
Enter origin station: Airport
Enter destination station: University

✅ Ticket purchased successfully!

============================================================
Ticket ID: a1b2c3d4
Route: Airport → University
Price: $5.50
Stations: 7 stations

Travel Instructions:
  1. Start at Airport
  2. Go to Downtown
  3. Go to Museum
  4. At Museum, transfer to Red line
  5. Go to Park
  6. At Park, transfer to Green line
  7. Go to Library
  8. Arrive at University
============================================================
```

## System Architecture

### Classes

#### `Station`
Represents a metro station that can belong to multiple lines (transfer stations).

**Attributes:**
- `name`: Station name
- `lines`: Set of line IDs this station belongs to
- `connections`: List of connected stations

#### `Line`
Represents a metro line with a color.

**Attributes:**
- `line_id`: Unique line identifier
- `color`: Line color
- `stations`: List of stations on this line

#### `Ticket`
Represents a purchased ticket with travel instructions.

**Attributes:**
- `ticket_id`: Unique ticket ID (UUID)
- `origin`: Origin station
- `destination`: Destination station
- `path`: List of stations in the route
- `price`: Ticket price
- `instructions`: Step-by-step travel instructions

#### `MetroSystem`
Main system class managing the metro network.

**Methods:**
- `add_line()`: Add a metro line
- `find_shortest_path()`: Calculate shortest route using BFS
- `purchase_ticket()`: Purchase a ticket for a route
- `display_stations()`: Show all stations
- `view_tickets()`: Display purchased tickets
- `save_to_csv()` / `load_from_csv()`: Data persistence

## CSV Data Storage

The system uses four CSV files for data persistence:

1. **stations.csv**: Station names and their line associations
2. **lines.csv**: Line IDs and colors
3. **connections.csv**: Station connections (graph edges)
4. **tickets.csv**: Purchase history

## Default Metro Map

The system comes with a default 3-line metro network:

### Red Line
- Central → Park → Museum → Station Square

### Blue Line
- Airport → Downtown → Museum → Port

### Green Line
- University → Library → Park → Stadium

### Transfer Stations
- **Museum**: Red ↔ Blue
- **Park**: Red ↔ Green

## Pricing

- Base fare: $2.00
- Per station: $0.50
- Formula: `Price = $2.00 + (stations × $0.50)`

## Algorithm

The shortest path is calculated using Breadth-First Search (BFS), which guarantees the minimum number of stations between origin and destination.

## Future Enhancements

- [ ] Graphical visualization with Matplotlib
- [ ] Add more metro lines and stations
- [ ] Real-time train schedules
- [ ] Ticket expiry dates
- [ ] Discount tickets (senior, student)
- [ ] Multiple payment methods

## License

This project is created for educational purposes.

## Author

Metro Ticket System - OOP Project
