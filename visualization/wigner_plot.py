from qlib import bra, ket, oper
from qlib import partial_trace
from qlib import compute_wigner
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def plot_wigner(wigner, x_grid, p_grid, title="Wigner Function", contour=True, figure_size=(8,6)):
    """
    Plot the Wigner function in two dimensions with a contour. 
    Parameters:
    - wigner: np.ndarray, computed Wigner function values.
    - x_grid: np.ndarray, grid of position values.
    - p_grid: np.ndarray, grid of momentum values.
    - title: str, title for the plot.
    """
    plt.figure(figsize=figure_size)
    if(contour):
        plt.contourf(x_grid, p_grid, wigner, 100, cmap='RdBu_r')
        plt.colorbar(label='Wigner function value')
    plt.xlabel('Position')
    plt.ylabel('Momentum')
    plt.title(title)
    plt.show()

def plot_wigner_3d(wigner, x_grid, p_grid, contour=True, figure_size=(10, 8)):
    """
    Plot the Wigner function in three dimensions.

    Parameters:
    - wigner: np.ndarray, computed Wigner function values.
    - x_grid: np.ndarray, grid of position values.
    - p_grid: np.ndarray, grid of momentum values.
    - title: str, title for the plot.
    """
    # Create a meshgrid for 3D plotting
    X, P = np.meshgrid(x_grid, p_grid)
    
    # Initialize the 3D plot
    fig = plt.figure(figsize=figure_size)
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    if(contour):
        ax.plot_surface(X, P, wigner, cmap='RdBu_r', edgecolor='none')
    else:
        ax.plot_surface(X, P, wigner)
    
    # Label axes
    ax.set_xlabel('Position')
    ax.set_ylabel('Momentum')
    ax.set_zlabel('Wigner Value')
    ax.set_title("Wigner Function (3D)")
    plt.show()

def animate_wigner_3d(states: list, x_grid, p_grid, contour=True, figure_size=(10, 8), interval=20, z_axis_bounds=(-0.5, 0.5)):
    X, P = np.meshgrid(x_grid, p_grid)
    are_kets = isinstance(states[0], ket)
    fig = plt.figure(figsize=figure_size)
    ax = fig.add_subplot(111, projection='3d')

    def update(frame):
        ax.clear()  
        curr_state = states[frame]
        if(are_kets):
            curr_state = curr_state.to_density_matrix()

        wig, _, _= compute_wigner(curr_state, x_grid, p_grid)

        if(contour):
            ax.plot_surface(X, P, wig, cmap='RdBu_r', edgecolor='none')
        else: 
            ax.plot_surface(X, P, wig)
        ax.set_xlabel('Position')
        ax.set_ylabel('Momentum')
        ax.set_zlabel('Wigner Value')
        z_min, z_max = z_axis_bounds
        ax.set_zlim(z_min, z_max)
        ax.set_title(f"Wigner Function at time step {frame}")
        return ax,

    return FuncAnimation(fig, update, frames=len(states), interval=interval)