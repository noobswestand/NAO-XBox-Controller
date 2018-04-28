#pip install pygame
#pip install webcolors
import pygame
import webcolors
from naoqi import ALProxy
import motion
import Record
import time
import os.path


robotActive=True#If the robot is on
RecordPlayMode=0#0=Nothing 1=Record 2=Play

pygame.init()
size = [360, 240]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("")


if (robotActive==True):
	#Connect to Robot
	ip="10.255.3.33"
	mp = ALProxy("ALMotion",ip,9559)
	pp = ALProxy("ALRobotPosture", ip, 9559)
	led = ALProxy("ALLeds",ip,9559)
	pFractionMaxSpeed=0.4
	mp.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])



woke=mp.robotIsWakeUp()

#globalVars
joystick_number=0	#The number of the joystick (0,1,2...)

pygame.joystick.init()
joystick = pygame.joystick.Joystick(joystick_number)
joystick.init()

joystick_name = joystick.get_name()
print joystick_name
clock = pygame.time.Clock()


#ROBOT VARIABLS
RArmDefault=[-7,75,15,50,0]
RArm=[-7,75,15,50,0]
LArmDefault=[7,75,-15,-50,0]
LArm=[7,75,-15,-50,0]
Hands=[15,15]
HandsDefault=[15,15]


dataFile="test.csv"
data = [[] for i in range(3)]
dataStep=0
dataLoad=False



def resetPosture():
	for i in range(len(RArmDefault)):
		RArm[i]=RArmDefault[i]
		LArm[i]=LArmDefault[i]
	for i in range(len(HandsDefault)):
		Hands[i]=HandsDefault[i]

def move(names,angles):
	"""Main function to tell the robot to move"""
	if (robotActive==True and RecordPlayMode!=2):
		mp.post.angleInterpolationWithSpeed(names, angles, pFractionMaxSpeed)

def moveAll(angles):
	"""Used to update the robot with all the current angles"""
	if (robotActive==True):
		names=["RHand","LHand","LShoulderRoll","LShoulderPitch","LElbowRoll","LElbowYaw","LWristYaw","RShoulderRoll","RShoulderPitch","RElbowRoll","RElbowYaw","RWristYaw"]
		#names=["RHand","LHand","LShoulderRoll","LShoulderPitch","LElbowRoll","LElbowYaw"]
		mp.post.angleInterpolationWithSpeed(names, angles, pFractionMaxSpeed)


def LegMovement():
	hat = joystick.get_hat(0)
	rl=hat[0]
	ud=hat[1]

	X = 0.0
	Y = 0.0
	Theta = 0.0
	Frequency=0.0
	#Move forward  ;-;
	if ud==1:
		X = 0.5
	if ud==-1:
		X = -0.5

	if ud!=0:
		mp.setWalkTargetVelocity(X, Y, Theta, Frequency)
		time.sleep(2.0)
		mp.setWalkTargetVelocity(0, 0, 0,0)




def HandMovement():
	"""Controls both hands (open/closed)"""
	#get triggers
	RTopTrigger = joystick.get_button( 5 )
	LTopTrigger = joystick.get_button( 4 )
	if (not RTopTrigger):
		JointNames = ["RHand"]
		Angles = [0]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
		Hands[0]=HandsDefault[0]
	else:
		JointNames = ["RHand"]
		Angles = [90]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
		Hands[0]=90
	if (not LTopTrigger):
		JointNames = ["LHand"]
		Angles = [0]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
		Hands[1]=HandsDefault[1]
	else:
		JointNames = ["LHand"]
		Angles = [90]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
		Hands[1]=90
	

def LeftArmMovement():
	"""Controls everything about the LEFT arm"""
	#Get joysticks
	axis=[]
	axes = joystick.get_numaxes()
	for i in range(axes):
		axis.append(joystick.get_axis(i))

	ButtonY=joystick.get_button(3)
	ButtonX=joystick.get_button(2)
	if (axis[2]>0.2 and ButtonY==False and ButtonX==False):
		#Left Shoulder
		if abs(axis[0])>0.35:
			LArm[0]+=axis[0]*5
		if abs(axis[1])>0.2:
			LArm[1]+=axis[1]*5
		JointNames = ["LShoulderRoll","LShoulderPitch"]
		Angles = [LArm[0],LArm[1]]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
	else:
		LArm[0]=LArmDefault[0]
		LArm[1]=LArmDefault[1]

	if (axis[2]>0.2 and ButtonY==True and ButtonX==False):
		if abs(axis[1])>0.35:
			LArm[2]+=axis[1]*5
		if abs(axis[0])>0.2:
			LArm[3]+=axis[0]*5
		JointNames = ["LElbowRoll","LElbowYaw"]
		Angles = [LArm[2],LArm[3]]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
	else:
		LArm[2]=LArmDefault[2]
		LArm[3]=LArmDefault[3]


	if (axis[2]>0.2 and ButtonY==False and ButtonX==True):
		
		if abs(axis[1])>0.35:
			LArm[4]+=axis[1]*5
		JointNames = ["LWristYaw"]
		Angles = [LArm[4]]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
	else:
		LArm[4]=LArmDefault[4]


