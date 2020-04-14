####################################################################
#    用于将手动show log 以show命令分割成若干文件，且以show xxxx命名
####################################################################
import os,re,sys,getopt
def usage():
    print('\n使用说明:\n')
    print('本工具用于将手动show log 以show命令分割成若干txt文件，且以show xxxx命名')
    print('  example:\n')
    print('      python test.py -i <inputfile_ARP.txt> \n')
    print('  输入文件须为文本，扩展名可以是.txt.log等。路径需为英文')
    print('  脚本自动在原始文件路径下创建名为hostname的文件夹，且将结果文件输出到该文件夹下\n')
# inputfile = r'C:\Users\qinci\Desktop\Untitled-1.txt'   #仅仅用作debug测试
try:
    opts,args = getopt.getopt(sys.argv[1:],'i:')
except getopt.GetoptError:
    usage()
    sys.exit(3)
for opt,filename in opts:
    if opt == '-i':
        inputfile=filename
l1= list()
l2= list()
###########抓取inputfile中的hostname字段名###########
file0=open(inputfile,'r',encoding='utf-8')
hostname = re.search('hostname (.+)\n',file0.read())
if hostname is not None:
    hostname=hostname.group(1)
else:
    hostname = '001-file-no-hostname'
file0.close()

######判断inputfile路径，用于在同路径下创建文件夹######
inputPath = re.search(r'(.+)\\(.+)*',inputfile)
inputPath = inputPath.group(1)
#############创建以hostname为名的文件夹###############
outputPath = inputPath+'\\'+hostname
folder = os.path.exists(outputPath)
if not folder:                  #判断文件夹是否存在，如不存在则创建之
	os.makedirs(outputPath)

##########使用正则分割，按照#show xxx分割文件#########
file0=open(inputfile,'r',encoding='utf-8')
pattern ='(.+#.*show.+\n?)'     #表达式加小括号()可以保留show xxx所在行，否则只记录“正文”行
result = re.split(pattern,file0.read())
file0.close()

######创建两个list,以result文件奇偶下标分别追加元素#####
# if '\ufeff' in result:        #因为split分割的第一个元素一定为空或者无效，因此无需判断直接删除第一个元素即可
#     result.remove('\ufeff')
#     print(' ufeff del')
# if  "show" not in result[0]:  #因为split分割的第一个元素一定为空或者无效，因此无需判断直接删除第一个元素即可
#     result.remove(result[0])
#     print('del 0')
result.remove(result[0])        #直接删除第一个元素
for i in range(len(result)):
    if i%2 == 0:
        l1.append(result[i])
    else:
        l2.append(result[i])
del result

########以list1的长度控制循环，利用l1和l2的元素关系，按照result奇偶下标成对输出到文件
for i in range(len(l1)):
    path0 =re.sub(':','',re.findall('show.+\n',l1[i])[0][:-1])  #只取第一个元素，并且去除元素后的换行符,且去除部分show 命令后的‘：’
    outputfile = outputPath+'\\'+path0+ '.txt'
    file1=open(outputfile,'w+',encoding='utf-8')
    file1.write(l1[i])
    file1.write(l2[i])
    file1.close()
