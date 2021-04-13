# Importations des fonctions nécessaires
from PIL import ImageTk, Image
from tkinter import *
from random import randrange

# Définition du canvas (espace de jeu)

fen1 = Tk()
fen1.title("SNAKE")
can1 = Canvas(fen1, width=500, height=300, bg="light blue")

# Les images
burger = PhotoImage(file='./burger.png')
head = PhotoImage(file='./head.png')
body = PhotoImage(file='./body.png')

# Déclarations des fonctions
# Cette fonction permet de réinitialiser le jeu


def new_game():
    global dx, dy, x, y, eat, flag, serpent, coord_serpent, direction, score, f, flag2

    flag2 = 0

    can1.delete(ALL)

    can1.create_rectangle(0, 0, 10, 300, fill="black")
    can1.create_rectangle(0, 0, 500, 10, fill="black")
    can1.create_rectangle(490, 0, 500, 300, fill="black")
    can1.create_rectangle(0, 300, 500, 290, fill="black")

    coord_serpent = [50, 60]

    serpent = [can1.create_image(
        coord_serpent[0], coord_serpent[1], image=head)]
    eat = 0

    x = randrange(20, 470, 10)
    y = randrange(20, 270, 10)
    f = can1.create_image(x, y, image=burger)

    dx = 10
    dy = 0
    direction = 2
    score = 0

    if flag == 0:
        flag = 1
        move()

# Cette fonction permet d'effectuer une pause en cours de partie


def pause(event):
    global flag, pause, flag2
    if flag2 != 1:
        if flag == 1:
            pause = can1.create_text(
                250, 150, font=('Fixedsys', 18), text="PAUSE")
            flag = 0
        elif flag == 0:
            flag = 1
            can1.delete(pause)
            move()

# Cette fonction va permettre de mettre le serpent en mouvement de manière automatique


def move():
    global dx, dy, x, y, eat, flag, f, serpent, coord_serpent, direction, score, flag2

    # Si le serpent mange une proie on rajoute un body et cela
    # en fonction de la direction afin que le nouveau carré soit bien
    # dessiné à la suite du dernier body composant le serpent

    if (coord_serpent[0] >= x and coord_serpent[0] <= x+20) and (coord_serpent[1] >= y and coord_serpent[1] <= y+10):
        can1.delete(f)
        eat = 1
        coord = len(coord_serpent)
        score = score+100
        # LEFT
        if direction == 1:

            x1 = coord_serpent[coord-2]
            y1 = coord_serpent[coord-1]
            x1 = x1+10

            coord_serpent.append(x1)
            coord_serpent.append(y1)

            serpent.append(can1.create_image(x1, y1, image=body))

        # RIGHT
        elif direction == 2:

            x1 = coord_serpent[coord-2]
            y1 = coord_serpent[coord-1]

            x1 = x1-10

            coord_serpent.append(x1)
            coord_serpent.append(y1)

            serpent.append(can1.create_image(x1, y1, image=body))

        # UP
        elif direction == 3:

            x1 = coord_serpent[coord-2]
            y1 = coord_serpent[coord-1]

            y1 = y1+10

            coord_serpent.append(x1)
            coord_serpent.append(y1)

            serpent.append(can1.create_image(x1, y1, image=body))

        # DOWN
        elif direction == 4:

            x1 = coord_serpent[coord-2]
            y1 = coord_serpent[coord-1]

            coord_serpent.append(x1)
            coord_serpent.append(y1)

            # On rajoute un nouveau body dans notre liste serpent
            serpent.append(can1.create_image(x1, y1, image=body))

    food()

    # Les coordonnées de chaque carré prendront les coordonnées du carré qui le succède
    # cela permettra à chacun des carré de se suivre et d'obtenir l'effet du serpent
    i = 2
    j = 1

    while j < len(serpent):
        coord_serpent[len(coord_serpent)-(i)
                      ] = coord_serpent[len(coord_serpent)-(i+2)]
        coord_serpent[len(coord_serpent)-(i-1)
                      ] = coord_serpent[len(coord_serpent)-(i+1)]
        i += 2
        j += 1

    # On fait avancé le serpent
    coord_serpent[0] = coord_serpent[0]+dx
    coord_serpent[1] = coord_serpent[1]+dy

    i = 2
    j = 1

    # Si le serpent touche le mur la partie s'arrête
    if coord_serpent[0] >= 490 or coord_serpent[0] <= 0 or coord_serpent[1] >= 290 or coord_serpent[1] <= 0:
        flag = 0
        flag2 = 1
        perdu = can1.create_text(250, 150, font=(
            'Fixedsys', 18), text="Score : "+str(score))

    # Si les coordonnées de la tête sont égales aux coordonnées d'un des "body" composant le serpent
    # cela signifie qu'il s'est recoupé par conséquent la partie s'arrête
    while j < len(serpent):
        if coord_serpent[0] == coord_serpent[i] and coord_serpent[1] == coord_serpent[i+1]:
            flag = 0
            flag2 = 1
            perdu = can1.create_text(250, 150, font=(
                'Fixedsys', 18), text="Score : "+str(score))
        i += 2
        j += 1

    i = 0
    j = 0

    # On redéfinie les coordonnées de chacun des "body" composant le corps du serpent
    if flag != 0:
        while j < len(serpent):
            can1.coords(serpent[j], coord_serpent[i], coord_serpent[i+1])

            i += 2
            j += 1

    if flag > 0:
        fen1.after(50, move)

