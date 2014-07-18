import pickle
f = open('nlconfigure.pickle','r')
obj = pickle.load(f)
if obj:
	print obj
patterns = [('INVALID'),('NND','VBM','IN','NND'),('NND','VBS','STR'),('NN','VBD','NNO'),('NND','VBM','NND'),('EX','VBD','NND','IN','NND'),('NND','VBE','NND'),('NND','VBD','IN','NND'),('NND','VBD','NND'),('EX','VBD','NND'),('NNO','VBD','NN'),('NND','VBH','NND')]

# 0 ('INVALID'), unkown pattern 
# 1 ('NND','VBM','IN','NND'), Ali go near tree
# 2 ('NND','VBS','STR'), Ali said 'Hello'
# 3 ('NN','VBD','NNO'), Ali is boy
# 4 ('NND','VBM','NNO'), Ali go home
# 5 ('EX','VBD','NND','IN','NND'), There was a boy in jungle
# 6 ('NND','VBE','NND'), Wolf eat ali
# 7 ('NNO','VBD','IN','NND'), A sheep live in jungle.
# 8 ('NND','VBD','NNO'), Ali is a boy
# 9 ('EX' ,'VBD','NND'), There is a boy.
# 10 ('NNO','VBD','NN'), The boy is called Ali.
# 11 ('NND','VBH','NNO'), The jungle has a sheep.

newtags = dict()
for verb in ['say','shout','tell','reply']:
	newtags[verb] = 'VBS' #stand for speech
for verb in ['move','run','walk','go','come']:
	newtags[verb] = 'VBM' #stand for motion
for verb in ['be','called','live']:
	newtags[verb] = 'VBD' #stand for define
for verb in ['eat']:
	newtags[verb] = 'VBE' #stand for eat
for verb in ['have']:
	newtags[verb] = 'VBH' 

directionsDict = {'inside':'INSIDE', 'in':'IN', 'into':'INSIDE','near':'NEAR' , 'right' :'RIGHT' , 'left' :'LEFT' , 'on':'ON', 'under':'UNDER',  'top':'TOP' , 'bottom':'BOTTOM'}

f.close()
f = open('nlconfigure.pickle','w')

pickle.dump([patterns,newtags,directionsDict],f)










