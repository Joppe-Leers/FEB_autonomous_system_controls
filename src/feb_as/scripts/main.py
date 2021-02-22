from simWrap import SimWrap

if __name__ == '__main__':
    simulationWrapper = SimWrap()
    simulationWrapper.init()
    
    while True:
        state, score, done = simulationWrapper.step([0, 1, 0])
        print("state: " + str(len(state)) + " score: " + str(score) + " done: " + str(done))

##if __name__ == '__main__':
##    simulationWrapper = SimWrap()
##    simulationWrapper.init()
##    count = 0
##    while count <= 50:
##        count+=1
##        print(count)
##        simulationWrapper.step([-1, 1, 0])
##        time.sleep(0.1)
##    simulationWrapper.reset()

##if __name__ == '__main__':
##    simulationWrapper = SimWrap()
##    simulationWrapper.init()
##    while True:
##        conesClose = simulationWrapper._SimWrap__getVision()
##        print(len(conesClose))
##        x = []
##        y = []
##        for cone in conesClose:
##            x.append(cone.location.x)
##            y.append(cone.location.y)
##        plt.scatter(x, y)
##        plt.scatter(0, 0)
##        plt.savefig('vision.jpg')
##        plt.close()
##        time.sleep(2)
