import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Constantes
# G en m3 kg-1 s-2
G = 6.674*(10**(-11))
# dt donc échelle de temps (un grand dt fait passer le temps plus vite)
dt = 10000000
# Nombre de frames pour le rendu
frames = 1000

# VECTEURS S : [x , y , Vx , Vy]
# Corps 1
m1 = 10000
s1 = [0,0,30,0]
liste_s1_x = []  # Liste qui servent à tracer le trajet du corps
liste_s1_y = []
liste_s1_x.append(s1[0])
liste_s1_y.append(s1[1])
# Corps 2
m2 = 1
s2 = [500,3500,130,0]
liste_s2_x = []  # Liste qui servent à tracer le trajet du corps
liste_s2_y = []
liste_s2_x.append(s2[0])
liste_s2_y.append(s2[1])

# Calcul de la force de gravitation (en N)
def Fab(ma, mb, d) :
    return G*ma*mb/(d**2)

# Calcul de la distance entre 2 corps (en m)
def d(sa, sb) :
    return np.sqrt((sb[1]-sa[1])**2 + (sb[0]-sa[0])**2)

# Calcul des composantes du vecteur qui sépare 2 objets (divisé par la distance pour le normer)
def vecteur_AB(A, B) :
    return [ B[0]-A[0] , B[1]-A[1] ] / d(A,B)

# Fonction qui met à jours les positions à chaque itération en calculant les forces, vitesses, positions
def update_pos(s1, s2) :
    
    distance = d(s1, s2)
    #print("Distance Terre -> Soleil :",distance)
    F = Fab(m1, m2, distance)
    
    # Permet de récupérer l'orientation de la force de gravité pour l'appliquer dans la bonne direction
    vect_grav12 = vecteur_AB(s1,s2)
    vect_grav21 = vecteur_AB(s2,s1)
    
    # BRAINSTORM POUR CORRIGER LA TRAJECTOIRE DE L'OBJET QUAND IL A UNE VITESSE INITIALE
    # Il faut récupérer le vecteur et changer son orientation
    # Soit je le met normal au vecteur gravité mais ça a pas trop de sens ?
    # je l'additionne au vecteur gravité pour avoir sa nouvelle direction ?
    # EST - CE QUE JE FAIS LA TRANSFORMATION AVANT OU APRES AVOIR APPLIQUE LA 2EME LDN ?
    
    '''
    vect_vit2 = vecteur_vitesse(s2)
    vect_vit2 = [vect_vit2[0]+vect_grav21[0] , vect_vit2[1]+vect_grav21[1]]
    vect_vit2 = vect_vit2 / np.sqrt(vect_vit2[0]**2 + vect_vit2[1]**2)
    print(vect_vit2)
    '''
    
    # Application de la deuxième loi de Newton sur le corps 1
    s1[0] = s1[0] + (1/2)*F/m1*(dt**2)*vect_grav12[0] + s1[2]
    s1[1] = s1[1] + (1/2)*F/m1*(dt**2)*vect_grav12[1] + s1[3]
    
    # Application de la deuxième loi de Newton sur le corps 2
    s2[0] = s2[0] + (1/2)*F/m2*(dt**2)*vect_grav21[0] + s2[2]
    s2[1] = s2[1] + (1/2)*F/m2*(dt**2)*vect_grav21[1] + s2[3]
    
    '''
    # TENTATIVE DE LE METTRE NORMAL AU VECTEUR GRAVITE
    # Je crée le vecteur pour avoir la vitesse de l'objet 2
    vect_vit2 = [s2[2],s2[3]]
    # Je récupère la norme du vecteur 2 pour connaître la vitesse de l'objet
    norme_vect_vit2 = np.sqrt(vect_vit2[0]**2 + vect_vit2[1]**2)
    # J'additionne le vecteur gravité et le vecteur vitesse pour avoir la direction de la nouvelle 'inertie' de l'objet
    vect_vit2 = [vect_vit2[0]+vect_grav21[0] , vect_vit2[1]+vect_grav21[1]]
    # Je normalise ce vecteur et je le multiplie par la norme originale afin de retrouver la vitesse d'origine
    vect_vit2 = vect_vit2/np.sqrt(vect_vit2[0]**2 + vect_vit2[1]**2)*norme_vect_vit2
    # Je change les paramètres de vitesse de l'objet
    s2[2] = vect_vit2[0]
    s2[3] = vect_vit2[1]
    
    # COPIE DE TOUT CA POUR LE CORPS 1
    vect_vit1 = [s1[2],s1[3]]
    norme_vect_vit1 = np.sqrt(vect_vit1[0]**2 + vect_vit1[1]**2)
    vect_vit1 = [vect_vit1[0]+vect_grav12[0] , vect_vit1[1]+vect_grav12[1]]
    vect_vit1 = vect_vit1/np.sqrt(vect_vit1[0]**2 + vect_vit1[1]**2)*norme_vect_vit1
    s1[2] = vect_vit1[0]
    s1[3] = vect_vit1[1]
    '''
    
    # ENFAIT C'EST TOUT FAUX, JE DIS QUE LA VITESSE EST CONSTANTE
    # CE QUI EST VRAIMENT PAS VRAI
    # Je devrai raisonner en conservation de l'énergie ? (Potentielle + cinétique)
    # OU ALORS JE REPASSE PAS PAR LA NORMALISATION
    # Faudrait peut etre reflechir juste en vecteur vu que ça me donne une vitesse en m/s
    
    # ON RECOMMENCE
    # Je crée le vecteur pour avoir la vitesse de l'objet 2
    vect_vit2 = [s2[2],s2[3]]
    # J'additionne le vecteur gravité et le vecteur vitesse pour avoir la nouvelle 'inertie' de l'objet
    vect_vit2 = [vect_vit2[0]+vect_grav21[0]*(1/2)*F/m2*(dt**2) , vect_vit2[1]+vect_grav21[1]*(1/2)*F/m2*(dt**2)]
    # Je change les paramètres de vitesse de l'objet
    s2[2] = vect_vit2[0]
    s2[3] = vect_vit2[1]
    # Pareil avec le corps 1
    vect_vit1 = [s1[2],s1[3]]
    vect_vit1 = [vect_vit1[0]+vect_grav12[0]*(1/2)*F/m1*(dt**2) , vect_vit1[1]+vect_grav12[1]*(1/2)*F/m1*(dt**2)]
    s1[2] = vect_vit1[0]
    s1[3] = vect_vit1[1]
    
    liste_s1_x.append(s1[0])
    liste_s1_y.append(s1[1])
    liste_s2_x.append(s2[0])
    liste_s2_y.append(s2[1])
    
    return s1, s2

