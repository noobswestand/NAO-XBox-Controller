import pygame
from naoqi import ALProxy
import motion
import csv
import os.path

import os 
working_directory = os.path.dirname(os.path.realpath(__file__))
file=working_directory+"record.csv"

#Arm Vars
RArmDefault=[-7,75,15,50]
RArm=[-7,75,15,50]

LArmDefault=[7,75,-15,50]
LArm=[7,75,-15,50]

Hands=[20,20]

def Record(path,Hands,LArm,RArm):
	"""Appends the given csv file with the given data"""
	if os.path.isfile(path)==False:
		file=open(path,'ab')
		writer=csv.writer(file)
		writer.writerow(['Hands','LArm','RArm'])
	else:
		file=open(path,'ab')
		writer=csv.writer(file)

	for i in range(len(Hands)):
		writer.writerow([Hands,RArm,LArm])

def Play(path):
	"""Returns a 2D array, with all the joint angles at any given frame"""
	file=open(path)
	reader=csv.reader(file)
	header=next(reader)
	data = [[] for i in range(3)]
	for row in reader:
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


		data[0].append(Hands2)
		data[1].append(LArm2)
		data[2].append(RArm2)

	return data


'''
def main():
	Record(file,RArm,LArm,Hands)
	Play(file)
'''