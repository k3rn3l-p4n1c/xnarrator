from nltk.tokenize import sent_tokenize,wordpunct_tokenize
from nltk.tag import pos_tag
import pickle
import en


key_obj = list()
objs_name = list()
def toInt(s): # TODO
	d = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,
	'ten':10,'eleven':11,'twelve':12,'thrirteen':13,'fourteen':14,
	'fifteen':15,'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19,
	'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90}
	try:
		return int(s)
	except:
		pass
	try:
		return d[s.lower()]
	except:
		pass
	try:
		a = 0
		for n in s.split('-'):
			a += toInt(n)
		return a
	except:
		pass	
	
	return 1
class NlPhrase:
	def __init__(self,tagged):
		self.main = tagged[-1][0]
		self.tag = NlPhrase.nl_simplifytag(tagged[-1])
		if self.tag in ['::','.','$',"''",')','(',',','CC','POS','SYM']:
			raise TypeError()
			
		self.article = False
		if tagged[0][1] == 'DT':
			self.article = True
			if tagged[0][0].lower() == 'a' or tagged[0][0].lower() == 'an':
				self.definited = False
			elif tagged[0][0].lower() == 'the':
				self.definited = True
			else:
				self.article = False
		self.number = 1
		if tagged[0][1] == 'CD':
			self.number = toInt(tagged[0][0])	
		try:
			self.main = en.verb.present(self.main)
		except: pass
			
		if self.tag == 'VB' or en.is_verb(self.main):
			if self.main in x_interpreter.tagdict.keys():
				self.tag = x_interpreter.tagdict[self.main]
		self.string = ""
		tagged.pop()
		for i in tagged:
			self.string += i[0] + ' '
		self.string += self.main
			
		if len(tagged) > 1:
			pass
		
	@staticmethod
	def nl_simplifytag(t): 
		global key_obj
		tag = t[1]
		if (t[1] == 'RP' or t[1] == 'RP' or t[1] == 'IN') :
			tag = 'IN'
		elif t[0] in objs_name:
			tag = 'NND'
		elif t[0] in key_obj:
			tag = 'NNO'
		elif t[1][:2] == 'NN':
			tag = 'NN'
		elif t[1][:2] == 'VB':
			tag = 'VB'
		return tag
	
	@staticmethod
	def constructor(sent):
		phrases = list()
		words =  wordpunct_tokenize(sent)
		words_tag = pos_tag(words)
		
		while len(words) > 0:
			i = 0
			if words[0] == "'" or words[0] == '"':
				start = words[0]
				i = 1
				STR = ""
				while i < len(words):
					if start in words[i]:
						break
					STR += words[i]+ ' '
					i+=1
				try: phrases.append(NlPhrase([(STR,'STR')]))
				except: pass
			elif pos_tag([words[0]])[0][1] == 'DT' or pos_tag([words[0]])[0][1] == 'CD':
				wt = NlPhrase.nl_simplifytag(words_tag[i])
				while not(wt[:2] == 'NN'):
					i += 1
					if i == len(words_tag):
						break
					wt = NlPhrase.nl_simplifytag(words_tag[i])
				try: 
					phrases.append(NlPhrase(words_tag[:i+1]))
				except: pass
			elif len(words)>1 and words[1].lower() == 'of' and words[0].lower() in x_interpreter.directionsDict:
					try: 
						phrases.append(NlPhrase([(words[0],'IN')]))
						i+=1
					except: pass
			else:
				try: phrases.append(NlPhrase([words_tag[0]]))
				except: pass
			words = words[i+1:]
			words_tag = words_tag[i+1:]
		return phrases
	
class NlSent:
	def __init__(self,s,i):
		self.orginal = s
		self.index = i
		self.words = wordpunct_tokenize(s)
		self.phrases = NlPhrase.constructor(s)
		self.patternindex = self.nl_pattern()
		self.pattern = x_interpreter.patterns[self.patternindex]

			
	def match_pattern(self,pattern):
		phrases = self.phrases
		self.pos_tagged = [None] * len(pattern);
		i = 0
		for ph in phrases:
			if ph.tag == pattern[i]:
				self.pos_tagged[i] = ph.main
				i+=1
			if i == len(pattern):
				return True
		self.pos_tagged = []
		return False
		
		
	def nl_pattern(self):
		for i,pat in enumerate(x_interpreter.patterns):
			if self.match_pattern(pat):
				return i
		return 0
	
