"""
Attraction Classes for Adventure Time Theme Park Simulation


This module contains all attraction classes including rides, food vendors,
and sideshow games. Each attraction manages its own state, queue, and riders.
"""

import matplotlib.pyplot as plt        #Graph
import matplotlib.patches as patches   #Shapes
from collections import deque         #Queue


class Attraction:
    """
    Base class for all theme park attractions.
    
    Attractions have a physical location and size, manage queues of patrons,
    and operate on cycles with specific durations and capacities.
    """
    
    def __init__(self, name, x, y, width, height, capacity, duration):
        """
        Initialize an attraction.
        
        Args:
            name (str): Name of the attraction
            x (float): X-coordinate of bottom-left corner
            y (float): Y-coordinate of bottom-left corner
            width (float): Width of bounding box
            height (float): Height of bounding box
            capacity (int): Maximum patrons per ride cycle
            duration (int): Time steps for one complete cycle
        """

        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.capacity = capacity
        self.duration = duration
        self.state = "idle"  # States: "idle" or "running"
        self.queue = deque()  # Patrons waiting for the attraction
        self.riders = []     # Patrons currently on the attraction
        self.time_remaining = 0  # Timesteps remaining in current cycle
        
    def get_bounding_box(self):
        """
        Return the bounding box coordinates.
        
        Returns:
            tuple: (x1, y1, x2, y2) coordinates of bounding box
        """
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    
    def overlaps(self, other):
        """
        Check if this attraction overlaps with another attraction.
        
        Args:
            other (Attraction): Another attraction to check against
            
        Returns:
            bool: True if attractions overlap, False otherwise
        """
        x1, y1, x2, y2 = self.get_bounding_box()
        ox1, oy1, ox2, oy2 = other.get_bounding_box()
        return not (x2 < ox1 or x1 > ox2 or y2 < oy1 or y1 > oy2)
    
    def add_to_queue(self, patron):
        """
        Add a patron to the attraction's queue.
        
        Args:
            patron (Patron): The patron joining the queue
        """
        self.queue.append(patron)
        patron.state = "queuing"
        patron.current_attraction = self
    
    def can_start_ride(self):
        """
        Check if the ride can start with current queue.
        
        Returns:
            bool: True if ride can start, False otherwise
        """
        return len(self.queue) >= 1 and self.state == "idle"  # Start with at least 1 patron
    
    def start_ride(self):
        """
        Start the ride/attraction with patrons from queue.
        
        Moves patrons from queue to riders list and changes state to running.
        """
        if self.can_start_ride():
            count = min(self.capacity, len(self.queue))
            for _ in range(count):
                patron = self.queue.popleft()
                self.riders.append(patron)
                patron.state = "riding"
            self.state = "running"
            self.time_remaining = self.duration
    
    def step_change(self):
        """
        Update attraction state for one timestep.
        
        Decrements time remaining and finishes ride when complete.
        Attempts to start new ride if idle.
        """
        if self.state == "running":
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.finish_ride()
        elif self.state == "idle":
            if len(self.queue) > 0:  # Only try to start if there are people in queue
                self.start_ride()
    
    def finish_ride(self):
        """
        Complete the ride and release patrons back to roaming state.
        """
        for patron in self.riders:
            patron.state = "roaming"
            patron.current_attraction = None
        self.riders = []
        self.state = "idle"
    
    def plot_me(self, ax):
        """
        Plot the attraction on the given matplotlib axes.
        
        Args:
            ax (matplotlib.axes.Axes): The axes to plot on
        """
        # Draw bounding box
        rect = patches.Rectangle((self.x, self.y), self.width, self.height,
                                linewidth=2, edgecolor='black', 
                                facecolor='lightblue', alpha=0.5)
        ax.add_patch(rect)
        
        # Draw attraction name
        ax.text(self.x + self.width/2, self.y + self.height/2, 
               self.name, ha='center', va='center', fontsize=8)
        
        # Draw queue and rider info
        info_text = f"Q:{len(self.queue)} R:{len(self.riders)}"
        ax.text(self.x + self.width/2, self.y - 5, 
               info_text, ha='center', va='top', fontsize=7, color='red')


class PirateShip(Attraction):
    """
    Pirate ship ride that swings back and forth in an arc.
    
    Animates by rotating between positive and negative angles.
    Large capacity ride with longer duration.
    """
    
    def __init__(self, name, x, y):
        """
        Initialize a pirate ship attraction.
        
        Args:
            name (str): Name of the pirate ship
            x (float): X-coordinate position
            y (float): Y-coordinate position
        """
        super().__init__(name, x, y, width=15, height=10, capacity=20, duration=20)
        self.angle = 0  # Current swing angle
        self.direction = 1  # Swing direction: 1 or -1
        self.max_angle = 60  # Maximum swing angle in degrees
        
    def step_change(self):
        """
        Update ride state including swing animation.
        
        Overrides parent to add swing animation when running.
        """
        super().step_change()
        
        # Animate swing when running
        if self.state == "running":
            self.angle += 3 * self.direction
            if abs(self.angle) >= self.max_angle:
                self.direction *= -1  # Reverse direction at max angle
        else:
            self.angle = 0  # Reset to center when idle
    
    def plot_me(self, ax):
        """
        Plot pirate ship with swing animation.
        
        Args:
            ax (matplotlib.axes.Axes): The axes to plot on
        """
        super().plot_me(ax)
        
        # Calculate ship position based on swing angle
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        
        ship_length = 8
        angle_rad = self.angle * 3.14159 / 180
        end_x = center_x + ship_length * 0.5 * angle_rad
        end_y = center_y - ship_length * 0.5
        
        # Draw ship as line with marker
        ax.plot([center_x, end_x], [center_y, end_y], 
               'brown', linewidth=4, marker='o', markersize=10)


