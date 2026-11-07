import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import PillowWriter

# m = masse objet en kg
m = 10
# g = cste gravité en m.s^-2
g = 9.8
# position initiale en m
x_init = 0
y_init = 0
# vitesse initiale en m.s^-1
vx_init = 5
vy_init = 5
# vecteurs de pos
x = [x_init]
y = [y_init]
# vecteurs de vitesse
vx = [vx_init]
vy = [vy_init]
# coefficient de frottements
k = 0.2
tau = m/k
# temps
t = np.linspace(0,1,100)

### BALISTIC
# angle en degré
angle = 270
angle_rad = angle*(np.pi)/180
# vitesse initiale selon l'angle en m.s^-1
va_init = 5

def chute(g, x, y, t) :
    n=0
    for i in t :
        x.append(vx_init*i)
        vx.append(vx_init)
        y.append(-(1/2)*g*(i**2) + vy_init*i)
        vy.append(-g*i + vy_init)
        n = n + 1
    return x, y
    
def balistic(angle_rad, g, x, y, t) :
    n = 0
    for i in t :
        x.append(va_init*np.cos(angle_rad)*i)
        y.append(-(1/2)*g*(i**2) + va_init*np.sin(angle_rad)*i)
        n = n + 1
    return x, y

def chute_frottements() :
    n=0
    for i in t :
        x.append(vx_init*i)
        vx.append(vx_init)
        y.append(g*(tau**2)*(1-np.exp(-i/tau)) - g*tau*i + y_init)
        vy.append(g*tau*(np.exp(-i/tau)-1) + vy_init)
        n = n + 1
    return x, y

x, y = chute(g, x, y, t)
#x, y = balistic(angle, g, x, y, t)
#x, y = chute_frottements()

def animate(i):
    traj.set_data(x[:i], y[:i])
    point.set_data(x[i], y[i])
    vitesse_y.set_data(t[:i], vy[:i])
    return traj,

fig, ax = plt.subplots(2)
point, = ax[0].plot([], [], color='blue', marker='o', markersize=5)
traj, = ax[0].plot([], [], color='blue', linestyle='dashed')
vitesse_y, = ax[1].plot([], [], color='red')
ax[0].set_xlim(min(x),max(x))
ax[1].set_xlim(min(t),max(t))
#plt.xlim(-200,200)
ax[0].set_ylim(min(y),max(y))
ax[1].set_ylim(min(vy),max(vy))
#plt.ylim(-200,200)
ax[0].grid()
ax[1].grid()

ani = animation.FuncAnimation(fig, animate, frames=100, interval=50, blit=True, repeat=False)
ani.save("C:/Users/matdan/Desktop/Code/Python Phys Sim/balistic.gif", writer='pillow', fps=30)
    
#plt.show()

### IDEES
# faire un truc pour calculer le meilleur angle pour maximiser la distance en fct de la vitesse initiale
# afficher trainee derrier la balle
# afficher angle a la base
# afficher vitesse de la balle en live
# faire que le temps continue jusqu'a arriver a 0, avec un dt qui s'incremente peut etre
# traj de roquette avec une terre ronde et apres calcul de max q et calcul de vitesse d'echappage pour etre en orbite

### PROBLEMES
# a 90 degre je pars pas vertical ??????