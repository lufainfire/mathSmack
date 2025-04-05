import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib import animation


fig = plt.figure(facecolor='xkcd:grey')
ax = plt.axes(projection = "3d")

#set background color and remove axis
ax.set_facecolor('xkcd:green')
ax.set_axis_off()

u = np.linspace(0, 2*np.pi, 100)
v = np.linspace(0, np.pi, 100)
r = 4

ax.set_xlim(0, 60)
ax.set_ylim(0, 60)
ax.set_zlim(0, 60)

x0 = r * np.outer(np.cos(u), np.sin(v)) + 10
y0 = r * np.outer(np.sin(u), np.sin(v)) + 10
z0 = r * np.outer(np.ones(np.size(u)), np.cos(v)) + 50

x1 = r * np.outer(np.cos(u), np.sin(v))
y1 = r * np.outer(np.sin(u), np.sin(v)) 
z1 = r * np.outer(np.ones(np.size(u)), np.cos(v)) +50

surface_color = "tab:blue"
surface_new_color = "xkcd:dark"

def init():
    ax.plot_surface(x0, y0, z0, color=surface_color)
    ax.plot_surface(x1, y1, z1, color=surface_new_color)
    return fig,

def animate(i):
    for artist in plt.gca().lines + plt.gca().collections:
        artist.remove()
    # add the new sphere
    if np.array_equal(x0,x1):
        print("collision")
        ax.plot_surface(x0 + i, -y0 + i, z0, color=surface_color)
        ax.plot_surface(x1 +i, -y1+i, z1+i, color=surface_new_color)

    else:
        ax.plot_surface(x0, y0, z0, color=surface_color)
        ax.plot_surface(x1 +i, y1+i, z1, color=surface_new_color)
    return fig

ani = animation. FuncAnimation(fig, animate, init_func = init, frames = 60, interval = 100)
plt.show()