class FerrisWheel(Attraction):
    """
    Ferris wheel that rotates continuously with visible pods.
    
    Shows rotation animation with pods positioned around the wheel.
    Medium capacity ride with longer duration.
    """
    
    def __init__(self, name, x, y):
        """
        Initialize a ferris wheel attraction.
        
        Args:
            name (str): Name of the ferris wheel
            x (float): X-coordinate position
            y (float): Y-coordinate position
        """
        super().__init__(name, x, y, width=12, height=12, capacity=24, duration=25)
        self.rotation = 0  # Current rotation angle in degrees
        
    def step_change(self):
        """
        Update wheel rotation animation.
        
        Overrides parent to add rotation when running.
        """
        super().step_change()
        
        # Rotate wheel when running
        if self.state == "running":
            self.rotation += 5  # Degrees per timestep
            if self.rotation >= 360:
                self.rotation = 0
    
    def plot_me(self, ax):
        """
        Plot ferris wheel with rotation and pods.
        
        Args:
            ax (matplotlib.axes.Axes): The axes to plot on
        """
        super().plot_me(ax)
        
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        radius = min(self.width, self.height) / 2.5
        
        # Draw wheel rim
        circle = plt.Circle((center_x, center_y), radius, 
                          fill=False, color='red', linewidth=2)
        ax.add_patch(circle)
        
        # Draw pods around the wheel
        num_pods = 8
        for i in range(num_pods):
            angle = (self.rotation + i * 45) * 3.14159 / 180
            pod_x = center_x + radius * 0.9 * plt.np.cos(angle)
            pod_y = center_y + radius * 0.9 * plt.np.sin(angle)
            ax.plot(pod_x, pod_y, 'ro', markersize=6)


class FoodVendor(Attraction):
    """
    Food vendor that serves patrons quickly.
    
    Small capacity with short service duration.
    Represents food carts, snack stands, etc.
    """
    
    def __init__(self, name, x, y):
        """
        Initialize a food vendor attraction.
        
        Args:
            name (str): Name of the food vendor
            x (float): X-coordinate position
            y (float): Y-coordinate position
        """
        super().__init__(name, x, y, width=6, height=6, capacity=5, duration=3)
        
    def plot_me(self, ax):
        """
        Plot food vendor with distinctive color scheme.
        
        Args:
            ax (matplotlib.axes.Axes): The axes to plot on
        """
        # Draw vendor box in yellow/green
        rect = patches.Rectangle((self.x, self.y), self.width, self.height,
                                linewidth=2, edgecolor='green', 
                                facecolor='yellow', alpha=0.6)
        ax.add_patch(rect)
        
        # Draw vendor name
        ax.text(self.x + self.width/2, self.y + self.height/2, 
               self.name, ha='center', va='center', fontsize=7)
        
        # Draw queue and rider info
        info_text = f"Q:{len(self.queue)} R:{len(self.riders)}"
        ax.text(self.x + self.width/2, self.y - 5, 
               info_text, ha='center', va='top', fontsize=7, color='red')


class SideshowGame(Attraction):
    """
    Sideshow game with quick play time.
    
    Small capacity carnival game (ring toss, balloon pop, etc.).
    Quick play duration with few players at once.
    """
    
    def __init__(self, name, x, y):
        """
        Initialize a sideshow game attraction.
        
        Args:
            name (str): Name of the sideshow game
            x (float): X-coordinate position
            y (float): Y-coordinate position
        """
        super().__init__(name, x, y, width=8, height=8, capacity=3, duration=8)
        
    def plot_me(self, ax):
        """
        Plot sideshow game with distinctive color scheme.
        
        Args:
            ax (matplotlib.axes.Axes): The axes to plot on
        """
        # Draw game box in pink/purple
        rect = patches.Rectangle((self.x, self.y), self.width, self.height,
                                linewidth=2, edgecolor='purple', 
                                facecolor='pink', alpha=0.6)
        ax.add_patch(rect)
        
        # Draw game name
        ax.text(self.x + self.width/2, self.y + self.height/2, 
               self.name, ha='center', va='center', fontsize=7)
        
        # Draw queue and rider info
        info_text = f"Q:{len(self.queue)} R:{len(self.riders)}"
        ax.text(self.x + self.width/2, self.y - 5, 
               info_text, ha='center', va='top', fontsize=7, color='red')