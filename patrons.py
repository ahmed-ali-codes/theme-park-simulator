"""
Patron Class for Adventure Time Theme Park Simulation

This module contains the Patron class representing visitors to the theme park.
Patrons can roam, queue for attractions, ride them, and eventually leave.
"""

import random


class Patron:
    """
    A visitor to the theme park.
    
    Patrons move around the park, visit attractions, and eventually leave
    after experiencing a set number of attractions.
    """
    
    def __init__(self, name, x, y, park_width, park_height, exit_x, exit_y):
        """
        Initialize a patron.
        
        Args:
            name (str): Unique identifier for the patron
            x (float): Initial x-coordinate position
            y (float): Initial y-coordinate position
            park_width (float): Width of the park for boundary checking
            park_height (float): Height of the park for boundary checking
            exit_x (float): X-coordinate of park exit
            exit_y (float): Y-coordinate of park exit
        """
        self.name = name
        self.x = x
        self.y = y
        self.park_width = park_width
        self.park_height = park_height
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.state = "roaming"  # States: "roaming", "queuing", "riding", "leaving"
        self.current_attraction = None  # Attraction patron is queuing for or riding
        self.target_attraction = None  # Attraction patron is moving towards
        self.color = 'blue'  # Display color for plotting
        self.visits = 0  # Number of attractions visited
        self.max_visits = random.randint(2, 4)  # Visit 2-4 attractions before leaving
        self.step_size = 2.0  # Faster movement speed
        self.stuck_counter = 0  # Counter to detect if patron is stuck
        
    def step_change(self, attractions, barriers):
        """
        Update patron position and state for one timestep.
        
        Args:
            attractions (list): List of all attractions in the park
            barriers (list): List of barrier coordinates (x, y, width, height)
        """
        if self.state == "roaming":
            # Check if patron should leave park
            if self.visits >= self.max_visits:
                self.leave_park()
            # Find new attraction to visit if none targeted
            elif self.target_attraction is None:
                self.find_new_target(attractions)
            # Move towards targeted attraction
            else:
                self.move_towards_target(barriers)
                
            # If stuck for too long, find new target
            if self.stuck_counter > 20:
                self.target_attraction = None
                self.stuck_counter = 0
                
        elif self.state == "leaving":
            # Move towards exit
            self.move_towards_exit(barriers)
        
    def find_new_target(self, attractions):
        """
        Select a random attraction to visit.
        
        Args:
            attractions (list): List of available attractions
        """
        if attractions:
            self.target_attraction = random.choice(attractions)
            self.stuck_counter = 0
    
    def move_towards_target(self, barriers):
        """
        Move one step towards the target attraction.
        
        Uses simple movement towards target with collision avoidance.
        Joins queue when close enough to attraction.
        
        Args:
            barriers (list): List of barrier coordinates to avoid
        """
        if self.target_attraction is None:
            return
            
        # Calculate target position (center of attraction)
        target_x = self.target_attraction.x + self.target_attraction.width / 2
        target_y = self.target_attraction.y + self.target_attraction.height / 2
        
        # Calculate direction vector
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        # Join queue if close enough to attraction
        if distance < 5:  # Increased distance for queue joining
            if self.target_attraction not in [p.current_attraction for p in self.target_attraction.queue]:
                self.target_attraction.add_to_queue(self)
                self.target_attraction = None
                self.visits += 1
                self.stuck_counter = 0
        else:
            # Move towards target
            if distance > 0:
                # Calculate new position
                new_x = self.x + (dx / distance) * self.step_size
                new_y = self.y + (dy / distance) * self.step_size
                
                # Check if we're actually moving
                old_x, old_y = self.x, self.y
                
                # Only move if new position is valid
                if self.is_valid_position(new_x, new_y, barriers):
                    self.x = new_x
                    self.y = new_y
                    # Reset stuck counter if we moved
                    if abs(new_x - old_x) > 0.1 or abs(new_y - old_y) > 0.1:
                        self.stuck_counter = 0
                    else:
                        self.stuck_counter += 1
                else:
                    self.stuck_counter += 1
    
    def is_valid_position(self, x, y, barriers):
        """
        Check if position is within park bounds and not in any barriers.
        
        Args:
            x (float): X-coordinate to check
            y (float): Y-coordinate to check
            barriers (list): List of barrier coordinates (x, y, width, height)
            
        Returns:
            bool: True if position is valid, False otherwise
        """
        # Check park boundaries (with small buffer)
        buffer = 1
        if x < buffer or x > self.park_width - buffer or y < buffer or y > self.park_height - buffer:
            return False
        
        # Check collision with barriers (but allow walking near attractions)
        for barrier in barriers:
            bx, by, bw, bh = barrier
            # Add small buffer to barriers
            if (bx - 1) <= x <= (bx + bw + 1) and (by - 1) <= y <= (by + bh + 1):
                return False
        
        return True
    
    def leave_park(self):
        """
        Mark patron as leaving the park and heading to exit.
        
        Changes state and color to indicate patron is departing.
        """
        self.state = "leaving"
        self.color = 'orange'
        self.target_attraction = None
    
    def move_towards_exit(self, barriers):
        """
        Move patron towards the exit.
        
        Args:
            barriers (list): List of barrier coordinates to avoid
        """
        dx = self.exit_x - self.x
        dy = self.exit_y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        # Remove patron when close to exit
        if distance < 5:
            self.state = "exited"
            return
        
        # Move towards exit with consistent speed
        if distance > 0:
            new_x = self.x + (dx / distance) * self.step_size
            new_y = self.y + (dy / distance) * self.step_size
            
            if self.is_valid_position(new_x, new_y, barriers):
                self.x = new_x
                self.y = new_y
    
    def plot_me(self, ax):
        """
        Plot the patron on the given matplotlib axes.
        
        Plots patrons in roaming or leaving states (not while queuing/riding).
        
        Args:
            ax (matplotlib.axes.Axes): The axes to plot on
        """
        if self.state in ["roaming", "leaving"]:
            ax.plot(self.x, self.y, 'o', color=self.color, markersize=6)