from MCLP_function import MCLP


a = MCLP()
#print(a.dfs)



print(a.MCLP_function(k=5,max_coverage=1000))


for i in range(1,20):
    print(a.MCLP_function(k=i,max_coverage=10000))