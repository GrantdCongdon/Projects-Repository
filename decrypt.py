from time import sleep
import random
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
            'r','s','t','u','v','w','x','y','z',' ','A','B','C','D','E','F','G',
            'H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X',
            'Y','Z','.','!','?',"'",',','1','2','3','4','5','6','7','8','9','0',
            '+','-','=']

alphanumericDictionary = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,
                           'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,
                           'p':15,'q':16,'r':17,'s':18,'t':19,'u':20,'v':21,
                           'w':22,'x':23,'y':24,'z':25,' ':26,'A':27,'B':28,
                          'C':29,'D':30,'E':31,'F':32,'G':33,'H':34,'I':35,
                          'J':36,'K':37,'L':38,'M':39,'N':40,'O':41,'P':42,
                          'Q':43,'R':44,'S':45,'T':46,'U':47,'V':48,'W':49,
                          'X':50,'Y':51,'Z':52,'.':53,'!':54,'?':55,"'":56,
                          ',':57,'1':58,'2':59,'3':60,'4':61,'5':62,'6':63,
                          '7':64,'8':65,'9':66,'0':67,'+':68,'-':69,'=':70}

elements = len(alphanumericDictionary)
numberList = []
finalNumbers = []
decryptedMessage = []
try:
    rawOrFile = int(input("Enter 0 for file key matrix and 1 to enter it manualy: "))
    if (rawOrFile==0):
        print("Place matrixKey file in the currect directory")
        sleep(0.5)
        with open("matrixKey.txt", 'r') as f:
            key = f.readlines()[0]
            keyList = key.split(".")
    elif (rawOrFile==1):
        keyList.append(int(input("Enter Upper Left: ")))
        keyList.append(int(input("Enter Upper Right: ")))
        keyList.append(int(input("Enter Lower Left: ")))
        keyList.append(int(input("Enter Lower Right: ")))
    else:
        print("Why, you probably did this on purpose")
        exit()
    sleep(0.5)
    filename = input("Enter the filename with extention of the encoded message: ")
    with open(filename+'.txt', 'r') as f:
        quotients = f.readlines()[1]
        quotientList = quotients.split("-")

    a = int(keyList[0])
    b = int(keyList[1])
    c = int(keyList[2])
    d = int(keyList[3])
    with open(filename+".txt", 'r') as f:
        encodedMessage = f.readlines()[0]
        encodedMessage.rstrip('\n')
    messageList = list(encodedMessage)
    messageList.remove('\n')

    for i in range(len(messageList)):
        numberList.append(alphanumericDictionary[messageList[i]])
    e=0
    determinant = (a*d) - (b*c)
    determinant = 1 / determinant
    keyList[0] = d*determinant
    keyList[2] = -c*determinant
    keyList[1] = -b*determinant
    keyList[3] = a*determinant
    a = keyList[0]
    b = keyList[1]
    c = keyList[2]
    d = keyList[3]
    print("Decrypting...")
    sleep(0.5)
    for value in range(random.randint(0, 100)):
            print(alphabet[random.randint(0, elements-1)] + alphabet[random.randint(0, elements-1)] +
                  alphabet[random.randint(0, elements-1)] + alphabet[random.randint(0, elements-1)] +
                  alphabet[random.randint(0, elements-1)] + alphabet[random.randint(0, elements-1)])
            sleep(0.1)
    while (e < len(numberList)):
        tempDecryptor = numberList[e:e+2]
        x = round(float(quotientList[e])*elements)
        y = round(float(quotientList[e+1])*elements)
        character1 = (a*x)+(c*y)
        character2 = (b*x)+(d*y)
        finalNumbers.append(character1)
        finalNumbers.append(character2)
        e=e+2
    for value in range(len(finalNumbers)):
        decryptedMessage.append(alphabet[int(finalNumbers[value])%elements])
    finalMessage = "".join(decryptedMessage)
    print("Computing...")
    sleep(3)
    print("Decrypted Messaage: ")
    sleep(0.75)
    print(finalMessage)
except KeyboardInterrupt:
    print("Exiting...")
except:
    print("Error\nSomething went wrong")
    print("\nIf problem repeats ask sender to resend")

