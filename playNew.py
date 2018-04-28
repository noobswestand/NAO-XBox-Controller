import pygame
from naoqi import ALProxy
import motion
import time
import csv
import os.path
import os 
from shutil import copyfile
from collections import deque


working_directory = os.path.dirname(os.path.realpath(__file__))
file=working_directory+"record.csv"

CurrentLine=0

robotActive=True
dataFile="test.csv"


if (robotActive==True):
	#Connect to Robot
	ip="10.255.14.127"
	mp = ALProxy("ALMotion",ip,9559)
	pFractionMaxSpeed=0.4



pygame.init()
size = [360, 240]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("")
clock = pygame.time.Clock()


def get_last_row(csv_filename):
	with open(csv_filename, 'r') as f:
		try:
			lastrow = deque(csv.reader(f), 1)[0]
		except IndexError:  # empty file
			lastrow = None
		return lastrow


def Play(path):

	dataStep=0
	done=False
	#Main Loop
	while done==False:

		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop


		do=False
		if os.path.isfile(path):
			try:
				copyfile(path, "read.csv")
				print 'Access on file "' + path +'" is available!'
				do=True
			except OSError as e:
				print 'Access-error on file "' + path + '"! \n' + str(e)

		if do==True:
			


			row=get_last_row("read.csv")
			#for row in reader:
				#RightHand,LeftHand,
					#LShoulderRoll,LShoulderPitch,LElbowRoll,LElbowYaw,
					#RShoulderRoll,RShoulderPitch,RElbowRoll,RElbowYaw
			Hands=row[0]
			Hands=Hands[1:]
			Hands=Hands[:-1]
			Hands=(Hands.split())
			Hands[0]=Hands[0][:-1]
			#Hands = [float(i) for i in Hands]
			Hands2 = []
			for item in Hands:
			    Hands2.append(float(item))

			LArm=row[2]
			LArm=LArm[1:]
			LArm=LArm[:-1]
			LArm=(LArm.split())
			for i in range(len(LArm)-1):
				LArm[i]=LArm[i][:-1]

			LArm2 = []
			for item in LArm:
				LArm2.append(float(item))

			

			RArm=row[1]
			RArm=RArm[1:]
			RArm=RArm[:-1]
			RArm=(RArm.split())
			for i in range(len(RArm)-1):
				RArm[i]=RArm[i][:-1]

			RArm2 = []
			for item in RArm:
			    RArm2.append(float(item))


			#data[0].append(Hands2)
			#data[1].append(LArm2)
			#data[2].append(RArm2)


			angles=[Hands2[0],Hands2[1],LArm2[0],LArm2[1],LArm2[2],LArm2[3],LArm2[4],RArm2[0],RArm2[1],RArm2[2],RArm2[3],RArm2[4]]
			angles = [ x * motion.TO_RAD for x in angles]
			moveAll(angles)



			#Delete the file
			#os.remove("read.csv")



		dataStep+=1
		clock.tick(30)#30


def moveAll(angles):
	"""Used to update the robot with all the current angles"""
	if (robotActive==True):
		names=["RHand","LHand","LShoulderRoll","LShoulderPitch","LElbowRoll","LElbowYaw","LWristYaw","RShoulderRoll","RShoulderPitch","RElbowRoll","RElbowYaw","RWristYaw"]
		#names=["RHand","LHand","LShoulderRoll","LShoulderPitch","LElbowRoll","LElbowYaw"]
		mp.post.angleInterpolationWithSpeed(names, angles, pFractionMaxSpeed)



Play(dataFile)