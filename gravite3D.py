import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import axes3d

# Constantes
# G en m3 kg-1 s-2
G = 6.674*(10**(-11))
# dt donc échelle de temps (un grand dt fait passer le temps plus vite)
dt = 10000000
# Nombre de frames pour le rendu
frames = 1000

# VECTEURS S : [x , y , z , Vx , Vy , Vz]
# Corps 1
m1 = 10000
s1 = [0,0,0,0,20,0]
liste_s1_x = []  # Liste qui servent à tracer le trajet du corps
liste_s1_y = []
liste_s1_z = []
liste_s1_x.append(s1[0])
liste_s1_y.append(s1[1])
liste_s1_z.append(s1[2])
# Corps 2
m2 = 1
s2 = [500,3500,1500,50,0,0]
liste_s2_x = []  # Liste qui servent à tracer le trajet du corps
liste_s2_y = []
liste_s2_z = []
liste_s2_x.append(s2[0])
liste_s2_y.append(s2[1])
liste_s2_z.append(s2[2])

# Calcul de la force de gravitation (en N)
def Fab(ma, mb, d) :
    return G*ma*mb/(d**2)

# Calcul de la distance entre 2 corps (en m)
def d(sa, sb) :
    return np.sqrt((sb[2]-sa[2])**2 + (sb[1]-sa[1])**2 + (sb[0]-sa[0])**2)

# Calcul des composantes du vecteur qui sépare 2 objets (divisé par la distance pour le normer)
def vecteur_AB(A, B) :
    return [ B[0]-A[0] , B[1]-A[1] , B[2]-A[2]] / d(A,B)

# Fonction qui met à jours les positions à chaque itération en calculant les forces, vitesses, positions
def update_pos(s1, s2) :
    
    distance = d(s1, s2)
    #print("Distance Terre -> Soleil :",distance)
    F = Fab(m1, m2, distance)
    
    # Permet de récupérer l'orientation de la force de gravité pour l'appliquer dans la bonne direction
    vect_grav12 = vecteur_AB(s1,s2)
    vect_grav21 = vecteur_AB(s2,s1)
    
    # Application de la deuxième loi de Newton sur le corps 1
    s1[0] = s1[0] + (1/2)*F/m1*(dt**2)*vect_grav12[0] + s1[3]
    s1[1] = s1[1] + (1/2)*F/m1*(dt**2)*vect_grav12[1] + s1[4]
    s1[2] = s1[2] + (1/2)*F/m1*(dt**2)*vect_grav12[2] + s1[5]
    
    # JE CROIS QU'IL FAUDRAIT MULTIPLIER LA VITESSE PAR DT ?? (ça marche mieux sans mais c'est chelou que je le fasse pas)
    # Application de la deuxième loi de Newton sur le corps 2
    s2[0] = s2[0] + (1/2)*F/m2*(dt**2)*vect_grav21[0] + s2[3]
    s2[1] = s2[1] + (1/2)*F/m2*(dt**2)*vect_grav21[1] + s2[4]
    s2[2] = s2[2] + (1/2)*F/m2*(dt**2)*vect_grav21[2] + s2[5]
    
    # ON RECOMMENCE
    # Je crée le vecteur pour avoir la vitesse de l'objet 2
    vect_vit2 = [s2[3],s2[4],s2[5]]
    # J'additionne le vecteur gravité et le vecteur vitesse pour avoir la nouvelle 'inertie' de l'objet
    vect_vit2 = [vect_vit2[0]+vect_grav21[0]*(1/2)*F/m2*(dt**2) ,
                 vect_vit2[1]+vect_grav21[1]*(1/2)*F/m2*(dt**2) ,
                 vect_vit2[2]+vect_grav21[2]*(1/2)*F/m2*(dt**2)]
    # Je change les paramètres de vitesse de l'objet
    s2[3] = vect_vit2[0]
    s2[4] = vect_vit2[1]
    s2[5] = vect_vit2[2]
    # Pareil avec le corps 1
    vect_vit1 = [s1[3],s1[4],s1[5]]
    vect_vit1 = [vect_vit1[0]+vect_grav12[0]*(1/2)*F/m1*(dt**2) ,
                 vect_vit1[1]+vect_grav12[1]*(1/2)*F/m1*(dt**2) ,
                 vect_vit1[2]+vect_grav12[2]*(1/2)*F/m1*(dt**2)]
    s1[3] = vect_vit1[0]
    s1[4] = vect_vit1[1]
    s1[5] = vect_vit1[2]
    
    liste_s1_x.append(s1[0])
    liste_s1_y.append(s1[1])
    liste_s1_z.append(s1[2])
    liste_s2_x.append(s2[0])
    liste_s2_y.append(s2[1])
    liste_s2_z.append(s2[2])
    
    return s1, s2

def animate(i) :
    update_pos(s1, s2)
    vect.set_data([s1[0],s2[0]] , [s1[1],s2[1]])
    vect.set_3d_properties([s1[2],s2[2]])
    direction2.set_data([s2[0],s2[0]+s2[3]*1] , [s2[1],s2[1]+s2[4]*1]) # Le *1 sert de facteur multiplicateur pour mieux voir le vecteur
    direction2.set_3d_properties([s2[2],s2[2]+s2[5]*1])
    corps1.set_data_3d(s1[0] , s1[1] , s1[2])
    corps2.set_data_3d(s2[0] , s2[1] , s2[2])
    traj1.set_data(liste_s1_x[:i] , liste_s1_y[:i])
    traj1.set_3d_properties(liste_s1_z[:i])
    traj2.set_data(liste_s2_x[:i] , liste_s2_y[:i])
    traj2.set_3d_properties(liste_s2_z[:i])
    print("Render :",i+1,'/',frames)
    return vect,

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

vect, = ax.plot([], [], linestyle='dashed', color='red')
direction2, = ax.plot([], [], color='green')
traj1, = ax.plot([], [])
corps1,  = ax.plot3D([], [], [], marker='o', markersize=15, color='purple')
traj2, = ax.plot([], [])
corps2,  = ax.plot3D([], [], [], marker='o', markersize=5, color='blue')

#plt.grid()
taille=2000
ax.set_xlim3d(-taille,taille)
ax.set_ylim3d(-taille,30000)
ax.set_zlim3d(-taille,taille)
ax.view_init(35,35)
ax.set_facecolor('white')
fig.set_facecolor('white')
fig.set_figheight(5)
fig.set_figwidth(8)

ani = animation.FuncAnimation(fig, animate, frames=frames, interval=50, blit=False, repeat=True)
ani.save("C:/Users/matdan/Desktop/Code/Python Phys Sim/gravite3D.gif", writer='pillow', fps=30)
#plt.show()