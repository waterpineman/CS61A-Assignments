def private(ag):
    print("haha")
    def punder(ag):
        return ag
    return punder

def horse(mask):
    horse = mask
    def mask(horse):
        return horse
    return horse(mask)

mask = lambda horse: horse(2)
horse(mask)