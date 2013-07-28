import random
import re

DEBUG = True

def debug(s):
    if DEBUG: print "DEBUG: %s" % s 

pie = {"NAME": "pie", "HP": 5, "AC": 10, "DESCRIPTION": "PIE!"}
sword = {"NAME": "sword", "DESCRIPTION": "your trusty sword", "DAMAGE": "D8+1"}
orcsword = {"NAME": "orc sword", "DESCRIPTION": "the orc's sword", "DAMAGE": "D8+1"}
cookie = {"NAME": "cookie", "DESCRIPTION": "a delicous cookie", "HP": 5, "AC": 10}
heroinv =[sword,cookie]
orcinv =[orcsword,pie]
orc = {"INVENTORY": orcinv, "NAME": "orc", "HP": 10, "AC": 15, "ATTACK": 5, "DAMAGE": "D8+1", "DESCRIPTION": "an average sized orc weilding a sword"}

# actor inferface is:
#   NAME:   string
#   HP:     positive integer
#   AC:     integer
#   ATTACK: interger
#   DAMAGE: string in the format: /D([4,6,8]|1[02]|20)+?\d+/

hero = {"INVENTORY": heroinv, "NAME": "hero", "HP": 10, "AC": 15, "ATTACK": 5, "DAMAGE": "D8+1", "DESCRIPTION": "you"}
finn = {"NAME": "Finn", "HP": 1, "AC": 0, "DESCRIPTION": "a stinky hooligan"}
nouns = [hero,orc,finn,sword,pie,orcsword,cookie]
actors =[hero,orc,finn]
objects = [sword,pie,orcsword,cookie]
def d4(): return random.randint(1, 4)
def d6(): return random.randint(1, 6)
def d8(): return random.randint(1, 8)
def d10(): return random.randint(1, 10)
def d12(): return random.randint(1, 12)
def d20(): return random.randint(1, 20)

# constants should be capitalized
DICE = {
    "D4": d4,
    "D6": d6,
    "D8": d8,
    "D10": d10,
    "D12": d12,
    "D20": d20
}

def hits(attacker, defender):
    return defender["AC"] <= (d20()+attacker["ATTACK"])

def roll_damage(actor):
    # XXX does not handle cases where damage includes subtraction
    tokens = actor["DAMAGE"].split("+")
    
    damage = 0
    for t in tokens:
        if t.isdigit():
            damage += int(t)
        elif t in DICE:
            # XXX die lookup does not include multiple dice, e.g. 2D8
            damage += DICE[t]()
        else:
            print "unable to parse token: %s" % t

    return damage

def eat(actor, food):
    print "%s attempts to eat %s" % (actor["NAME"], food["NAME"])
    
    if hits(actor, food):
        damage = roll_damage(actor)
        food["HP"] -= damage
        print "%s has taken %s points of damage" % (food["NAME"], damage)
        if food["HP"] < 1:
            print "%s has completely consumed %s" % (actor["NAME"], food["NAME"])        
    else:
        print "%s unable to fit %s into mouth" % (actor["NAME"], food["NAME"])

def attack(attacker, defender):
	print "%s swings his sword at %s" % (attacker["NAME"], defender["NAME"])

	if hits(attacker, defender):
		damage = roll_damage(attacker)
		defender["HP"] -= damage
		print "%s has taken %s points of damage" % (defender["NAME"], damage)
		if defender["HP"] < 1:
			print "%s has slain %s" % (attacker["NAME"], defender["NAME"])
	else:
		print "%s misses" % (attacker["NAME"])
		
def is_alive(actor):
	return 0 < actor["HP"]

def display(message, include_prompt=True):
    """Display message and return input if prompt is included."""
    if include_prompt:
        raw_input("%s\n\n> " % message)
    else: 
        print "%s\n" % message
        
def parse_input(s):
    """Break input into VERB OBJECT INDIRECT_OBJECT for strings in format:
    <VERB> <MAYBE OBJECT> to|with <INDIRECT_OBJECT>"""
       
    input_re = re.compile(
        r"^\s*(?P<verb>[a-z]+)(\s+(?P<object>[a-z]+))?(\s+(to|with)\s+(?P<indirect_object>[a-z]+))?",
        re.IGNORECASE)
    
    m = input_re.match(s)
    if m:
        verb = m.group("verb")
        object = m.group("object")
        indirect_object = m.group("indirect_object")
        verb = verb.lower()
        if object: object.lower()
        if indirect_object: indirect_object.lower()
        
        debug("parse_input() => %s, %s, %s" % (verb, object, indirect_object))
        return verb, object, indirect_object
        
    print "ERROR: unable to parse input: %s" % s
    
    
        
print "A hero walks into a room, in the room there is an orc with a pie."

prompt = raw_input("what do you do?")
#TODO: don't forget to lower case what you get in the prompt
#print "prompt=[%s]" % prompt
#print "prompt.find('i')=[%s]" % prompt.find("i")
# XXX same key

# TODO: need to add word boundry checking to i as want to match i by itself
#       not as part of a word, e.g. time.  An easy way to overcome this 
#       initially is to force the user to spell out inventory.

#if prompt == "i" or "I":
	#print "You have %s" % stuff

# TODO: you should create a lookup table of actions like the DICE dictionary
#       and have that trigger the actions.  It could be simple at first, maybe
#       only fight and look.


tokens = prompt.split(" ")
verb = tokens[0]
obj = ""
if 1 < len(tokens):
    obj = tokens[1]
#print "the verb is " + verb
#print "the object is " + obj
if prompt == "i":
    for item in heroinv:
        print "You have  %s" % item["DESCRIPTION"]
if verb.find("look") != -1:
    found = False
    if len(obj) != 0:
        for n in nouns:
            if a["NAME"] == obj:
                print a["DESCRIPTION"]
            found = True
        if not found:
            print "I don't know what you meant by that"
    else:
        print "You stand in a small square room on the other side of the room is an orc with a pie"
if verb.find("give") != -1:
    found = False
    found1 = False
    for o in heroinv:
        if o["NAME"] == obj:
            found = True
            for a in actors:
                if a["NAME"] == indirect_object:
                    heroinv.remove(o)
                    a["INVENTORY"].append(o)
                    print "%s takes %s" % (a["NAME"], o["NAME"])
                    found1 = True
            if not found1:
                print "I don't know what you meant by that"
    if not found:
        print "I don't know what you meant by that"
if verb.find("attack"):    
    found = False
    for a in actors:
        if a["NAME"] == obj:
            attack(hero,a)
            found = True
    if not found:
        print "I don't know what you meant by that"
if cookie in orcinv:
    print "The orc is so happy he gives you a pie!"
    orcinv.remove(pie)
    heroinv.append(pie)
    print "The hero and the orc are victorious!"
import sys
sys.exit(1)

while is_alive(orc) and is_alive(hero):
	attack(orc,hero)
	if is_alive(hero):
		attack(hero,orc)

while not is_alive(orc) and is_alive(hero) and is_alive(pie):
	eat(hero,pie)


while not is_alive(hero) and is_alive(orc) and is_alive(pie):
	eat (orc,pie)

if not is_alive(pie) and not is_alive(hero):
	print "The orc is victorious"

if not is_alive(pie) and not is_alive(orc):
	print "The hero is victorious"

