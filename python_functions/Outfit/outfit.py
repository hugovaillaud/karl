"""
Outfit Creator
"""
import numpy as np
from random import randint


def get_outfit(db, outfit=list(), categories=[], bp_needed=[], undesired=list()) :
	"""
	Returns an outfit made with clothes from database db, given:
	:param db: the database of clothes | format : refer to clothes.json
	:param outfit: a partial outfit that needs to be completed/modified | format : same as in clothes.json
	:param categories: a set of categories of clothes that need to be added to the outfit | format : list of strings containing existing clothes categories
	:param bp_needed: a set of body parts that need to be covered (refer to bodyparts documentation) | format : list of integers naming body parts (refer to bodyParts.txt)
	:param undesired: a  set of clothes ids that the user explicitly don't want in the outfit | format : list of ids generated by mongodb to refer to clothes, (examples in clothe
	:return:
	"""
	[db, outfit, categories, bp_needed] = check_outfit_conflict(db, outfit, categories, bp_needed, undesired)
	
	"""if outfit, categories and bodyparts needed are specified"""
	if len(outfit) and len(categories) and len(bp_needed):
		for category in categories:

			clothes = np.array(get_clothes_by_cat(db, category))

			outfit.extend(get_clothes_by_cat(clothes, bp_needed))


	"""if only outfit and categories are specified"""
	if len(outfit) and len(categories) and not(len(bp_needed)):
		for category in categories:

			outfit.extend(get_rand_clothes(db, category))


	"""if the outfit and bodyparts needed are specified""" #TODO
	if len(outfit) and not(len(categories)) and len(bp_needed):
		outfit.extend(get_best_clothe_bp(db, bp_needed))


	"""if categories and bodyparts needed are specified"""
	if not(len(outfit)) and len(categories) and len(bp_needed):

		for category in categories:
			clothes = np.array(get_clothes_by_cat(db, category))
			outfit.extend(get_best_clothe_bp(clothes, bp_needed))


	"""if categories are specified"""
	if not(len(outfit)) and len(categories) and not(len(bp_needed)):
		for category in categories:

			outfit.extend(get_rand_clothes(db, category))


	"""if the bodyparts needed are specified"""
	if not(len(outfit)) and not(len(categories)) and len(bp_needed):

		outfit.extend(get_best_clothe_bp(db, bp_needed))


	"""if nothing is specified"""
	if not(len(categories)) and not(len(bp_needed)):

		outfit = make_simple_outfit(db, outfit)

	return outfit


def get_clothes_by_cat(db, cat):
	"""
²	takes a clothes dataset and a clothe category, sends back all the clothes of this category
	:param db:
	:param cat:
	:return:
	"""
	clothes = list()
	for i in range(len(db)-1):
		if db[i]['category'] == cat:
			clothes.append(db[i])
	return clothes


def get_rand_clothes(db, cat=[]):
	"""
	takes a clothes dataset (and a clothe category), and returns a single clothe
	:param db:
	:param cat:
	:return:
	"""
	if len(cat):
		clothes = get_clothes_by_cat(db, cat)
		clothe = clothes[randint(0, len(clothes)-1)]
	else:
		clothe = db[randint(0, len(db) - 1)]
	return clothe


def get_clothes_by_bp(db, bodyParts):
	"""
	takes a clothes dataset and a clothes bodyparts, and returns clothes that cover these bodyparts
	:param db:
	:param bodyParts:
	:return:
	"""
	clothes = list()

	for i in range(0,len(db)-1):
		if match_body_parts(db[i]['bodyparts'],bodyParts):
			clothes.append(db[i])
	return clothes


def match_body_parts(bp1, bp2):
	"""
	check if there is a match between two sets of bodyparts
	:param bp1:
	:param bp2:
	:return:
	"""
	for i in bp1:
		for j in bp2:
			if i == j:
				return True
	return False


def comp_body_parts(bp_needed, bpComp):
	"""
	#return the number of bodyparts needed that are in the bodyparts set 'bpComp'
	:param bp_needed:
	:param bpComp:
	:return:
	"""

	cnt = 0

	for bp in bp_needed:
		if bp in bpComp:
			cnt += 1
	return cnt


def get_best_clothe_bp(db, bp_needed) :
	"""
	returns an optimum clothe given a set of bodyparts
	:param db:
	:param bp_needed:
	:return:
	"""
	db=np.array(db)
	score = np.empty(0)

	for i in range(0,len(db)-1):
		score = np.append(score, comp_body_parts(db[i]['bodyparts'], bp_needed))

	clothe = get_rand_clothes(db[np.argwhere(score == np.amax(score))])
	return clothe.tolist()


def make_simple_outfit(db, outfit):
	"""
	makes a default outfit with a tshirt, a jacket and pants
	:param db:
	:param outfit:
	:return:
	"""
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
			outfit.append(get_rand_clothes(db,categories[0][i]))

	return outfit


def check_outfit_conflict(db, outfit, categories, bodyPartsNeeded, undesired) :
	"""
	checks all the conflicts that can happen for the arguments of the function getOutfit, correct them if appropriate

	:param db:
	:param outfit:
	:param categories:
	:param bodyPartsNeeded:
	:param undesired:
	:return:
	"""
	if len(outfit) and len(categories) :
		for clothe in outfit :
			if clothe['category'] in categories :
				categories.remove(clothe['category'])
				print(clothe['name'],  "is already a clothe of category :", clothe['category'])

	if len(outfit) and len(bodyPartsNeeded) :
		for clothe in outfit :
			for bodyPart in clothe['bodyparts'] :
				if bodyPart in bodyPartsNeeded :
					bodyPartsNeeded.remove(bodyPart)
					print(bodyPart, "is already covered by :", clothe['name'])

	new_outfit = outfit

	if len(outfit) and len(undesired) :
		for clothe in outfit :
			if clothe['_id'] in undesired :
				new_outfit.remove(clothe)
				print(clothe['name'], "is both in outfit and undesired clothes. Removing of clothe in outfit")

	outfit = new_outfit

	newdb = db

	if len(undesired) :
		for clothe in db :
			if clothe['_id'] in undesired :
				newdb.remove(clothe)

	db = newdb

	return [db, outfit, categories, bodyPartsNeeded]


def print_clothes_names(outfit):
	"""
	#input : a list of clothes | the function returns
	:param outfit:
	:return:
	"""
	for cloth in outfit:
		print(cloth['name'])

