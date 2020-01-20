def testexist(flg):
    if flg == 1:
        return True
    else:
        return False


flg = 1
existflg = testexist(flg)
print(existflg)