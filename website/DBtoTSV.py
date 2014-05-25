import redis
import os
dbc = redis.StrictRedis(host='localhost',port=6379,db=0)
f = open('tables.tsv','w')
f.write('table\tteam\tproject\tsubmission\n')
for sub in range(1,187):
        if sub < 10:
            submission = "submission00" + str(sub)
        elif sub < 100:
            submission = "submission0" + str(sub)
        else:
            submission = "submission" + str(sub)
        thisEntry = dbc.hgetall(submission)
        if(thisEntry):
            outString = thisEntry['table'] + "\t" + thisEntry['teamName'] + "\t" + thisEntry['projectName'] + "\t" + submission + "\n"
            f.write(outString)

f.close()
            
        