# Bloc qui sert juste à print des infos pour quand je code, pas important
'''
distance = d(s1,s2)
print(distance)
Force = Fab(m1,m2,d(s1,s2))
print(Force)
vecteur12 = vecteur_AB(s1,s2)
vecteur21 = vecteur_AB(s2,s1)
print(vecteur12)
print(vecteur21)
'''

def animate(i) :
    update_pos(s1, s2)
    vect.set_data([s1[0],s2[0]],[s1[1],s2[1]])
    direction2.set_data([s2[0],s2[0]+s2[2]*1],[s2[1],s2[1]+s2[3]*1])
    corps1.set_data(s1[0],s1[1])
    corps2.set_data(s2[0],s2[1])
    traj1.set_data(liste_s1_x[:i],liste_s1_y[:i])
    traj2.set_data(liste_s2_x[:i],liste_s2_y[:i])
    print("Render :",i+1,'/',frames)
    return vect,

fig, ax = plt.subplots(1)

vect, = ax.plot([], [], linestyle='dashed', color='red')
direction2, = ax.plot([], [], color='green')
traj1, = ax.plot([], [])
corps1,  = ax.plot([], [], marker='o', markersize=15, color='purple')
traj2, = ax.plot([], [])
corps2,  = ax.plot([], [], marker='o', markersize=5, color='blue')

plt.grid()
plt.xlim(-5000,50000)
plt.ylim(-5000,5000)
ax.set_facecolor('white')
fig.set_facecolor('white')
fig.set_figheight(5)
fig.set_figwidth(8)

ani = animation.FuncAnimation(fig, animate, frames=frames, interval=50, blit=True, repeat=False)
ani.save("C:/Users/matdan/Desktop/Code/Python Phys Sim/gravite.gif", writer='pillow', fps=30)