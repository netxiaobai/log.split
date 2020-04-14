####################################################################
#    用于将手动show log 以show命令分割成若干文件，且以show xxxx命名
####################################################################
import re,sys,getopt
def usage():
    print('\n使用说明:    \n')
    print('本工具用于将手动show log 以show命令分割成若干txt文件，且以show xxxx命名')
    print('  example:\n')
    print('      python test.py -i <inputfile_ARP.txt> \n')
    print('  输入文件须为文本，扩展名可以是.txt.log等\n')
# inputfile ='D:\\test\\001.log'
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
pattern ='(R.+\#show.+\n?)' #表达式加小括号()可以保留show run 这一行
#pattern ='R.+\#show.+\n?
file0=open(inputfile,'r',encoding='utf-8')
# hostname = re.findall('hostname',file0)
# hostname = hostname[9:]
# print(type(hostname))
result = re.split(pattern,file0.read())
result.remove('\ufeff')
file0.close()
for i in range(len(result)):
    if i%2 == 0:
        l1.append(result[i])
    else:
        l2.append(result[i])
#del result
for i in range(len(l1)):
    path0 =re.sub(':','',re.findall('show.+\n',l1[i])[0][:-1])  #只取第一个元素，并且去除元素后的换行符
    outputfile = 'D:\\test\\123\\' +path0+ '.txt'
    file1=open(outputfile,'w+',encoding='utf-8')
    file1.write(l1[i])
    file1.write(l2[i])
    file1.close()