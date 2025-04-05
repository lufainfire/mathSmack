import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

mpl.rcParams['axes3d.mouserotationstyle'] = 'trackball'  # 'azel', 'trackball', 'sphere', or 'arcball'

from mpl_toolkits.mplot3d import Axes3D

def ballSphere(disk, radius):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return x+disk[0],y+disk[1],z+disk[2]

def plotting_spheres(data, colors):
    fig = plt.figure(figsize=(12,12), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    for k,sph in enumerate(data):
        x, y, z = sph[0], sph[1], sph[2]
        ax.plot_surface(x, y, z,  rstride=4, cstride=4, 
                        color=colors[k], linewidth=0, alpha=0.5)
    ax.set_aspect("equal")
    plt.show()

N = 5 # spheres
position = [[7, 9, 2],[5, 9, 9],[9, 3, 9],[5, 5, 1],[5, 7, 9]]
rs = [3,3,3,3,3]
colors = ("r","g","b","y","m")
#data = [ballSphere(position[k,:], rs[k]) for k in range(N)]
#print(position)
#plotting_spheres(data, colors)
def createSphere(N,xs,ys,zs,radius):
    x = []
    y = []
    z = []
    for i in xs:
        x.append(int(i))
    for i in ys:
        y.append(int(i))
    for i in zs:
        z.append(int(i))
    position = np.ndarray(x,y,z)
    for i in range(N):
        rs.append(radius)
    data = [ballSphere(position[k,:], rs[k]) for k in range(N)]
    plotting_spheres(data, colors)
        
class Ball:
    def __init__(self, radius, position, velocity, mass):
        self.radius = radius
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass

    def move(self, dt):
        self.position += self.velocity * dt

    def check_wall_collision(self, box_size):
        for i in range(2):
            if self.position[i] - self.radius < 0 or self.position[i] + self.radius > box_size:
                self.velocity[i] *= -1

    def collision(self, other):
        delta_pos = other.position - self.position
        distance = np.linalg.norm(delta_pos)
        if distance < self.radius + other.radius:
            delta_vel = other.velocity - self.velocity
            unit_vector = delta_pos / distance
            velocity_change = np.dot(delta_vel, unit_vector)
            if velocity_change < 0:
                impulse = 2 * velocity_change / (self.mass + other.mass)
                self.velocity += impulse * other.mass * unit_vector
                other.velocity -= impulse * self.mass * unit_vector
xs = []
ys = []
zs = []

def init_balls(num_particles, box_size):
    balls = []
    for _ in range(num_particles):
        radius = 0.01
        position = np.random.rand(2) * (box_size - 2 * radius) + radius
        velocity = np.random.randn(2) * 0.1
        mass = 1.0
        balls.append(Ball(radius, position, velocity, mass))
    return balls

def update(frame, balls, box_size, ax):
    for ball in balls:
        ball.move(0.1)
        ball.check_wall_collision(box_size)
        for other_ball in balls:
            if ball != other_ball:
                ball.collision(other_ball)
    #remove (clean) and put it back
    ax.clear()
    xs = []
    ys = []
    zs = []
    for ball in balls:
        #alternator to switch between x and y position points to add them to the array
        alternator = True
        for i in ball.position:
            if alternator:
                xs.append(i)
                alternator = False
                zs.append(0)
            else:
                ys.append(i)
                alternator = True
        #print(particle.position)
    #creating new scatters as balls
    ax.scatter(xs,ys,zs)
    ax.set_xlim(0, box_size)
    ax.set_ylim(0, box_size)
    ax.set_aspect('equal')

def run_simulation(num_particles=30, box_size=1.0):
    particles = init_balls(num_particles, box_size)
    #fig, ax = plt.subplots()
    #ax = fig.add_subplot(projection='3d')
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    createSphere(num_particles,xs,ys,zs,0.1)
    ax.scatter(xs, ys, zs)
    ani = FuncAnimation(fig, update, fargs=(particles, box_size, ax),
                      frames=200, interval=50, repeat=False)
    #surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()

run_simulation()