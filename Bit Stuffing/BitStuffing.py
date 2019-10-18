import re

def stringToBinary(st):
    return ' '.join(format(ord(x), 'b') for x in st)
	
#input: argument in string format with space inbetween  
def binaryToString(bn): 
    bn = bn.split(' ')
    bn_ascii = list(map(lambda i : int(i,2),bn))
    text = ''.join(chr(i) for i in bn_ascii)
    return text
	
def bitStuffing(binValue):
    stuffedBit = re.sub(r'(\s*1\s*1\s*1\s*1\s*1\s*)', r'\g<1>0', binValue) #can also use just \1 to match the grouped string. 
    return stuffedBit
	
def bitUnstuffing(binValue):
    unstuffedBit = re.sub(r'(\s*1\s*1\s*1\s*1\s*1\s*)(0)', r'\g<1>'+re.escape(""), binValue) #removing second group and keeping the first
    return unstuffedBit
	
def displayValues(text,value):
    print(text,value,"\n")

if __name__ == "__main__":

    #data load
    fr = open("inputTxtFile.txt", "r")
    text = fr.read()
    
    #convert string to bit stream
    binValue = stringToBinary(text) 

    #bit stuffing method called
    stuffedBitStream = bitStuffing(binValue)

    displayValues("The bitstuffed values:",stuffedBitStream.replace(" ",""))
    
    #bitunstuffing method called
    unstuffedBitStream  = bitUnstuffing(stuffedBitStream)
    
    #convert bit stream to string
    strValue = binaryToString(unstuffedBitStream)

    #storing the converted string in an output file
    if(strValue==text):        
        fw = open("outputTxtFile.txt", "w")
        fw.write(strValue)
        fw.close()

    

