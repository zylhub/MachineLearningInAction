# coding=utf-8
def loadDataSet():
	"""加载测试数据"""
	postList = ['my dog has flea problems help please',
	            'maybe not take him to dog park stupid',
	            'my dalmation is so cute I love him',
	            'stop posting stupid worthless garbage',
	            'mr licks ate my steak how to stop hime',
	            'quit buying worthless dog food stupid']
	postingList = [post.split() for post in postList]
	classVec = [0, 1, 0, 1, 0, 1]
	return postingList, classVec


def createVocabList(dataSet):
	"""创建词表"""
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)


# one-hot 模型
def setOfWords2Vec(vocabList, inputSet):
	"""根据词表得到输入的词向量"""
	returnVec = [0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print 'the word: %d is not in my vocabulary!' % word
	return returnVec


from numpy import *


def trainNB0(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = sum(trainCategory) / float(numTrainDocs)
	# p0Num = zeros(numWords); p1Num = zeros(numWords)
	# p0Denom = 0.0; p1Denom = 0.0
	p0Num = ones(numWords);
	p1Num = ones(numWords)
	p0Denom = 2.0;
	p1Denom = 2.0
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p1Vect = p1Num / p1Denom
	p0Vect = p0Num / p0Denom
	return log(p0Vect), log(p1Vect), pAbusive


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
	p1 = sum(vec2Classify * p1Vec) + log(pClass1)  # vec2Classify:词向量  p1Vec 对应词是类别1的概率，求和得到条件概率之和
	p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1)
	if p1 > p0:
		return 1
	else:
		return 0


def testingNB():
	listOPosts, listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
	p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
	testEntry = ['love', 'my', 'dalmation']
	thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
	testEntry = ['stupid', 'garbage']
	thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as :', classifyNB(thisDoc, p0V, p1V, pAb)


# 词袋模型
def bagOfWords2VecMN(vocabList, inputSet):
	returnVec = [0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1
	return returnVec


# import re
# regEx = re.compile('\W*')  # \W按照非字母数字切分文本
# regEx.split(mySent)

def textParse(bigString):
	import re
	listOfTokens = re.split(r'\W*', bigString)
	return [tok.lower() for tok in listOfTokens if len(tok) > 2]


def spamTest():
	docList = []
	classList = []
	fullText = []
	for i in range(1, 26):
		wordList = textParse(open('email/spam/%d.txt' % i).read())
		docList.append(wordList)  # 每一行表示一篇文档
		fullText.extend(wordList)
		classList.append(1)

		wordList = textParse(open('email/ham/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)

	vocabList = createVocabList(docList)
	trainingSet = range(50)
	testSet = []

	for i in range(10):
		randIndex = int(random.uniform(0, len(trainingSet)))  # 随机生成测试集
		testSet.append(trainingSet[randIndex])
		del (trainingSet[randIndex])

	trainMat = []
	trainClasses = []
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
		trainClasses.append(classList[docIndex])

	p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses)) # 条件概率和类概率

	# 分类过程
	errorCount = 0
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList, docList[docIndex])  # 词向量
		if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:  # 分类结果
			print "input word", docList[docIndex], "real lable: ", classList[docIndex]
			errorCount += 1
	print 'the error rate is:', float(errorCount) / len(testSet)


if __name__ == '__main__':
	testingNB()
	spamTest()
