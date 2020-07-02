class Game:

    def __init__(self):
        self.level = 0
        self.difficulty = 30
        self.score = 0
        self.gamestate = 0
        self.drawscore = False
        self.coord = []
        self.scoreList = []

    def writehighscores(self):
        with open('high_scores.txt', 'w') as file:
            for data in self.scoreList:
                file.write(str(data) + "\n")

    def readhighscores(self, firstname):
        tmpScoreList = []
        tmpItem = 0
        tmpScore = {}
        with open('high_scores.txt', 'r') as file:
            for line in file:
                try:
                    self.scoreList.append(line.rstrip())
                except:
                    pass
        if firstname:
            self.scoreList.append(firstname + " " + str(self.score))
        ## convert to dict
        try:
            for item in self.scoreList:
                x = item.split()
                tmpScore[int(x[1])] = x[0]
        except:
            pass
        ## sort by keys
        tmpScore = sorted(tmpScore.items(), reverse=True)
        ## convert to list
        try:
            for item in tmpScore:
                text = item[1] + " " + str(item[0])
                tmpScoreList.append(text)
        except:
            pass
        self.scoreList = tmpScoreList
