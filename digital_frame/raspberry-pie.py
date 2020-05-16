## Import libraries 

import math,random,pygame,sys


## Set up class for main game variables

class Game():
	def __init__(self):
		self.score=0
		self.raspberryCount=0


## Set up class for the player's turret

class Turret(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("turret.png")
		self.rect = self.image.get_rect()
		self.rect.x = 240; self.rect.y = 630


## Set up method to enable the player's turret to move
        
	def moveMe(self,direction):
		if direction=="left" and self.rect.x>5:
			self.rect.x-=5
		if direction=="right" and self.rect.x<(480-self.rect.width):
			self.rect.x+=5


## Set up class for bullets

class Bullet(pygame.sprite.Sprite):
	def __init__(self,turret):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("bullet.png")
		self.rect=self.image.get_rect()
		self.rect.x=turret.rect.x+(turret.rect.width/2)-(self.rect.width/2)
		self.rect.y=turret.rect.y-turret.rect.height

## Set up method to move bullets up the screen

	def updatePosition(self):
		if self.rect.y>0-self.rect.height:
			self.rect.y-=5
		else:
			self.kill()


## Set up class for fruit

class Fruit(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.genus=random.randint(1,3) 
		if self.genus==1: imagefile="raspberry"
		if self.genus==2: imagefile="strawberry"
		if self.genus==3: imagefile="cherry"
		self.image=pygame.image.load(imagefile+".png")
		self.image=pygame.transform.rotate(self.image,-15+random.randint(0,20))
		self.rect=self.image.get_rect()
		self.rect.y=-0-self.rect.height
		self.rect.x=(random.randint(2,44)*10)


## Set up method to enable fruit to fall down the screen

	def updatePosition(self,game):
		if self.rect.y<640:
			self.rect.y+=3
		else:
			if self.genus==1:
				game.score+=10
				game.raspberryCount+=1	
			else:
				game.score-=50
			self.kill()

## Set up method to update score and remove fruit when shot

	def shot(self,game):
		if self.genus==1:
			game.score-=50
		else:
			game.score+=10
		self.kill()


## Initialise the game

pygame.init()
pygame.key.set_repeat(1, 20)
scoreFont=pygame.font.Font(None,17)
statusFont=pygame.font.Font(None,17)
black=(0,0,0)
screen=pygame.display.set_mode([480, 640])
pygame.display.set_caption('Raspberry Pie')


## Create initial object instances

game=Game()
turret=Turret()
sprites=pygame.sprite.Group()
sprites.add(turret)
fruits=pygame.sprite.Group()
bullets=pygame.sprite.Group()


## Initialise game over flag and timer

end_game=False
clock=pygame.time.Clock()
tock=0


## Main loop starts here

while end_game!=True:
	clock.tick(30) 
	tock+=1
	screen.fill(black)
    

## Process events

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_LEFT:
				turret.moveMe("left")
			if event.key==pygame.K_RIGHT:
				turret.moveMe("right")
			if event.key==pygame.K_SPACE:
				bullet=Bullet(turret)
				bullets.add(bullet)


## Move objects

	for bullet in bullets:
		bullet.updatePosition()

	for fruit in fruits:
		fruit.updatePosition(game)


## Add new fruit if 2 seconds has elapsed

	if tock>60: 
		if len(fruits)<10:
			fruit=Fruit()
			fruits.add(fruit)
		tock=0


## Check for collisions

	collisions=pygame.sprite.groupcollide(fruits,bullets,False,True)
	if collisions: 
		for fruit in collisions:
			fruit.shot(game)


## Update player score

	scoreText=scoreFont.render('Score:'+str(game.score),True,(255,255,255),(0,0,0))
	screen.blit(scoreText,(0,620))
	statusText=statusFont.render('Raspberries:'+str(10-game.raspberryCount),True,(255,210,210),(0,0,0))
	screen.blit(statusText,(0,10))


## Update the screen and check for game over

	sprites.draw(screen); bullets.draw(screen); fruits.draw(screen)
	pygame.display.flip()
	if game.raspberryCount>=10: 
		end_game=True


## Game over: display the player's final score

scoreBadge=pygame.image.load("scoreframe.png")
scoreBadge.convert_alpha()
left=90;top=250
screen.blit(scoreBadge,(left,top))
scoreFont=pygame.font.Font(None,52)
statusText=scoreFont.render('Your Score:'+str(game.score),True,(0,0,0),(231,230,33))
screen.blit(statusText,(105,300))
pygame.display.flip() 

## Wait for the player to close the game window

while True: 
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
