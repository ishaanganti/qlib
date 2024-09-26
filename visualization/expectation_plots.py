from qlib import *
from numpy import linspace
import matplotlib.pyplot as plt
import numpy as np

def expectation_line_plot(states, opers, t0 = None, tf = None, plot_style = "vanilla"):
    if not isinstance(opers, list):
        opers = [opers]

    num_states = len(states)
    if(t0 == None and tf == None):
        t0, tf = 0, num_states - 1
    interval = tf - t0 + 1
    time_range = linspace(t0, tf, num_states)
    
    fig, ax = plt.subplots()
    
    if plot_style == "clean":
        line_color, legend_edge_color = set_clean_plot_style(ax, inverted=False)
    elif plot_style == "clean_inverted":
        line_color, legend_edge_color = set_clean_plot_style(ax, inverted=True)
    elif plot_style == "vanilla":
        line_color, legend_edge_color = set_vanilla_plot_style(ax)
    else: # for a random user input
        line_color, legend_edge_color = 'black', 'white'

    result = np.zeros((len(opers), len(states)))
    states_array = np.array([state.to_vector() for state in states])
    for idx, oper in enumerate(opers):
        oper_array = oper.to_matrix()
        temp = np.dot(states_array, oper_array)
        result[idx] = np.sum(np.conj(states_array) * temp, axis=1).real
        ax.plot(time_range, result[idx], linewidth=2, label=f'Oper {idx + 1}')
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Expected Value')
    ax.set_title('Expected Value of Observable Over Time')
    
    # clean legend setup
    legend = ax.legend(frameon=True, framealpha=1)
    legend.get_frame().set_edgecolor(legend_edge_color)

    # return figure and axis objects for further manipulation
    return fig, ax

def set_clean_plot_style(ax, inverted=False):
    if not inverted:
        # light mode
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#dddddd')
        ax.spines['bottom'].set_color('#dddddd')
        ax.tick_params(axis='both', colors='gray', which='both')
        ax.xaxis.label.set_color('gray')
        ax.yaxis.label.set_color('gray')
        ax.title.set_color('gray')
        ax.grid(True, color='#eeeeee', linestyle='-', linewidth=1)
        ax.set_facecolor('white')
        line_color = 'steelblue'
        legend_edge_color = 'white'
    else:
        # dark mode
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#dddddd')
        ax.spines['bottom'].set_color('#dddddd')
        ax.tick_params(axis='both', colors='gray', which='both')
        ax.xaxis.label.set_color('gray')
        ax.yaxis.label.set_color('gray')
        ax.title.set_color('gray')
        ax.grid(True, color='#333333', linestyle='-', linewidth=1)
        ax.set_facecolor('#202020')
        line_color = '#00bcd4'
        legend_edge_color = '#202020'

    return line_color, legend_edge_color 

def set_vanilla_plot_style(ax):
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.grid(False)
    ax.set_facecolor('white')
    return 'black', 'white'

