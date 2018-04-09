#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 12:40:27 2018

@author: hugo
"""
from random import randint
import numpy as np


#makes an outfit with a dataset of clothes. Can be specified a incomplete outfit, categories to add, body parts to cover, and clothes undesired on the outfit
def getOutfit(db, outfit = list(), categories = [], bpNeeded = [], undesired = list()) :

	"""if outfit, categories and bodyparts needed are specified"""
	if len(outfit) and len(categories) and len(bpNeeded) :
		for category in categories:

			clothes = np.array(getClothesbyCat(db,category))

			outfit.append(getBestClotheBP(clothes, bpNeeded))


	"""if only outfit and categories are specified"""
	if len(outfit) and len(categories) and not(len(bpNeeded)) :
		for category in categories:

			outfit.append(getRandClothe(db,category))


	"""if the outfit and bodyparts needed are specified""" #to improve
	if len(outfit) and not(len(categories)) and len(bpNeeded) :
		outfit.append(getBestClotheBP(db, bpNeeded))


	"""if categories and bodyparts needed are specified"""
	if not(len(outfit)) and len(categories) and len(bpNeeded) :
		for category in categories:

			clothes = np.array(getClothesbyCat(db,category))

			outfit.append(getBestClotheBP(clothes, bpNeeded))


	"""if categories are specified"""
	if not(len(outfit)) and len(categories) and not(len(bpNeeded)) :
		for category in categories:

			outfit.append(getRandClothe(db,category))


	"""if the bodyparts needed are specified"""
	if not(len(outfit)) and not(len(categories)) and len(bpNeeded) :

		outfit.append(getBestClotheBP(db, bpNeeded))


	"""if nothing is specified"""
	if not(len(categories)) and not(len(bpNeeded)) :

		outfit = makeSimpleOutfit(db, outfit)

	return outfit



#takes a clothes dataset and a clothe category, sends back all the clothes of this category
def getClothesbyCat(db, cat):
    clothes = list()
    for i in range(0, len(db)-1):
        if (db[i]['category'] == cat):
            clothes.append(db[i])
    return clothes


#takes a clothes dataset and a clothe category, and returns a single clothe of this category
def getRandClothe(db, cat = []):
	if len(cat):
		clothes = getClothesbyCat(db, cat)
		clothe = clothes[randint(0, len(clothes)-1)]
	else:
		clothe = db[randint(0, len(db) - 1)]
	return clothe


#takes a clothes dataset and a clothes bodyparts, and returns clothes that cover these bodyparts
def getClothesbyBP(db, bodyParts):

	clothes =list()

	for i in range(0,len(db)-1):
		if (matchBodyParts(db[i]['bodyparts'],bodyParts)):
			clothes.append(db[i])
	return clothes


#check if there is a match between two sets of bodyparts
def matchBodyParts(bp1, bp2):
	for i in bp1:
		for j in bp2:
			if (i == j):
				return True
	return False


#return the number of bodyparts needed that are in the bodyparts set 'bpComp'
def compBodyParts(bpNeeded, bpComp):

	cnt = 0

	for bp in bpNeeded:
		if bp in bpComp:
			cnt = cnt + 1
	return cnt


#returns an optimum clothe given a set of bodyparts
def getBestClotheBP(db, bpNeeded) :

	db=np.array(db)
	score = np.empty(0)

	for i in range(0,len(db)-1):
		score = np.append(score,compBodyParts(db[i]['bodyparts'],bpNeeded))

	clothe = getRandClothe(db[np.argwhere(score == np.amax(score))])
	return clothe.tolist()


#makes a default outfit with a tshirt, a jacket and pants
def makeSimpleOutfit(db, outfit):

	categories = [['pants','tshirt','jacket'],[True, True, True]]

	for clothe in outfit:
		if 4 in clothe['bodyparts']:
			categories[1][0] = False
		if 2 in clothe['bodyparts']:
			categories[1][1] = False
		if 6 in clothe['bodyparts'] and 9 in clothe['bodyparts']:
			categories[1][2] = False

	for i in range(0,3):
		if categories[1][i]:
			outfit.append(getRandClothe(db,categories[0][i]))

	return outfit
