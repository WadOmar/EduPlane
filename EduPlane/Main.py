import pygame
import random
from math import*

# Initialisation de pygame
pygame.init()
pygame.font.init()

# Chargement des polices
police = pygame.font.SysFont('Comic Sans MS', 20)
titreMenu = pygame.font.SysFont("comicsansms",115)

# Chargement des couleurs
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0, 100, 200)
brightRed = (255,0,0)
brightGreen = (0,255,0)

# Génération d'étoiles
listeEtoiles = []
for iX in range (1000):
	for iY in range (600):
		if random.randint(0,10000) == 1:
			listeEtoiles.append((iX, iY))
			
# Création de la fenetre
fenetre = pygame.display.set_mode( (1000,600) ) # Création d'une fenêtre graphique de taille 1000x600 pixels
pygame.display.set_caption("EduPlain Ralim ~ ISN 2018-2019") # Définit le titre de la fenêtre

# Chargement des images
avion = pygame.image.load("images/avion.png")
avion = pygame.transform.rotate(avion, -90)

# Chargement des sons

# Définition des fonctions
def quitterJeu():
	pygame.quit()
	quit()
	
def checkLeave(): # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
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
	
	texteBouton = pygame.font.SysFont("comicsansms",20)
	textSurf = texteBouton.render(msg, True, black)
	textRect = textSurf.get_rect()
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	fenetre.blit(textSurf, textRect)

def clavierEtSouris(): # Gestion du clavier: Quelles touches sont pressées ?
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
			listeEtoiles[iEtoile] = (listeEtoiles[iEtoile][0]-int(vitesse * 1.5), listeEtoiles[iEtoile][1])
		else:
			listeEtoiles[iEtoile] = (1000, listeEtoiles[iEtoile][1])
			
def dessiner():
	global xAvion, yAvion, listeEtoiles
	fenetre.fill(white)
	for iEtoile in range (len(listeEtoiles)):
		pygame.draw.circle(fenetre, (0,100,55), listeEtoiles[iEtoile], 3)
	fenetre.blit(avion,(xAvion,yAvion))

def menu():
	menu = True
	while menu:
		checkLeave()
		
		fenetre.fill(blue)
		TextSurf = titreMenu.render("EduPlain Ralim", True, black)
		TextRect = TextSurf.get_rect()
		TextRect.center = ((500),(100))
		
		fenetre.blit(TextSurf, TextRect)

		bouton("GO!",400,450,100,50,green,brightGreen,game_loop)
		bouton("Quit",600,450,100,50,red,brightRed,quitterJeu)
		
		fenetre.blit(avion, (500, 300))
		
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

		bouton("Reprendre",400,450,100,50,green,brightGreen,reprendre)
		bouton("Quit",600,450,100,50,red,brightRed,quitterJeu)
		
		pygame.display.update()
		clock.tick(15)

def reprendre():
	global enPause
	enPause = False
	
def game_loop():
	global xAvion, yAvion, vitesse
	quitter = False
	xAvion = 400
	yAvion = 300
	fenetre.fill(white)
	while not quitter:
		temps = pygame.time.get_ticks()
		vitesse = int (log(temps, 100))
		checkLeave()
		clavierEtSouris()
		dessiner()
		deplacementEtoiles()
		pygame.display.update()
		print (vitesse)
		clock.tick(50)
	
# On crée une nouvelle horloge qui nous permettra de fixer la vitesse de rafraichissement de notre fenêtre
clock = pygame.time.Clock()

menu()
game_loop()
pygame.quit()