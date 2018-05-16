import sys, os
import re

##quoted from source of wiki page guide on usage messages  https://stackoverflow.com/questions/983201/python-and-sys-argv
if len(sys.argv) < 2:
    sys.exit('Usage Error: Please use a baseball text file for your argument!')
    filename = sys.argv[1]
if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: Your file: %s was not found!' % sys.argv[1])
##end quoted

filename = sys.argv[1]
name_regex = re.compile(r'(.*)(?= batted)')
attempts_regex = re.compile(r'(?<=batted )(\d.*)(?= times)')
hits_regex = re.compile(r'(?<=with )(\d.*)(?= hits)')
roster = []
finalroster=[]

class Player:
        def __init__(self, name, bats, hits):
                self.name = name
                self.bats = bats
                self.hits = hits
                #self.avg = self.hits/self.bats
        def avg(self):
            if(0==self.bats) :
                return 0
            else:
                 stat=(self.hits)*1.0 / (self.bats)
                 stat=format(round(float(stat),3),'.3f')
                 return stat


def name_test(test):
	match = name_regex.search(test)
	if match is not None:
		return match.group(1)
	else:
		return False

def attempts_test(test):
	match = attempts_regex.search(test)
	if match is not None:
		return match.group(1)
	else:
		return False

def hits_test(test):
	match = hits_regex.search(test)
	if match is not None:
		return match.group(1)
	else:
		return False


####first lets make a gigantic roster of every at bat
with open(filename) as f:
    for line in f:
        strip=line.strip()
        #check to make sure the line is a stats line by using the return of the name test, we want it to go if its not false
        if(False != (name_test(strip))):
            name=(name_test(strip))
            attempts=float((attempts_test(strip)))*1.0
            hits=float((hits_test(strip)))*1.0
            a=(Player(name,attempts,hits))
            roster.append(a)

#sort list by name so we can go through and add up same names
roster.sort(key=lambda x: x.name, reverse=True)


#check for mulitple occurences of name and add hits and bats
fname = None
oldName = None
fhits=0
fbats=0

for item in roster:
    if item.name == oldName:
        #if our name equals are old name then lets add hits and bats on to that
        fname=item.name
        fhits=fhits+item.hits
        fbats=fbats+item.bats
    elif item.name!=oldName:
        #if our name does not equal the old name then we have reached a new name
        if oldName == None:
            #Special case for our first name, we need to make sure it's stats get added
            fname=item.name
            fhits=fhits+item.hits
            fbats=fbats+item.bats
        else:
            #when we see a new name, lets set our previous stats and append that player to the final roster
            currentPlayer=Player(fname,fbats,fhits)
            finalroster.append(currentPlayer)
            #let's reset our stats counter and start our new players tally
            fhits=0
            fbats=0
            fname = None
            fname=item.name
            fhits=fhits+item.hits
            fbats=fbats+item.bats
        #set our new name to old name so we can see if it comes up next for our next plater
        oldName = item.name

#print our finalized roster sorted by average
finalroster.sort(key=lambda x: x.avg(), reverse=True)
for x in range(len(finalroster)):
 print (str(finalroster[x].name)+str(": ")+str(finalroster[x].avg()))
