import matplotlib.pyplot as pls
import numpy as np

"""Simulate Viscek Model for Flocking Birds

Create Your Own Active Matter Simulation (With Python)
Philip Mocz (2021) Princeton Univeristy, @PMocz
https://medium.com/swlh/create-your-own-active-matter-simulation-with-python-76fce4a53b6f

"""

def main():
  """Finite volume simulation"""
  
  # Simulation parameters
  v0 = 1.0 # Velocity
  eta = 0.5 # Random fluctuation in angle (in radians)
  L = 10 # Size of box
  R = 1 # Interaction radius
  dt = 0.2 # Time step
  Nt = 200 # Number of time steps
  N = 500 # Number of birds
  plotRealTime = True
  
  # Initialize
  np.random.seed(17) # Set the random number generator seed
  
  # Bird positions
  x = np.random.rand(N,1) * L
  y = np.random.rand(N,1) * L
  
  # Bird velocities
  theta = 2 * np.pi * np.random.rand(N, 1)
  vx = v0 * np.cos(theta)
  vy = v0 * np.sin(theta)
  
  # Preparatory figure
  fig = plt.figure(figsize=(4,4), dpi=80)
  ax = plt.gca()
  
  # Simulation main loop
  for i in range(Nt):
    # Move
    x += vx * dt
    y += vy * dt
    
    # Apply periodic BCs
    x = x % L
    y = y % L
    
    # Find mean angle of neighbors within R
    mean_theta = theta
    for b in range(N):
      neighbors = (x - x[b])**2 + (y - y[b])**2 < R**2
      sx = np.sum(np.cos(theta[neighbors]))
      sy = np.sum(np.sin(theta[neighbors]))
      mean_theta[b] = np.arctan2(sy, sx)
      
    # Add random perturbations
    theta = mean_theta + eta * (np.random.rand(N,1) - 0.5)
    
    # Update velocities
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)
    
    # Plot in real time
    if plotRealTime or (i == Nt - 1):
      plt.cla()
      plt.quiver(x, y, vx, vy)
      ax.set(xlim=(0, L), ylim=(0, L))
      ax.set_aspect('equal')
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)
      plt.pause(0.001)
  
  # Save figure
  plt.savefig('activematter.png', dpi=240)
  plt.show()
  
  return 0


if __name__ == "__main__":
  main()
