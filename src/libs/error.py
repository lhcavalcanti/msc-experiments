# Import libraries
from dis import dis
import numpy as np



class Error:

    def desvioPadrao(self, desvioArray):
        value=0
        for i in desvioArray:
            value = value + (i-0.25)**2

        return np.sqrt(value/len(desvioArray))

    def measureDistortion(self, errorArray):
        arrayX = errorArray[:, 0]
        arrayY = errorArray[:, 1]

        square = np.zeros(1000000)
        distortionX = np.array([])
        distortionY = np.array([])
        squareAppend = [i/1000000 for i in range(1, 1000001, 1)]
        squareAppend = np.append(squareAppend, square)
        #print(squareAppend)

        print(self.desvioPadrao(squareAppend))


        halfX = 1.5
        halfY = 1.2

        count = 0

        for i in arrayX:
            if i == halfX:
                distortionX = np.append(distortionX, [1])
            elif i > halfX:
                distortionX = np.append(distortionX, [round(abs(i-2.5),3)])
            else:
                distortionX = np.append(distortionX, [round(abs(i-0.5),3)])
        
        for i in arrayY:
            if i == halfY:
                distortionY = np.append(distortionY, [1])
            if i > halfY:
                distortionY = np.append(distortionY, [round(abs(i-2.2),3)])
            else:
                distortionY = np.append(distortionY, [round(abs(i-0.2),3)])
            
        for i in arrayY:
            if round(min(abs(i-0.2),(abs(i-2.2))),3)>0.25-(np.sqrt(np.var(distortionY))) and round(min(abs(i-0.2),(abs(i-2.2))),3)<0.25 +(np.sqrt(np.var(distortionY))):
                count += 1

        #print("variancia distortionY", np.var(distortionY))
        #print(count/len(arrayY))
        #return np.mean(distortionX)/np.var(distortionX), np.mean(distortionY)/np.var(distortionY)
        #return np.sqrt((np.var(distortionX))), np.sqrt(np.var(distortionY))
        return self.desvioPadrao(distortionX), self.desvioPadrao(distortionY)
        #return distortionX, distortionY
        #return np.var(distortionX), np.var(distortionY)
        #return 0.25-(3*np.sqrt(np.var(distortionX))), 0.25 +(3* np.sqrt(np.var(distortionX)))
        #return np.mean(distortionX), np.mean(distortionY)

    def pointDistance(self, truth, predict):
        diff = np.subtract(truth, predict) # Points difference x2 - x1, y2 - y1
        # print(truth[0:2], ' - ', predict[0:2], ' = ' , diff[0:2])
        # print ('square() = ',  np.square(diff[0:2]))
        # print ('sum() = ',  np.sum(np.square(diff[0:2]), axis=1, keepdims=True))
        # print('mean() = ', np.sum(np.square(diff[0:2]), axis=1, keepdims=True).mean())
        return np.sum(np.square(diff), axis=1, keepdims=True) #  Components sum (x^2 + y^2) 
    
    def MSE(self, truth, predict):
        return self.pointDistance(truth, predict).mean() # Square supressed by missing distance sqrt
    
    def RMSE(self, truth, predict):
        return np.sqrt(self.MSE(truth, predict))
