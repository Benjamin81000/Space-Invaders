from tkinter import*
from random import randrange

def Tir1(event):
    global Tir , points
    if flag==1:
        tir=can.create_rectangle(Ship[0][1]+1,Ship[0][2]-15,Ship[0][1]-1,Ship[0][2]-45,width=2,outline=Ship[0][3])
        Tir.append([tir,Ship[0][1],Ship[0][2]])
        points-=10 #Réduit le score pour chaque tir effectué

def move():
    #Déplacement du Tir
    global Tir
    for i in range (len(Tir)):
        Tir[i][2] = Tir[i][2]-10
        if(Tir[i][2]>0):
            can.coords(Tir[i][0], Tir[i][1]+1,Tir[i][2]-15, Tir[i][1]-1,Tir[i][2]-45)

    #Supprime les Tirs lorsqu'ils sortent du Canvas
    if Tir[0][2]<0:
        can.delete(Tir[0][0])
        del(Tir[0])

def ajouter_aliens():
    global VitesseTir
    for i in range(nb_ennemi):
        #soit on met dans la liste un alien rouge, soit un alien bleu
        AlienBouR=randrange(0,2)
        if AlienBouR==0:
            alien= can.create_image(50+i*100, 25,image=photo1)
            c = 'red'
        else :
            alien= can.create_image(50+i*100, 25,image=photo2)
            c ='blue'
        #Nous faisons 2 lignes d'aliens
        if i<l//100:
            aliens.append([alien , 50+i*100, 25, vx, c ])
        else :
            aliens.append([alien , 100+(i-l//100)*100, 75, vx, c ])
        #augmente la vitesse du Tir
        if i==12:
            VitesseTir-=10

def depAliens(): # Déplacement des ennemis
    global Atouche, fini
    for i in range (len(aliens)):
        aliens[i][1]=aliens[i][1]+aliens[i][3]
        if aliens[i][1]>l-20:
            aliens[i][2]=aliens[i][2]+50
            aliens[i][1]= 25
        if aliens[i][2]>450:
            fini+=1 #empêche la réapparition d'ennemis
            Atouche += 1
            lose()

def affaliens(): # Affichage des ennemis
    for i in range(len(aliens)):
        can.coords(aliens[i][0], aliens[i][1], aliens[i][2])
        #les ennemis ont de base 1 chance sur 50 de tirer
        chanceDeTirer=randrange(0,VitesseTir)
        if chanceDeTirer==0:
            projalien=can.create_oval(aliens[i][1]+5,aliens[i][2]+5,aliens[i][1]-5,aliens[i][2]-5,fill=aliens[i][4], outline=aliens[i][4])
            projsaliens.append([projalien,aliens[i][1],aliens[i][2],vy,aliens[i][4]])


def depProjectileAlien(): # Déplacement des projectiles ennemis et limites
    #Supprime les Tirs ennemis lorsqu'ils sortent du Canvas
    if len(projsaliens)>0:
        if projsaliens[0][2]>l:
            can.delete(projsaliens[0][0])
            del(projsaliens[0])
    for i in range(len(projsaliens)):
        projsaliens[i][2]=projsaliens[i][2]+projsaliens[i][3]

def affProjectileAlien(): # Affichage des projectiles ennemis
    for i in range(len(projsaliens)):
        can.coords(projsaliens[i][0],projsaliens[i][1]+3,projsaliens[i][2]+3,projsaliens[i][1]-3,projsaliens[i][2]-3)

def collision():
    global points, Tir, aliens, Atouche

    #Tir ennemi sur vaisseau
    Atouche=0
    for i in range (len(projsaliens)):
        if projsaliens[i][1]+3>Ship[0][1]-25 and projsaliens[i][1]-3<Ship[0][1]+25 and projsaliens[i][2]+3>Ship[0][2]-15 and projsaliens[i][2]-3<Ship[0][2]and Ship[0][3] == projsaliens[i][4]:
            Atouche+=1
            lose()

    #Tir allié sur ennemi
    SUPR=False
    #Si le jeu tourne, si il y a des Tirs en cours, si il y a des ennemis
    if flag==1 and len(Tir)>0 and len(aliens)>0:
        for i in range (len(Tir)):
            for j in range (len(aliens)):
                if Tir[i][1]>aliens[j][1]-25 and Tir[i][1]<aliens[j][1]+25 and Tir[i][2]>aliens[j][2] and Tir[i][2]<aliens[j][2]+50 and Ship[0][3] == aliens[j][4] :
                #Supprimme l'alien
                    SUPR=True
                    can.delete(aliens[j][0])
                    del(aliens[j])
                #On supprime également les tirs
                    can.delete(Tir[i][0])
                    del(Tir[i])
                    points+=100
                #Résolution pour que le programme ne plante pas avec le del
                    return SUPR

def switch(event): #changement de couleur
    if flag==1:
        #Supprime le vaisseau actuel
        can.delete(Ship[0][0])

        #Change la couleur du vaisseau et du Tir
        if(Ship[0][3] == 'blue'):
            Ship[0][3] = 'red'
            Ship[0][0] = can.create_image(Ship[0][1],Ship[0][2],image=photo)
        else:
            Ship[0][3] = 'blue'
            Ship[0][0] = can.create_image(Ship[0][1],Ship[0][2],image=photo4)

def avance(gd, hb, i):
    #bloque le vaisseau dans le Canvas
    if(Ship[i][1] +gd< l-20 and Ship[i][1] +gd>0+20 and Ship[i][2] +hb< l-40 and Ship[i][2] +hb> 0 and flag==1):
        Ship[i][1] = Ship[i][1] +gd
        Ship[i][2] = Ship[i][2] +hb
        can.coords(Ship[i][0],Ship[i][1],Ship[i][2])

#Déplacement du vaisseau
def gauche(event):
    avance(-20,0,0)
def droite(event):
    avance(20, 0,0)
def haut(event):
    avance(0, -20,0)
def bas(event):
    avance(0, 20,0)

def Nettoyer():
    global can, photo2, photo1,photo,flag,Points,points,photo3, photo4, fondjeu
    #Enlève le menu pour lancer le jeu
    for c in fenetre.winfo_children():
        c.destroy()

    # Définition du Canvas
    can = Canvas(fenetre, width =l, height =l-30, bg='black')
    fondjeu= PhotoImage(file ='Fond.gif')
    photo3= PhotoImage(file='lose.gif')
    photo2= PhotoImage(file ='ennemi1.png')
    photo1= PhotoImage(file ='ennemi.png')
    photo = PhotoImage(file ='Ship.png')
    photo4= PhotoImage(file ='Ship2.png')
    fond = can.create_image(l/2,l/2,image=fondjeu)
    Ship[0][0] = can.create_image(x,y,image=photo4)
    can.pack(side=TOP)
    bouton1=Button(fenetre, text="Retourner au Menu", command=Nettoyer1)
    bouton1.pack(side=BOTTOM)
    Points=can.create_text((60,l-40), text=points, fill='white')
    Score_text=can.create_text((25,l-40), text='Score =', fill='white')

    #pour ne pas faire réapparaitre les ennemis lors du rappel de la fonction ok()
    if flag==0:
        flag=1
        ajouter_aliens()

    #Réinitialise les points
    points = 0

    #Lancement du jeu
    ok()

def ok():
    global Points, nb_ennemi

    if flag==1:
        depAliens()
        affaliens()
        depProjectileAlien()
        affProjectileAlien()
        collision()
        if (len (aliens))==0 and fini==0:
            if nb_ennemi <= (l//100)*2 :
                nb_ennemi+=1
            ajouter_aliens()
        if (len(Tir))>0:
            move()
        can.itemconfigure(Points, text=points)
        fenetre.after(20,ok)


def pause(event): # Appuyer sur "p" met le jeu en pause
    global flag
    if flag==1:
        flag=0
    else:
        flag=1
        ok()


def Nettoyer2():
    for c in fenetre.winfo_children():
        c.destroy()
    hight()

def lose():
    #Lorsque un vaisseau ennemi atteint les 3/4 du canvas
    #ou que le vaisseau allié est touché
    global projsaliens, aliens, Tir, Ship, end, end1, flag, nom, hightScore

    #met le jeu en pause
    if flag==1:
        flag=0

    #Rentre le score dans le HightScore et le classe dans l'ordre de grandeur
    it = True
    for i in range(len(hightScore)):
        if points>hightScore[i] and it:
            if i == 0:
                hightScore[i+2] = hightScore[i+1]
            if i < 2:
                hightScore[i+1] = hightScore[i]
            hightScore[i]=points
            it = False

    #Affiche l'image si on a perdu
    if Atouche==1:
        end = can.create_image(l/2, l/2, image=photo3)
        end1=1

    #Réinitialise les listes
    if (len(projsaliens))>0:
        projsaliens=[]
    if (len(aliens))>0:
        aliens=[]
    if (len(Tir))>0:
        Tir=[]
    Ship =[[0,x,y,coul]]

def hight():
    global fondClassement, end1
    end1=0 #évite le problème de canvas avec l'image du end

    can = Canvas(fenetre, width =l, height=l-30, bg='black')
    can.pack(side=TOP)
    fondClassement= PhotoImage(file ='Fond_class.gif')
    fond = can.create_image(l/2,l/2,image=fondClassement)
    Score_text=can.create_text((l/2+50,50), text='CLASSEMENT', font="Arial 40 italic", fill='white')
    for i in range (len(hightScore)):
        label3=Label(fenetre,font="Arial 40 italic", text="" +str(hightScore[i]))
        label3.place(x=l/2, y=l/4+100*i)
    bouton1=Button(fenetre, text="Retourner au Menu", command=Nettoyer1)
    bouton1.pack(side=BOTTOM)


def Aide():
    #Tutoriel sur le fonctionnement des différentes touches utilisées
    label1=Label(fenetre, text="Pour tirer avec le vaisseau, cliquer sur la touche 'A'")
    label2=Label(fenetre, text="Pour déplacer le vaisseau, utiliser les flèches directionnelles")
    label3=Label(fenetre, text="Pour mettre le jeu sur pause, appuyer sur la touche 'P'")
    label4=Label(fenetre, text="Pour changer de couleur, appuyer sur la barre espace")
    label3.place(x=l/2-100, y=l/2-40)
    label1.place(x=l/2-100, y=l/2-20)
    label2.place(x=l/2-100, y=l/2)
    label4.place(x=l/2-100, y=l/2+20)

def Nettoyer1(): #Nettoie le canvas
    global Ship, flag, nb_ennemi
    #On remet le nombre d'aliens à la normale
    nb_ennemi=l//100

    if flag==1:
        flag=0

    if end1==1:
        can.delete(end)

    #renvoie vers lose() pour réinitialiser les listes
    if Atouche==0:
        lose()

    for c in fenetre.winfo_children():
        c.destroy()
    MenuPrinc()

def MenuPrinc():
    global fond, points

    fond = PhotoImage(file="Fond_ecran.gif")
    fond1=Label(fenetre, image=fond)
    fond1.grid(row=1, column=1, rowspan=10, columnspan=10)
    barre_menu = Menu(fenetre)
    fenetre['menu'] = barre_menu

    sousMenu = Menu(barre_menu)
    barre_menu.add_cascade(label='Options', menu=sousMenu)
    sousMenu.add_command(label='Commandes', command=Aide)
    bouton=Button(fenetre, text="Lancer le jeu", command=Nettoyer)
    bouton.place(x=l/2-100, y=l/2-100, width=200, height=50)
    Bclassement=Button(fenetre, text="High Score", command=Nettoyer2)
    Bclassement.place(x=l/2-100, y=l/2+50, width=200, height=50)

    #Empêche le score de s'afficher plusieurs fois dans le classement
    points=0


#Variable à définir
l=600
nb_ennemi=l//100 #Nombre d'ennemis dans le canvas
points = 0
hightScore=[0,0,0]


aliens=[]
vx,vy = 5,5 # Valeurs de déplacements
flag=0
projsaliens=[]
VitesseTir=50

#x et y sont la position du vaisseau
x=l/2
y=l-l/20-30
coul = 'blue'
Ship =[[0,x,y,coul]]
Tir = []


fenetre = Tk()
fenetre.geometry("600x600")
fenetre.title("Switch Invaders @DAWAE")


end1=0 #Permet de savoir si le jeu s'est terminé
Atouche=0
fini=0

MenuPrinc()

fenetre.bind("<Left>",gauche)
fenetre.bind("<Right>",droite)
fenetre.bind("<Up>",haut)
fenetre.bind("<Down>",bas)
fenetre.bind("a",Tir1)
fenetre.bind("<p>", pause)
fenetre.bind("<space>",switch)

fenetre.mainloop()
