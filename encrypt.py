from time import sleep
import random
import emailModule
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

#71
sendEmail = emailModule.emailModule()
elements = len(alphanumericDictionary)
numberList = []
encryptedList = []
encryptedMessage = []
quotientList = []
a=2
b=3
c=4
d=5
try:
    message = input("Enter message you would like to encrypt: ")
    filename = input("Name message file: ")
    choice = int(input("Enter 0 to randomize key matrix and 1 to enter your own: "))
    if (choice==1):
        a = int(input("Enter Upper Left Key Number: "))
        b = int(input("Enter Upper Right Key Number: "))
        c = int(input("Enter Lower Left Key Number: "))
        d = int(input("Enter Lower Right Key Number: "))
    elif (choice==0):
        print("Warning: Not all randomizations work and may result in corrupted decryptions")
        sleep(1.5)
        print("Randomizing...")
        determinant=0
        while (determinant==0):
            a = random.randint(0,20)
            b = random.randint(0,20)
            c = random.randint(0,20)
            d = random.randint(0,20)
            determinant = (a*d) - (b*c)
            print("Retrying...")
    else:
        a=2
        b=3
        c=4
        d=5
        print("Error\nUsing defualt matrix")
    arrayMatrix = [a, b, c, d]
    with open("matrixKey.txt", "w+") as f:
        f.write(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)+'\n')
    sleep(0.5)
    print('Encrypting...')
    sleep(0.5)
    listText = list(message)
    for q in range(len(listText)):
        numberList.append(alphanumericDictionary[listText[q]])
    if (len(numberList)%2>0):
        numberList.append(26)
    i = 0
    for value in range(random.randint(0, 100)):
        print(alphabet[random.randint(0, elements-1)] + alphabet[random.randint(0, elements-1)] +
              alphabet[random.randint(0, elements-1)] + alphabet[random.randint(0, elements-1)] +
              alphabet[random.randint(0, elements-1)] + alphabet[random.randint(0, elements-1)])
        sleep(0.1)
    while(i < len(numberList)):
        tempEncryptor = numberList[i:i+2]
        encryptedCharacter1 = ((a*tempEncryptor[0])+(c*tempEncryptor[1]))%elements
        encryptedCharacter2 = ((b*tempEncryptor[0])+(d*tempEncryptor[1]))%elements
        quotientList.append(((a*tempEncryptor[0])+(c*tempEncryptor[1]))/elements)
        quotientList.append(((b*tempEncryptor[0])+(d*tempEncryptor[1]))/elements)
        encryptedList.append(encryptedCharacter1)
        encryptedList.append(encryptedCharacter2)
        i=i+2
    for value in range(len(encryptedList)):
        encryptedMessage.append(str(alphabet[encryptedList[value]]))
    finalMessage = "".join(encryptedMessage)
    print("Computing...")
    sleep(3)
    print("Message Encrypted: ")
    sleep(0.75)
    print(finalMessage)
    with open(filename+".txt", 'w+') as f:
        f.write(finalMessage)
        f.write("\n")
        for v in range(len(quotientList)):
            f.write(str(quotientList[v]))
            f.write("-")
    sendChoice = input("Enter 1 if you would like to send your message via email or 0 if not: ")
    if (sendChoice==1):
        sender = input("Enter email address: ")
        password = input("Enter email password: ")
        reciever = input("Enter reciever's email address: ")
        subject = input("Enter subject: ")
        print("Sending...")
        sendEmail.sendMail(sender, password, reciever, subject, filename=filename+'.txt')
        print("Email Sent")
    else:
        print("Finished")
        exit()

except KeyboardInterrupt:
    print("Exiting...")

except:
    print("Error\nSomthing went wrong")
    print("\nCheck Message for errors and don't include as many special symbols")


