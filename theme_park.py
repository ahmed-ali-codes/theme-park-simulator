"""
Theme Park Class for Adventure Time Simulation

This module contains the ThemePark class which manages the entire simulation
including attractions, patrons, barriers, and the simulation loop.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import csv
from patrons import Patron
from attractions import PirateShip, FerrisWheel, FoodVendor, SideshowGame


class ThemePark:
    """
    The main theme park simulation manager.
    
    Manages all attractions, patrons, barriers, and coordinates the
    simulation timestep updates and visualization.
    """
    
    def __init__(self, width, height):
        """
        Initialize the theme park.
        
        Args:
            width (float): Width of the park
            height (float): Height of the park
        """
        self.width = width
        self.height = height
        self.attractions = []  # List of all attractions
        self.patrons = []  # List of all active patrons
        self.barriers = []  # List of barrier coordinates (x, y, width, height)
        self.entrance_x = 5  # X-coordinate of park entrance
        self.entrance_y = 5  # Y-coordinate of park entrance
        self.exit_x = width - 5  # X-coordinate of park exit
        self.exit_y = height - 5  # Y-coordinate of park exit
        self.timestep = 0  # Current simulation timestep
        self.spawn_rate = 4  # Timesteps between patron spawns (slower spawning)
        self.patron_count = 0  # Total patrons spawned
        self.patrons_exited = 0  # Total patrons who have left
        
    def add_attraction(self, attraction):
        """
        Add an attraction to the park if it doesn't overlap with existing ones.
        
        Args:
            attraction (Attraction): The attraction to add
            
        Returns:
            bool: True if successfully added, False if overlaps
        """
        # Check for overlaps with existing attractions
        for existing in self.attractions:
            if attraction.overlaps(existing):
                print(f"Warning: {attraction.name} overlaps with {existing.name}")
                return False
        
        # Add attraction (but DON'T add its bounding box as barrier - patrons can walk near attractions)
        self.attractions.append(attraction)
        return True
    
    def add_barrier(self, x, y, width, height):
        """
        Add a barrier to the park.
        
        Barriers are areas where patrons cannot walk (walls, decorations, etc.).
        
        Args:
            x (float): X-coordinate of bottom-left corner
            y (float): Y-coordinate of bottom-left corner
            width (float): Width of barrier
            height (float): Height of barrier
        """
        self.barriers.append((x, y, width, height))
    
    def spawn_patron(self):
        """
        Create a new patron at the park entrance.
        
        Increments patron count and adds new patron to the park.
        """
        self.patron_count += 1
        patron = Patron(f"P{self.patron_count}", 
                       self.entrance_x, self.entrance_y,
                       self.width, self.height,
                       self.exit_x, self.exit_y)
        self.patrons.append(patron)
    
    def step_change(self):
        """
        Update simulation by one timestep.
        
        Updates all attractions and patrons, spawns new patrons,
        and removes patrons who have exited the park.
        """
        self.timestep += 1
        
        # Spawn new patrons after timestep 5 (as per requirement)
        if self.timestep > 5 and self.timestep % self.spawn_rate == 0:
            self.spawn_patron()
        
        # Update all attractions
        for attraction in self.attractions:
            attraction.step_change()
        
        # Update all patrons
        for patron in self.patrons:
            patron.step_change(self.attractions, self.barriers)
        
        # Count and remove patrons who have exited
        exited_patrons = [p for p in self.patrons if p.state == "exited"]
        self.patrons_exited += len(exited_patrons)
        self.patrons = [p for p in self.patrons if p.state != "exited"]
    
    def plot_park(self, ax):
        """
        Plot the entire park including barriers, attractions, and patrons.
        
        Args:
            ax (matplotlib.axes.Axes): The axes to plot on
        """
        ax.clear()
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.set_title(f"Adventure Time Park - Timestep {self.timestep}")
        ax.grid(True, alpha=0.3)
        
        # Plot barriers
        for barrier in self.barriers:
            if len(barrier) == 4:
                x, y, w, h = barrier
                rect = patches.Rectangle((x, y), w, h,
                                        linewidth=1, edgecolor='black',
                                        facecolor='gray', alpha=0.3)
                ax.add_patch(rect)
        
        # Plot attractions
        for attraction in self.attractions:
            attraction.plot_me(ax)
        
        # Plot patrons
        for patron in self.patrons:
            patron.plot_me(ax)
        
        # Plot entrance and exit markers
        ax.plot(self.entrance_x, self.entrance_y, 'g*', 
               markersize=15, label='Entrance')
        ax.plot(self.exit_x, self.exit_y, 'r*', 
               markersize=15, label='Exit')
        
        # Add statistics
        stats_text = (f"Patrons in Park: {len(self.patrons)} | "
                     f"Total Spawned: {self.patron_count} | "
                     f"Exited: {self.patrons_exited}")
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               verticalalignment='top', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.legend(loc='upper right')


def load_map_from_file(filename):
    """
    Load park configuration from CSV file.
    
    CSV format: type,name,x,y,width,height
    Types: pirate_ship, ferris_wheel, food_vendor, sideshow, barrier
    
    Args:
        filename (str): Path to the map CSV file
        
    Returns:
        tuple: (attractions list, barriers list, park_width, park_height)
    """
    attractions = []
    barriers = []
    park_width = 100
    park_height = 100
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Create appropriate attraction based on type
                if row['type'] == 'pirate_ship':
                    attractions.append(PirateShip(row['name'], 
                                                 float(row['x']), float(row['y'])))
                elif row['type'] == 'ferris_wheel':
                    attractions.append(FerrisWheel(row['name'], 
                                                  float(row['x']), float(row['y'])))
                elif row['type'] == 'food_vendor':
                    attractions.append(FoodVendor(row['name'], 
                                                 float(row['x']), float(row['y'])))
                elif row['type'] == 'sideshow':
                    attractions.append(SideshowGame(row['name'], 
                                                   float(row['x']), float(row['y'])))
                elif row['type'] == 'barrier':
                    barriers.append((float(row['x']), float(row['y']),
                                   float(row['width']), float(row['height'])))
    except FileNotFoundError:
        print(f"File {filename} not found. Using default configuration.")
    except KeyError as e:
        print(f"Error reading map file: missing column {e}")
    
    return attractions, barriers, park_width, park_height


def load_parameters_from_file(filename):
    """
    Load simulation parameters from CSV file.
    
    CSV format: parameter,value
    Parameters: timesteps, spawn_rate, park_width, park_height
    
    Args:
        filename (str): Path to the parameters CSV file
        
    Returns:
        dict: Dictionary of parameter names to values
    """
    params = {
        'timesteps': 100,
        'spawn_rate': 3,
        'park_width': 100,
        'park_height': 100
    }
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                params[row['parameter']] = int(row['value'])
    except FileNotFoundError:
        print(f"Parameter file {filename} not found. Using defaults.")
    except KeyError as e:
        print(f"Error reading parameter file: missing column {e}")
    
    return params