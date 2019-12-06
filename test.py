a={'a':[1,2,3],'c':[1,2,3],'d':[4,5,6]}
arr=[]
for b in a:
    arr.extend(a[b])

print(arr)