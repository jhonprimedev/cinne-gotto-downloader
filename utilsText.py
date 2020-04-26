import secrets 
import string 

def clearStartAndEnd(text):
    return text.strip()

def generateCode():
    N = 40
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                                                  for i in range(40)) 
    return res