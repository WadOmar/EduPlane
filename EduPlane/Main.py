import pygame
import random
from math import*

# Initialisation de pygame
pygame.init()
pygame.font.init()

# Chargement des polices
police = pygame.font.SysFont('Comic Sans MS', 20)
titreMenu = pygame.font.SysFont("comicsansms",115)
TitreCarburant = pygame.font.SysFont("comicsansms",80)

# Chargement des couleurs
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0, 100, 200)
brightRed = (255,0,0)
brightGreen = (0,255,0)
yellow = (255,255,102)
brightYellow = (255,255,0)
orange = (255,153,51)
brightOrange = (255,128,0)

# Getion d'etoiles
listeEtoiles = []
for iX in range (1000):
	for iY in range (600):
		if random.randint(0,10000) == 1:
			listeEtoiles.append((iX, iY))

# Ceation de la fenetre
fenetre = pygame.display.set_mode( (1000,600) ) # Creation d'une fenetre graphique de taille 1000x600 pixels
pygame.display.set_caption("EduPlain Ralim ~ ISN 2018-2019") # Definit le titre de la fenetre

# Chargement des images
avion = pygame.image.load("images/avion.png")
avion = pygame.transform.rotate(avion, -90)

# Chargement des sons

# Definition des fonctions
def quitterJeu():
	pygame.quit()
	quit()

def checkLeave(): # Permet de gerer un clic sur le bouton de fermeture de la fenetre
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitterJeu()

def bouton(msg,x,y,w,h,ic,ac,action=None): # Permet de faire un bouton cliquable
	souris = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w > souris[0] > x and y+h > souris[1] > y:
		pygame.draw.rect(fenetre, ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(fenetre, ic,(x,y,w,h))

	texteBouton = pygame.font.SysFont("comicsansms",30)
	textSurf = texteBouton.render(msg, True, black)
	textRect = textSurf.get_rect()
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	fenetre.blit(textSurf, textRect)

def clavierEtSouris(): # Gestion du clavier: Quelles touches sont pressees ?
	global yAvion
	clavier = pygame.key.get_pressed()

	if clavier[pygame.K_UP] == True and yAvion >= 10:
		yAvion -= 5
	if clavier[pygame.K_DOWN] == True and yAvion <= 500:
		yAvion += 5
	if clavier[pygame.K_ESCAPE] == True:
		pause()

def deplacementEtoiles():
	global listeEtoiles, vitesse
	for iEtoile in range (len(listeEtoiles)):
		if listeEtoiles[iEtoile][0] > 0:
			listeEtoiles[iEtoile] = (listeEtoiles[iEtoile][0]-vitesse, listeEtoiles[iEtoile][1])
		else:
			listeEtoiles[iEtoile] = (1000, listeEtoiles[iEtoile][1])

def deplacementMissiles():
	global listeMissiles, vitesse

def dessiner():
	global xAvion, yAvion, listeEtoiles, fuel
	fenetre.fill(white)
	for iEtoile in range (len(listeEtoiles)):
		pygame.draw.circle(fenetre, (0,100,55), listeEtoiles[iEtoile], 3)

	nbBarres = fuel // 100
	barres = ""

	for iBarre in range (nbBarres):
		barres = barres + "I"

	fuelDisplay = police.render("Carburant: " + barres, False, black)

	fenetre.blit(fuelDisplay, (10, 0))
	fenetre.blit(avion,(xAvion,yAvion))
	pygame.display.flip()

def gererFuel():
	global fuel, consommation
	fuel -= consommation
	if fuel == 0:
		outOfFuel()

def outOfFuel():
	global perdu
	perdu = True
	while perdu:
		checkLeave()

		TextSurf = TitreCarburant.render("CARBURANT EPUISE", True, black)
		TextRect = TextSurf.get_rect()
		TextRect.center = ((500),(100))

		fenetre.blit(TextSurf, TextRect)

		bouton("Plus de carburant ?",25,450,300,100,green,brightGreen,shopFuel)
		bouton("Quit",675,450,300,100,red,brightRed,quitterJeu)
		bouton("Reessayer",350,450,300,100,orange,brightOrange,game_loop)

		pygame.display.update()
		clock.tick(15)

def moreFuel():
	global fuel, shopFuel
	fuel += 1000
	shopFuel = False

def shopFuel():
	shopFuel = True
	while shopFuel:
		checkLeave()

		fenetre.fill(green)
		TextSurf = titreMenu.render("SHOP D'URGENCE", True, black)
		TextRect = TextSurf.get_rect()
		TextRect.center = ((500),(100))

		bouton("ACHETER! Un full pour 100 balles",400,450,300,50,yellow,brightYellow,moreFuel)

		pygame.display.update()
		clock.tick(15)

def menu():
    global menuV
    menuV = True
    while menuV:

        checkLeave()

        fenetre.fill(blue)
        TextSurf = titreMenu.render("EduPlain Ralim", True, black)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((500),(100))

        fenetre.blit(TextSurf, TextRect)

        bouton("Jouer!",350,200,300,100,green,brightGreen,game_loop)
        bouton("Credits",350, 320, 300, 100, yellow, brightYellow, credits)
        bouton("Quit",350,440,300,100,red,brightRed,quitterJeu)
        bouton("?", 930, 530, 50, 50, orange, brightOrange, aide)

        pygame.display.update()
        clock.tick(15)

def credits():
    global menuV
    menuV = True
    credit = True
    while credit:
        checkLeave()

        fenetre.fill(white)

        TextSurf = titreMenu.render("CREDITS", True, black)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((500), (100))

        fenetre.blit(TextSurf, TextRect)

        bouton("Retour", 350, 450, 300, 100, green, brightGreen, menu)
        pygame.display.update()
        clock.tick(15)

def aide():
    aide = True
    while aide:
        checkLeave()

        fenetre.fill(white)

        TextSurf = titreMenu.render("HELP", True, black)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((500), (100))

        fenetre.blit(TextSurf, TextRect)

        bouton("Retour", 350, 450, 300, 100, green, brightGreen, menu)
        pygame.display.update()
        clock.tick(15)
def pause():
	global enPause
	enPause = True
	while enPause:
		checkLeave()

		TextSurf = titreMenu.render("PAUSE", True, black)
		TextRect = TextSurf.get_rect()
		TextRect.center = ((500),(100))

		fenetre.blit(TextSurf, TextRect)

		bouton("Reprendre",150,450,300,100,green,brightGreen,reprendre)
		bouton("Quit",550,450,300,100,red,brightRed,quitterJeu)

		pygame.display.update()
		clock.tick(15)

def reprendre():
	global enPause
	enPause = False

def game_loop():
	global xAvion, yAvion, vitesse, fuel, consommation
	quitter = False
	xAvion = 400
	yAvion = 300
	fuel = 1000
	consommation = 10
	fenetre.fill(white)
	while not quitter:
		temps = pygame.time.get_ticks()
		vitesse = int(log(temps, 100))
		checkLeave()
		clavierEtSouris()
		dessiner()
		deplacementEtoiles()
		gererFuel()
		pygame.display.update()
		print (vitesse)
		clock.tick(50)

# On cree une nouvelle horloge qui nous permettra de fixer la vitesse de rafraichissement de notre fenetre
clock = pygame.time.Clock()

menu()
pygame.quit()
