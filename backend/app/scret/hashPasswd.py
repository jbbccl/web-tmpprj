import hashlib

salt='你说得对'

def hashPass(rowPasswd):
    rowPasswd+=salt
    #print(rowPasswd)
    hashPasswd = hashlib.sha1(rowPasswd.encode("utf-8")).hexdigest()
    #print(hashPasswd)
    return hashPasswd 

