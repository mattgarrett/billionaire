#/usr/bin/python

class indicators:
	def __init__(self):
		self.K=[-1,-1,-1]
		self.D=[-1,-1]
	#Traditional stochastic index
	#Fast stochastic window of 14 days
	#Slow stochastic window of 3 fast stochastic days
	def stochastic_hardcode(self,idx):
		if len(idx)<17:
			return self.K, self.D
		else:
			for j in range(2):
				win_D=idx[-2+j:-18+j:-1]
				for i in range(3):
					win_K=win_D[i:i+14]
					self.K[2-i]=float(100*(win_K[0]-min(win_K))/(max(win_K)-min(win_K)))
				self.D[j]=float(sum(self.K)/3)
			return self.K, self.D
	
	#Customized stochastic index
	#Fast stochastic window of K days
	#Slow stochastic window of D fast stochastic days for D_length data points
	def stochastic(self, idx, K=14, D=3, D_length=2):
		if D < 2:
			print('Slow stochastic index D must be >= 2\n')
			return self.K, self.D
		elif K < D+2:
			print('Fast stochastic index K must be >= D+2\n')
			print('Min value for K='+str(D+2)+' for D='+str(D)+'\n')
			return self.K, self.D
		elif len(idx)<K+D+D_length-2:
			print('Insufficient data width\n')
			return self.K, self.D
		else:
			self.K=[-1]*D
			self.D=[-1]*2
			for j in range(D_length):
				win_D=idx[-2+j:-1-(K+D)+j:-1]
				for i in range(D):
					win_K=win_D[i:i+K]
					self.K[D-1-i]=float(100*(win_K[0]-min(win_K))/(max(win_K)-min(win_K)))
				self.D[j]=float(sum(self.K)/3)
			return self.K, self.D

	#momentum
	def momentum(self, idx, history=10):
		if history > len(idx):
			print('Insufficient data width\n')
			return 0
		else:
			return idx[-1]-idx[-history]
	
	#simple moving average
	def SMA(self, idx, history=10):
		if history > len(idx):
			print('Insufficient data width\n')
			return 0
		else:
			return float(sum(a[-history:])/history)
	#exponential moving average
	def EMA(self, idx, history=22):
		if history > len(idx)-1:
			print('Insufficient data width\n')
			return 0
		else:
			EMA=self.CalculateEMA(idx,todayClose,history,yesterdayEMA)
			return EMA

	def CalculateEMA(self, idx, todayClose, history, yesterdayEMA):
		self.EMA=[idx[0]]
		k=float(2/(history+1))
		for i in range(1,len(idx)):
			if i <= history:
				self.EMA.append(self.SMA(idx[0:i]))
			else:
				self.EMA.append(float(EMA[-1]*(1-k)+idx[i]*k))
		return self.EMA[-1]

	def MACD(self, idx):
		EMA9=self.EMA(idx,9)
		EMA12=self.EMA(idx,12)
		EMA26=self.EMA(idx,26)
		MACD=[EMA12[i]-EMA26[i] for i in range(len(idx))]
