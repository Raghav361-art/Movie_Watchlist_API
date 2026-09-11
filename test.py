def generate(numRows):
    res = []
    prev = []
    if numRows > 0:
        prev = [1]
        res.append(prev)

    for i in range(2, numRows+1):
        cur = [0]*i 
        cur[0] = prev[0] 
        cur[-1] = prev[-1] 

        for j in range(len(prev)-1):
            cur[j+1] = prev[j]+prev[j+1]

        prev = cur
        res.append(prev)

    return res

print(generate(5))