"""
python3 adventureTime.py           Default Mode
python3 adventureTime.py -i              Interactive Mode
python3 adventureTime.py -f map1.csv -p para1.csv     Batch Mode


Adventure Time - Theme Park Simulation

Main entry point for the theme park simulation.
Handles command-line arguments, user interaction, and simulation execution.
"""


import matplotlib.pyplot as plt         #Graph
import argparse       #Command line argument
import sys             #System control
from theme_park import ThemePark, load_map_from_file, load_parameters_from_file
from attractions import PirateShip, FerrisWheel, FoodVendor, SideshowGame


def interactive_mode():
    """
    Run simulation in interactive mode.
    
    Prompts user for park configuration including dimensions,
    number of each attraction type, and simulation duration.
    
    Returns:
        tuple: (ThemePark object, number of timesteps)
    """
    print("=" * 50)
    print("Adventure Time - Interactive Mode")
    print("=" * 50)
    
    # Get park dimensions
    park_width = int(input("Enter park width (default 100): ") or "100")
    park_height = int(input("Enter park height (default 100): ") or "100")
    
    # Create park
    park = ThemePark(park_width, park_height)
    
    # Get number of each attraction type
    print("\nAttractions Configuration:")
    num_pirate_ships = int(input("Number of Pirate Ships (0-3): ") or "1")
    num_ferris_wheels = int(input("Number of Ferris Wheels (0-3): ") or "1")
    num_food_vendors = int(input("Number of Food Vendors (0-5): ") or "2")
    num_sideshows = int(input("Number of Sideshows (0-5): ") or "2")
    
    # Pre-defined positions for attractions (to avoid overlaps)
    positions = [
        (20, 20), (50, 20), (20, 60), (50, 60), (75, 40), 
        (30, 80), (70, 70), (40, 40), (15, 40), (60, 35)
    ]
    pos_idx = 0
    
    # Add pirate ships
    for i in range(num_pirate_ships):
        if pos_idx < len(positions):
            x, y = positions[pos_idx]
            park.add_attraction(PirateShip(f"Pirate Ship {i+1}", x, y))
            pos_idx += 1
    
    # Add ferris wheels
    for i in range(num_ferris_wheels):
        if pos_idx < len(positions):
            x, y = positions[pos_idx]
            park.add_attraction(FerrisWheel(f"Ferris Wheel {i+1}", x, y))
            pos_idx += 1
    
    # Add food vendors
    for i in range(num_food_vendors):
        if pos_idx < len(positions):
            x, y = positions[pos_idx]
            park.add_attraction(FoodVendor(f"Food Cart {i+1}", x, y))
            pos_idx += 1
    
    # Add sideshows
    for i in range(num_sideshows):
        if pos_idx < len(positions):
            x, y = positions[pos_idx]
            park.add_attraction(SideshowGame(f"Game {i+1}", x, y))
            pos_idx += 1
    
    # Get simulation parameters
    print("\nSimulation Configuration:")
    timesteps = int(input("Number of timesteps (default 300): ") or "300")
    spawn_rate = int(input("Patron spawn rate (default 4): ") or "4")
    park.spawn_rate = spawn_rate
    
    print("\n" + "=" * 50)
    print(f"Park configured with {len(park.attractions)} attractions")
    print("=" * 50)
    
    return park, timesteps


def batch_mode(map_file, param_file):
    """
    Run simulation in batch mode.
    
    Loads park configuration from CSV files.
    
    Args:
        map_file (str): Path to map configuration CSV file
        param_file (str): Path to parameters CSV file
        
    Returns:
        tuple: (ThemePark object, number of timesteps)
    """
    print("=" * 50)
    print("Adventure Time - Batch Mode")
    print("=" * 50)
    print(f"Map file: {map_file}")
    print(f"Parameter file: {param_file}")
    print("=" * 50)
    
    # Load configuration files
    attractions, barriers, park_width, park_height = load_map_from_file(map_file)
    params = load_parameters_from_file(param_file)
    
    # Create park with parameters
    park = ThemePark(params.get('park_width', park_width), 
                    params.get('park_height', park_height))
    
    # Add all attractions
    for attraction in attractions:
        park.add_attraction(attraction)
    
    # Add all barriers
    for barrier in barriers:
        park.add_barrier(*barrier)
    
    # Set spawn rate
    park.spawn_rate = params.get('spawn_rate', 3)
    
    print(f"\nPark configured with {len(park.attractions)} attractions")
    print(f"Spawn rate: {park.spawn_rate} timesteps")
    print("=" * 50)
    
    return park, params.get('timesteps', 100)