def RightArmMovement():
	"""Controls everything about the RIGHT arm"""
	#Get joysticks
	axis=[]
	axes = joystick.get_numaxes()
	for i in range(axes):
		axis.append(joystick.get_axis(i))

	ButtonY=joystick.get_button(3)
	ButtonX=joystick.get_button(2)
	if (axis[2]<-0.2 and ButtonY==False and ButtonX==False):
		#Right Shoulder
		
		if abs(axis[0])>0.35:
			RArm[0]+=axis[0]*5
		if abs(axis[1])>0.2:
			RArm[1]+=axis[1]*5

		JointNames = ["RShoulderRoll","RShoulderPitch"]
		Angles = [RArm[0],RArm[1]]  #105+((axis[1]-0.75)*50)
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
	else:
		RArm[0]=RArmDefault[0]
		RArm[1]=RArmDefault[1]

	if (axis[2]<-0.2 and ButtonY==True and ButtonX==False):
		
		if abs(axis[1])>0.35:
			RArm[2]+=axis[1]*5
		if abs(axis[0])>0.2:
			RArm[3]+=axis[0]*5
		JointNames = ["RElbowRoll","RElbowYaw"]
		Angles = [RArm[2],RArm[3]]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
	else:
		RArm[2]=RArmDefault[2]
		RArm[3]=RArmDefault[3]


	if (axis[2]<-0.2 and ButtonY==False and ButtonX==True):
		
		if abs(axis[1])>0.35:
			RArm[4]+=axis[1]*5
		JointNames = ["RWristYaw"]
		Angles = [RArm[4]]
		Angles = [ x * motion.TO_RAD for x in Angles]
		move(JointNames,Angles)
	else:
		RArm[4]=RArmDefault[4]


def UpdateEyes():
	if (RecordPlayMode==0):
		color="blue"#None
	elif (RecordPlayMode==1):
		color="green"#Record
	else:
		color="red"#Play

	
	color2=webcolors.name_to_rgb(color)
	led.post.setIntensity("LeftFaceLedsRed", float(color2[0])/255)
	led.post.setIntensity("LeftFaceLedsGreen", float(color2[1])/255)
	led.post.setIntensity("LeftFaceLedsBlue", float(color2[2])/255)
	color2=webcolors.name_to_rgb(color)
	led.post.setIntensity("RightFaceLedsRed", float(color2[0])/255)
	led.post.setIntensity("RightFaceLedsGreen", float(color2[1])/255)
	led.post.setIntensity("RightFaceLedsBlue", float(color2[2])/255)





done=False
ButtonStart=False
ButtonBack=False
pButtonStart=False
pButtonBack=False
#Main Loop
while done==False:

	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop


	pButtonStart=ButtonStart
	pButtonBack=ButtonBack
	ButtonStart=joystick.get_button(7)
	ButtonBack=joystick.get_button(6)

	RightArmMovement()
	LeftArmMovement()
	HandMovement()
	LegMovement()
	UpdateEyes()#Updates the eyes based on the "mode" it is in



	'''
	#Reset position
	if (ButtonStart==True):
		pp.goToPosture("Stand", 1.0)
		resetPosture()

	#Autonomous life toggle
	if (ButtonBack==True):
		woke = not woke
		if woke==False:
			mp.rest()
			resetPosture()
		else:
			mp.wakeUp()
    		resetPosture()
    '''




    #Start/Stop Recording
	if (ButtonStart==True and pButtonStart==False):
		dataStep=0
		if RecordPlayMode==0:
			RecordPlayMode=1
			if os.path.isfile(dataFile):
				os.remove(dataFile)
		else:
			RecordPlayMode=0

    #Play Recoding
	if (ButtonBack==True and pButtonBack==False):
		dataStep=0
		if RecordPlayMode==0:
			RecordPlayMode=2
		else:
			RecordPlayMode=0
	
	if (RecordPlayMode==1):
		#Record!
		Record.Record(dataFile,Hands,LArm,RArm)
		print Hands,LArm,RArm

	#Play!
	if (RecordPlayMode==2 and dataLoad==False):
		data=Record.Play(dataFile)
		dataLoad=True
	if (RecordPlayMode==2):
		
		LArm=data[1][dataStep]
		RArm=data[2][dataStep]

		#print Hands
		angles=[Hands[0],Hands[1],LArm[0],LArm[1],LArm[2],LArm[3],LArm[4],RArm[0],RArm[1],RArm[2],RArm[3],RArm[4]]
		print angles
		print angles[4],angles[5]
		angles = [ x * motion.TO_RAD for x in angles]
		moveAll(angles)

	

	dataStep+=1
	clock.tick(30)#30

