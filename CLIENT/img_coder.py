import os, random, shutil
from PIL import Image

code_dict = {
    0:'A', 1:'A', 2:'A', 3:'A', 4:'A', 5:'A', 6:'A', 7:'A', 8:'A', 9:'A', 10:'A', 11:'A', 12:'A', 13:'A', 14:'A', 15:'A', 16:'A', 17:'A',
    18:'B', 19:'B', 20:'B',
    21:'C', 22:'C', 23:'C', 24:'C', 25:'C', 26:'C',
    27:'D', 28:'D', 29:'D', 30:'D', 31:'D', 32:'D', 33:'D', 34:'D', 35:'D', 36:'D',
    37:'E', 38:'E', 39:'E', 40:'E', 41:'E', 42:'E', 43:'E', 44:'E', 45:'E', 46:'E', 47:'E', 48:'E', 49:'E', 50:'E', 51:'E', 52:'E', 53:'E', 54:'E', 55:'E', 56:'E', 57:'E', 58:'E', 59:'E', 60:'E', 61:'E', 62:'E', 63:'E',
    64:'F', 65:'F', 66:'F', 67:'F', 68:'F',
    69:'G', 70:'G', 71:'G',
    72:'H', 73:'H', 74:'H', 75:'H', 76:'H', 77:'H', 78:'H', 79:'H', 80:'H', 81:'H', 82:'H', 83:'H', 84:'H', 85:'H',
    86:'I', 87:'I', 88:'I', 89:'I', 90:'I', 91:'I', 92:'I', 93:'I', 94:'I', 95:'I', 96:'I', 97:'I', 98:'I', 99:'I',
    100:'J', 101:'J',
    102:'K', 103:'K',
    104:'L', 105:'L', 106:'L', 107:'L', 108:'L', 109:'L', 110:'L', 111:'L', 112:'L',
    113:'M', 114:'M', 115:'M', 116:'M', 117:'M',
    118:'N', 119:'N', 120:'N', 121:'N', 122:'N', 123:'N', 124:'N', 125:'N', 126:'N', 127:'N', 128:'N', 129:'N', 130:'N', 131:'N', 132:'N',
    133:'O', 134:'O', 135:'O', 136:'O', 137:'O', 138:'O', 139:'O', 140:'O', 141:'O', 142:'O', 143:'O', 144:'O', 145:'O', 146:'O',
    147:'P', 148:'P', 149:'P', 150:'P', 151:'P', 152:'P',
    153:'Q', 154:'Q',
    155:'R', 156:'R', 157:'R', 158:'R', 159:'R', 160:'R', 161:'R', 162:'R', 163:'R', 164:'R', 165:'R', 166:'R', 167:'R',
    168:'S', 169:'S', 170:'S', 171:'S', 172:'S', 173:'S', 174:'S', 175:'S', 176:'S', 177:'S', 178:'S', 179:'S', 180:'S', 181:'S',
    182:'T', 183:'T', 184:'T', 185:'T', 186:'T', 187:'T', 188:'T', 189:'T', 190:'T', 191:'T', 192:'T', 193:'T', 194:'T', 195:'T', 196:'T', 197:'T', 198:'T', 199:'T', 200:'T', 201:'T',
    202:'U', 203:'U', 204:'U', 205:'U', 206:'U', 207:'U',
    208:'V', 209:'V',
    210:'W', 211:'W', 212:'W', 213:'W', 214:'W',
    215:'X', 216:'X',
    217:'Y', 218:'Y', 219:'Y', 220:'Y',
    221:'Z', 222:'Z', 223:'Z',
    224:' ', 225:' ', 226:' ', 227:' ', 228:' ', 229:' ', 230:' ', 231:' ', 232:' ', 233:' ', 234:' ', 235:' ', 236:' ', 237:' ', 238:' ', 239:' ', 240:' ', 241:' ', 242:' ', 243:' ', 244:' ',
    245:'.', 246:'.', 247:'.', 248:'.', 249:'.', 250:'.',
    251:',', 252:',', 253:',', 254:',', 255:',',
    }

def CorrectString(string):
    alphabet = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '.', ','}
    string = string.upper()  ## преобразование всей строки в верхний регистр
    for i in string:
        if i in alphabet:
            continue
        else:
            string = string.replace(i, '') ## удаление всех символов НЕ содержащихся в алфавите(alphabet)
    return string

def SelectionImages(string):
    count_msg = 0 ## счётчик отправляемых изображений

    for i in os.listdir(path='4send/'): ## удаление всех ненужных файлов в папке для отправки изображений
        os.remove('4send/' + str(i))

    for i in CorrectString(string):  ## цикл по всем елементам заданной строки
        if i == ' ':
            temp_img = [item for item in os.listdir(path="images/") if ('space_') in item]
            shutil.copyfile('images/' + temp_img[random.randint(0, len(temp_img)-1)], '4send/' + str(count_msg) + '_msg.jpg')
        else:
            temp_img = [item for item in os.listdir(path="images/") if (str(i) + '_') in item]  ## список всех изображений по заданному елементу строки
            shutil.copyfile('images/' + temp_img[random.randint(0, len(temp_img)-1)], '4send/' + str(count_msg) + '_msg.jpg')

        ## копирование рандомного изображения из выбранных и обновление счетчика изображений
        count_msg += 1

    shutil.copyfile('images/end.jpg', '4send/end.jpg')

    return count_msg

def ClearDirectory():
    for i in os.listdir(path='recv/'): ## удаление всех ненужных файлов в папке для получения изображений
        if i == 'end.jpg':
            continue
        os.remove('recv/' + str(i))

def DecodeImages():
    decoded_msg = ''
    for i in range(len(os.listdir(path='recv/')) - 1):
        im = Image.open('recv/' + str(i) + '_msg.jpg')
        print(str(i))
        pix = im.load()
        print(pix[14,88][1])
        decoded_msg += code_dict[pix[14,88][1]]
    return decoded_msg

def RandomName():
    rnd_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z', ' ', '.', ',', 'a', 'c', 'b', 'e', 'd', 'g', 'f', 'i', 'h', 'k', 'j', 'm', 'l', 'o', 'n', 'q', 'p', 's', 'r', 'u',
    't', 'w', 'v', 'y', 'x', 'z', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '#', '%', '$']
    name = ''
    for i in range(random.randint(8,17)):
        name += rnd_alphabet[random.randint(0, len(rnd_alphabet))]
    return name

##print(RandomName())
##SelectionImages('ABCDEFGHIJKLMNOPQRфырпворфыпвоп 12131123 ,.шоФЫШ;%!";!:"ST')
##print(DecodeImages())
