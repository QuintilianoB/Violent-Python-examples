import crypt
import hashlib

def testpass(cryptpass):
    salt = cryptpass.split('$')[2]
    senha_sha_512 = cryptpass.split('$')[3].split(':')[0]
    print (salt + "\n")
    print (senha_sha_512 + "\n")
    dicfile = open('dic.txt', 'r')

    for word in dicfile.readlines():
        word = word.strip('\n')
        crypto = crypt.crypt(word,"$6$" + salt)
        senha_teste = crypto.split('$')[3]
        print (senha_teste + "\n")
        if senha_teste == senha_sha_512:
            print ("[+]Senha encontrada: "+word+"\n")
            return

    print ("[-]Password not found.\n")
    return

def main():
    passwd = "$6$ar7v3ZNo$BQ5Hqs8slLLZfwhZwgtXo/S7BveTbg2sQnZ/Cn52Ag0Y6bUI.Bww9FAdnh4DmgI.V1skHXKVZ7FIn5IqnPDV90:" \
             "16431:0:99999:7:::"
    testpass(passwd)

if __name__ == '__main__':
    main()