# La fonction food va permettre de générer au hasard de la nourriture dans le canvas


def food():
    global eat, x, y, f, coord_serpent
    if eat == 1:
        x = randrange(20, 470, 10)
        y = randrange(20, 270, 10)
        i = 0
        i2 = 0

        # Afin d'éviter de générer de la nourriture sur le serpent
        # j'utilise ce bout de code qui s'occupera de générer un nouveau burger
        # si les coordonnées du précédent sont égales aux coordonnées d'un carré composant
        # le corps du serpent

        while i < len(coord_serpent):
            i2 = 1
            if x == coord_serpent[i] and y == coord_serpent[i+1]:
                while x == coord_serpent[i] and y == coord_serpent[i+1]:
                    x = randrange(10, 480, 10)
                    y = randrange(10, 280, 10)
                i = 0
                i2 = 0
            if i2 == 1:
                i += 4
        f = can1.create_image(x, y, image=burger)
        eat = 0

# Les fonctions left, right, up et down vont permettrent de contrôler le serpent à l'aide des touches fléchées du clavier


def left(event):
    global dx, dy, direction, coord_serpent
    if direction != 2:
        dx = -10
        dy = 0
        direction = 1


def right(event):
    global dx, dy, direction
    if direction != 1:
        dx = 10
        dy = 0
        direction = 2


def up(event):
    global dx, dy, direction
    if direction != 4:
        dx = 0
        dy = -10
        direction = 3


def down(event):
    global dx, dy, direction
    if direction != 3:
        dx = 0
        dy = 10
        direction = 4

# Programme principal


# Définition des touches qui permettront de déplacer le serpent
can1.bind_all("<Left>", left)
can1.bind_all("<Right>", right)
can1.bind_all("<Up>", up)
can1.bind_all("<Down>", down)
can1.bind_all("<p>", pause)

can1.grid(row=0, column=0, rowspan=10)


# On crée le bouton New game qui va permettre de réinitialiser la partie

Button(fen1, text="New game", font=("Fixedsys"), command=new_game).grid(
    row=4, column=1, sticky=N, padx=5)
Button(fen1, text="Quit", font=("Fixedsys"),
       command=fen1.destroy).grid(row=6, column=1, sticky=N)

# Création des murs (que le serpent ne doit passer dépasser le mur)

can1.create_rectangle(0, 0, 10, 300, fill="black")
can1.create_rectangle(0, 0, 500, 10, fill="black")
can1.create_rectangle(490, 0, 500, 300, fill="black")
can1.create_rectangle(0, 300, 500, 290, fill="black")

# Liste des coordonnées du serpent

coord_serpent = [50, 60]

# Définition des coordonnées de départ du serpent

serpent = [can1.create_image(coord_serpent[0], coord_serpent[1], image=head)]

# Définition du drapeau ( indicateur permettant d'arrêter le programme )
flag = 1
eat = 0

# On dessine le 1er burger
x = randrange(20, 470, 10)
y = randrange(20, 270, 10)
f = can1.create_image(x, y, image=burger)

# Définition des pas d'avancement du serpent
dx = 10
dy = 0

# Etant donné que le serpent avance vers la droite on assigne 2 à direction qui correspond à la fonction right()

direction = 2

# Le compteur de score

score = 0
pause = 0

# Ce compteur va permettre de ne pas remettre le jeu en route
# à l'aide de la touche pause dans le cas où le joueur aurait perdu

flag2 = 0

move()

fen1.mainloop()