def default_mode():
    """
    Run simulation in default mode with pre-configured park.
    
    Creates a sample park with various attractions for demonstration.
    
    Returns:
        tuple: (ThemePark object, number of timesteps)
    """
    print("=" * 50)
    print("Adventure Time - Default Mode")
    print("=" * 50)
    print("Running with sample park configuration...")
    print("Watch patrons enter, visit multiple attractions, then exit!")
    print("=" * 50)
    
    # Create park with default dimensions
    park = ThemePark(100, 100)
    
    # Add sample attractions
    park.add_attraction(PirateShip("Pirate Adventure", 20, 20))
    park.add_attraction(FerrisWheel("Sky View", 50, 20))
    park.add_attraction(FoodVendor("Snack Shack", 20, 60))
    park.add_attraction(SideshowGame("Ring Toss", 50, 60))
    park.add_attraction(FoodVendor("Ice Cream", 75, 40))
    
    timesteps = 400
    
    print(f"\nPark configured with {len(park.attractions)} attractions")
    print(f"Spawn rate: Every 4 timesteps (slower entry)")
    print(f"Timesteps: {timesteps}")
    print(f"Blue dots = Roaming | Orange dots = Leaving to Exit")
    print("=" * 50)
    
    return park, timesteps


def run_simulation(park, timesteps):
    """
    Execute the simulation loop with visualization.
    
    Args:
        park (ThemePark): The configured theme park
        timesteps (int): Number of timesteps to simulate
    """
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 10))
    
    print(f"\nRunning simulation for {timesteps} timesteps...")
    print("Close the plot window to end simulation.")
    print("-" * 50)
    
    # Simulation loop
    for t in range(timesteps):
        park.step_change()
        
        # Update plot every 3 timesteps for better visualization
        if t % 3 == 0:
            park.plot_park(ax)
            plt.pause(0.05)
            
        # Print stats every 10 timesteps
        if t % 10 == 0:
            print(f"Timestep: {t:4d} | In Park: {len(park.patrons):3d} | "
                  f"Spawned: {park.patron_count:3d} | Exited: {park.patrons_exited:3d}")
    
    # Final plot
    park.plot_park(ax)
    plt.show()
    
    # Print summary statistics
    print("\n" + "=" * 50)
    print("Simulation Complete!")
    print("=" * 50)
    print(f"Total timesteps: {park.timestep}")
    print(f"Total patrons spawned: {park.patron_count}")
    print(f"Patrons remaining in park: {len(park.patrons)}")
    print(f"Patrons exited: {park.patrons_exited}")
    print(f"Number of attractions: {len(park.attractions)}")
    
    # Print attraction statistics
    print("\nAttraction Statistics:")
    print("-" * 50)
    for attraction in park.attractions:
        queue_size = len(attraction.queue)
        riders = len(attraction.riders)
        status = attraction.state
        print(f"{attraction.name:20s} | Queue: {queue_size:2d} | "
              f"Riders: {riders:2d} | Status: {status}")
    
    print("=" * 50)


def main():
    """
    Main entry point for the simulation.
    
    Parses command-line arguments and runs simulation in appropriate mode.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Adventure Time Theme Park Simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python3 adventureTime.py -i
    
  Batch mode:
    python3 adventureTime.py -f map1.csv -p para1.csv
    
  Default mode:
    python3 adventureTime.py
        """
    )
    
    parser.add_argument('-i', '--interactive', 
                       action='store_true',
                       help='Run in interactive mode (prompts for configuration)')
    parser.add_argument('-f', '--map-file', 
                       type=str,
                       help='Map configuration CSV file for batch mode')
    parser.add_argument('-p', '--param-file', 
                       type=str,
                       help='Parameter CSV file for batch mode')
    
    args = parser.parse_args()
    
    # Determine mode and configure park
    try:
        if args.interactive:
            park, timesteps = interactive_mode()
        elif args.map_file and args.param_file:
            park, timesteps = batch_mode(args.map_file, args.param_file)
        elif args.map_file or args.param_file:
            print("Error: Both -f and -p required for batch mode")
            parser.print_help()
            sys.exit(1)
        else:
            park, timesteps = default_mode()
        
        # Run the simulation
        run_simulation(park, timesteps)
        
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()