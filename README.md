# Adventure Time Theme Park Simulation

A Python-based interactive theme park simulation that models patron behavior, attraction dynamics, and visual animation in a virtual amusement park environment.

## 🎡 Overview

This project simulates a theme park where virtual patrons enter, roam around, queue for attractions, ride them, and eventually exit. The simulation includes animated rides, realistic patron behavior, and a visual interface using Matplotlib.

## ✨ Features

- **Multiple Attraction Types**:
  - Pirate Ship (swinging animation)
  - Ferris Wheel (rotating animation)
  - Food Vendor (quick service)
  - Sideshow Games (quick play)

- **Three Simulation Modes**:
  - **Default Mode**: Pre-configured sample park
  - **Interactive Mode**: Customize park via command prompts
  - **Batch Mode**: Load park configuration from CSV files

- **Realistic Patron Behavior**:
  - Patrons roam, queue, and ride attractions
  - Visit 2-4 attractions before leaving
  - Intelligent pathfinding with barrier avoidance
  - Animation visualization with different colors for states

- **Visual Simulation**:
  - Real-time animation with Matplotlib
  - Attraction-specific animations (swinging, rotating)
  - Statistics overlay
  - Color-coded patron states (blue=roaming, orange=leaving)

## 📁 Project Structure

```
adventure-time-theme-park/
│
├── adventureTime.py          # Main entry point
├── attractions.py            # Attraction classes (PirateShip, FerrisWheel, etc.)
├── theme_park.py             # ThemePark class and file loading
├── patrons.py                # Patron class and behavior
│
├── map1.csv                  # Sample map configuration 1
├── map2.csv                  # Sample map configuration 2
├── para1.csv                 # Sample parameters 1
├── para2.csv                 # Sample parameters 2
│
├── requirements.txt          # Python dependencies
├── uml_class_diagram.svg     # UML class diagram
└── README.md                 # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/ahmed-ali-codes/theme-park-simulator.git
cd theme-park-simulator
```

### 2. Install Dependencies
```bash
pip install matplotlib
```

### 3. Run the Simulation

**Default Mode** (pre-configured park):
```bash
python3 adventureTime.py
```

**Interactive Mode** (customize your park):
```bash
python3 adventureTime.py -i
```

**Batch Mode** (load from CSV files):
```bash
python3 adventureTime.py -f map1.csv -p para1.csv
```

## 📊 CSV File Format

### Map Configuration (`map1.csv`, `map2.csv`)
```csv
type,name,x,y,width,height
pirate_ship,Pirate Adventure,15,15,15,10
ferris_wheel,Sky Wheel,45,15,12,12
barrier,Park Boundary,0,0,100,5
```

**Types**: `pirate_ship`, `ferris_wheel`, `food_vendor`, `sideshow`, `barrier`

### Parameters Configuration (`para1.csv`, `para2.csv`)
```csv
parameter,value
timesteps,400
spawn_rate,4
park_width,100
park_height,100
```

## 🎮 How to Use

### Interactive Mode
1. Run `python3 adventureTime.py -i`
2. Enter park dimensions (default 100x100)
3. Specify number of each attraction type (0-5)
4. Set simulation duration and spawn rate
5. Watch the simulation run with real-time animation!

### Batch Mode
1. Prepare your map CSV file with attractions and barriers
2. Prepare your parameters CSV file
3. Run: `python3 adventureTime.py -f your_map.csv -p your_params.csv`

### During Simulation
- **Blue dots**: Patrons roaming and visiting attractions
- **Orange dots**: Patrons leaving the park
- **Green star**: Park entrance
- **Red star**: Park exit
- **Gray boxes**: Barriers (patrons cannot walk through)
- **Colored boxes**: Attractions with queue/rider info

## 🎯 Key Features in Detail

### Attraction Behaviors
- **Pirate Ship**: Swings back and forth with realistic pendulum motion
- **Ferris Wheel**: Rotates continuously with visible pods
- **Food Vendor**: Quick service with small capacity
- **Sideshow Games**: Quick play time with few players

### Patron AI
- Random attraction selection
- Barrier avoidance
- Queue management
- Visit counting before exit
- Stuck detection and recovery

### Statistics Display
- Real-time patron counts
- Queue and rider information per attraction
- Total spawned and exited patrons
- Attraction status (idle/running)

## 🔧 Customization

### Creating Custom Maps
1. Create a CSV file following the map format
2. Place attractions strategically (avoid overlaps)
3. Add barriers to create interesting park layouts
4. Adjust parameters in the parameters CSV file

### Modifying Attraction Parameters
Edit `attractions.py` to change:
- Ride durations
- Capacities
- Animation speeds
- Visual appearance

### Adjusting Patron Behavior
Edit `patrons.py` to modify:
- Movement speed
- Number of visits before leaving
- Stuck detection thresholds
- Pathfinding logic

## 📈 Sample Output

```
==================================================
Adventure Time - Default Mode
==================================================
Running with sample park configuration...
Watch patrons enter, visit multiple attractions, then exit!
==================================================

Park configured with 5 attractions
Spawn rate: Every 4 timesteps (slower entry)
Timesteps: 400
Blue dots = Roaming | Orange dots = Leaving to Exit
==================================================

Timestep:    0 | In Park:   0 | Spawned:   0 | Exited:   0
Timestep:   10 | In Park:   1 | Spawned:   1 | Exited:   0
Timestep:   20 | In Park:   4 | Spawned:   4 | Exited:   0
...
```

## 🛠️ Development

### Adding New Attraction Types
1. Create a new class in `attractions.py` inheriting from `Attraction`
2. Implement custom `step_change()` for animation
3. Implement custom `plot_me()` for visualization
4. Update `load_map_from_file()` in `theme_park.py` to handle new type

### Extending Simulation Features
- Add different patron types (families, couples, singles)
- Implement weather effects
- Add day/night cycles
- Include revenue tracking
- Add more complex pathfinding algorithms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Matplotlib for visualization capabilities
- Python Standard Library for robust data structures
- All contributors who help improve this simulation

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Provide detailed description of the problem or suggestion
- Include steps to reproduce if reporting a bug

---