class NlText:
	# no doc 
	def __init__(self,text):
		self.words = wordpunct_tokenize(text)
		self.adapte()
		self.string = NlText.list2str(self.words)
		self.sentences = sent_tokenize(self.string)
		self.nl_sents = []
		self.sentcount = len(self.sentences)
		for i,s in enumerate(self.sentences):
			self.nl_sents.append(NlSent(s,i))
	
	def giveSent(self,i):
		if i <= self.index:
			return self.nl_sents[i]
	def adapte(self):
		i = 0
		last_nnp = None
		while i < len(self.words):
			if pos_tag([self.words[i]])[0][1] == 'NNP':
				last_nnp = self.words[i]
			if pos_tag([self.words[i]])[0][1] == 'PRP':
				self.words[i] = last_nnp
			try:
				self.words[i] = en.verb.present(self.words[i])
			except:
				pass
			try:
				if not en.is_verb(self.words[i]):
					self.words[i] = en.noun.singular(self.words[i])
			except:pass
			
			i += 1
	
	@staticmethod
	def list2str(l):
		s = ""
		for i in l:
			s += i + ' '
		return s
class x_interpreter:
	patterns = list()
	tagdict = dict()
	directionsDict = dict()
	def __init__(self,source_code):
		self.source_code = source_code
		self.words = wordpunct_tokenize(source_code)
		f = open('nlconfigure.pickle','rb')	
		obj = pickle.load(f)
		x_interpreter.patterns = obj[0]
		x_interpreter.tagdict = obj[1]
		x_interpreter.directionsDict = obj[2]
		self.nl_text = NlText(source_code)
		
	def commands(self,index):
		global objs_name
		cmds = list()
		sents = self.nl_text.nl_sents
		for s in sents:
			pt = s.pos_tagged
			for ph in s.phrases:
				if ph.main in key_obj:
					objs_name.append(ph.main)
			if s.patternindex == 3:
				objs_name.append(pt[0])
			if s.patternindex == 10:
				objs_namea.append(pt[2])
		self.nl_text = NlText(self.source_code)
		sents = self.nl_text.nl_sents
		objs_name = []
		for s in sents:
			if not s.patternindex:
					continue
			
			pt = s.pos_tagged
			
			for phrase in s.phrases:
				if phrase.main in key_obj:
					if not phrase.main in objs_name:
						cmds.append("NEW {} {}".format(phrase.main,phrase.number))
						objs_name.append(phrase.main)
			for t in pt:
				if t in key_obj:
					if not t in objs_name:
						cmds.append("NEW {} 1".format(t))
						objs_name.append(t)
			if s.patternindex in [1,5,7]:
				pos  = x_interpreter.directionsDict.get(pt[-2],'NEAR')
			if s.patternindex == 1:
				cmds.append("MOVE {} {} {}".format(pt[0],pt[3],pos))
			if s.patternindex == 2:
				pt = s.pos_tagged
				cmds.append("SAY {} {}".format(pt[0],pt[2]))
			if s.patternindex == 3:
				cmds.append("SETNAME {} {}".format(pt[0],pt[2]))
			if s.patternindex == 4:
				cmds.append("MOVE {} {} IN".format(pt[0],pt[2]))
			if s.patternindex == 5:
				cmds.append("MOVE {} {} {}".format(pt[2],pt[4],pos))
			if s.patternindex == 6:
				cmds.append("EAT {} {}".format(pt[0],pt[2]))
			if s.patternindex == 7:
				cmds.append("MOVE {} {} {}".format(pt[0],pt[3],pos))
			if s.patternindex == 8:
				cmds.append("SETNAME {} {}".format(pt[2],pt[0]))
			if s.patternindex == 10:
				cmds.append("SETNAME {} {}".format(pt[0],pt[2]))
				objs_name.append(pt[2])	
			if s.patternindex == 11:
				cmds.append("MOVE {} {} ON".format(pt[2],pt[0]))
			
				
		return cmds
def set(key_objects_name):
	"""document"""
	global key_obj
	global objs_name
	key_obj = key_objects_name
	objs_name = []
def compile(source_code):
	"""document"""
	x = x_interpreter(source_code)
	return x.commands(0)

def main():
	pass
if __name__ == "__main__":
	main()
