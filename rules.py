#/usr/bin/python
import sys
import indicators

class rules:
	import indicators
	def __init__(self):
		self.idx=[]
		self.IND=indicators.indicators()
	def getIdx(self,idx):
		self.idx=idx
	#golden cross
	def applyGoldenCross(self):
		[K,D]=self.IND.stochastic(self.idx)
		#there is a cross
		if (K[-1]-D[-1])*(K[0]-D[0])<=0:
			if K[-1]>K[0]:
				#upward trend
				return 0
			elif K[-1]<K[0]:
				#downward trend
				return 0
			else:
				#flat fast stochastic
				#must look at slow to determine
				if D[-1]>D[0]:
					#downward trend
					return 0
				else:
					#upward trend
					return 0
		else:
			return 0
	#momentum
	def applyMomentum(self):
		M=self.IND.momentum(self.idx)
		

def main(idx=[], stock=0, cash=0):
	RULES=rules()
	RULES.getIdx(idx)
	IND=indicators.indicators()
	if len(idx)==0:
		print ('No History\n')
	elif len(idx)<50:
		print ('Insufficient data for operation\n')
		return 0
	else:
		RULES.applyGoldenCross()
	return 0
if __name__=="__main__":
	import sys
	testrules(sys.argv)
