import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Ball:
    def __init__(self, radius, position, velocity, mass):
        self.radius = radius
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass

    def move(self, dt):
        self.position += self.velocity * dt

    def collision(self, box_size):
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
        ball.collision(box_size)
        for other_ball in balls:
            if ball != other_ball:
                ball.check_particle_collision(other_ball)
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
num_particles=30
box_size=1.0
particles = init_balls(num_particles, box_size)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.scatter(xs, ys, zs)
ani = FuncAnimation(fig, update, fargs=(particles, box_size, ax),frames=200, interval=50, repeat=False)
plt.show()
