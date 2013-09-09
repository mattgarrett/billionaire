#/usr/bin/python
import sys
import indicators

class rules:
	import indicators
	def __init__(self):
		self.STOCKS=0
		self.CASH=0
		self.AIMD=0
		self.IDX=[]
		self.IND=indicators.indicators()
	def setAssets(self, stocks, cash):
		self.STOCKS=stocks
		self.CASH=cash
	def getIdx(self, idx):
		self.IDX=idx
	def applyMarket(self):
		if len(self.IDX)==1:
			return int(self.CASH)
		else:
			return 0

	#simple rule: buy more when price hikes, sell if not 
	def applySimple(self):
		if len(self.IDX) < 50:
			return 0
		else:
			if (self.IDX[-1] > self.IDX[-2]):
				return 4
			elif (self.IDX[-1] < self.IDX[-2]):
				return -1
			else:
				return 0

	#AIMD to simple rule: hike linear, exponential sell
	def applySimpleAIMD(self):
		if len(self.IDX) < 50:
			return 0
		else:
			if (self.IDX[-1] > self.IDX[-2]):
				self.AIMD=self.AIMD+self.IDX[-1]-self.IDX[-2]
				if self.STOCKS*self.AIMD > self.CASH:
					self.AIMD=0
			elif (self.IDX[-1] < self.IDX[-2]):
				self.AIMD=self.AIMD/2 
			return self.AIMD
	#golden cross
	def applyGoldenCross(self):
		[K,D]=self.IND.stochastic(self.IDX)
		#there is a cross
		if (K[-1]-D[-1])*(K[0]-D[0])<=0:
			if K[-1]>K[0]:
				#upward trend
				return 1
			elif K[-1]<K[0]:
				#downward trend
				return -1
			else:
				#flat fast stochastic
				#must look at slow to determine
				if D[-1]>D[0]:
					#downward trend
					return -1
				else:
					#upward trend
					return 1
		else:
			return 0
	#momentum
	def applyMomentum(self):
		return self.IND.momentum(self.IDX)

	def applySMA(self,length):
		return self.IND.SMA(self.IDX,length)
	
	def applyEMA(self,length):
		EMA=self.IND.EMA(self.IDX,length)
		return self.IND.EMA(self.IDX,length)
	
	def apply_moving_avg_cross(self):
		SMA150=self.applySMA(150)
		EMA35=self.applyEMA(35)
		EMA5=self.applyEMA(5)
		if len(SMA150) < 5:
			return 0
		if SMA150[-1] > SMA150[-5]:
			if EMA5[-1] > EMA35[-1] and EMA5[-2] < EMA35[-2]:
				return 1
		elif SMA150[-1] < SMA150[-5]:
			if EMA5[-1] < EMA35[-1] and EMA5[-2] > EMA35[-2]:
				return -1
		else:
			return 0

def main(argv, stock=0, cash=0):
	RULES=rules()
	RULES.setAssets(stock, cash)
	RULES.getIdx(argv)
	if len(argv)==0:
		print ('No History\n')
	elif len(argv)<50:
		print ('Insufficient data for operation\n')
		return 0
	else:
		Market=RULES.applyMarket()
		Simple=RULES.applySimple()
		SimpleAIMD=RULES.applySimpleAIMD()
		Decision=RULES.applyGoldenCross()
		Momentum=RULES.applyMomentum()
		#BMAC=RULES.apply_moving_avg_cross()
	return 0
if __name__=="__main__":
	import sys
	testrules(sys.argv)
