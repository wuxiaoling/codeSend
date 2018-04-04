#coding=utf-8
import os
import json
import gevent
import sys,codecs,subprocess,pexpect,time,threading

reload( sys )
sys.setdefaultencoding('utf-8')
#强制规范必要文件
def mkfile():
	f={'./exclude.txt':666,'./config.json':666}
	for i,v in f.items():
		if os.path.exists(i)==False:
			open(i,'wa+').close()
			os.system("chmod "+v+" ./exclude.txt")

#打开配置文件
def openConfig(path):
	try:
		config = codecs.open(path,'r','utf-8');
		data=config.read()
		data={} if data=="" else json.loads(data)
		config.close()
	except Exception as e:
		print e
		data={}
	return data

#打开日志缓存
def openOld(path):
	try:
		f_old = codecs.open(path,'r','utf-8');
		data=f_old.read()
		data={} if data=="" else json.loads(data)
		f_old.close()
	except Exception as e:
		print e
		data={}
	return data
	
#保存日志缓存
def saveOld(path,data):
	try:
		f_old = codecs.open(path,'wr+','utf-8')
		data=json.dumps(data)
		f_old.write(data)
		data=True
		f_old.close()
	except Exception as e:
		print e
		data=False
	return data
#执行复制操作
def copys(paths,i,v):
#for i,v in dispath.items():
	bakupPath=v[2]+'bakup/'
	old_path=paths
	disPath_one=v[2] if i=='/' else v[0]+"@"+i+":"+v[2]
	#发送文件
	cmd="rsync --progress  -uabrz --partial --log-file=./rsync.log  --force  --delete --delete-excluded="+bakupPath+"/* --backup-dir="+bakupPath+" "+old_path+" "+disPath_one+" --exclude-from=./exclude.txt "
	try:
		child = pexpect.spawn(cmd)
		if i!='/':
			child.expect(['password:'])
			child.sendline(v[1])
		#child.interact()
		while(True):
			child.expect('to-check=')
			datas=child.readline()
			one=datas.split('/')[0]
			two=datas.split('/')[1].split(')')[0]
			pre=100-int(float(one) / float(two)*100)
			#sys.stdout.flush()
			sys.stdout.write('源目录'+paths+'----->'+disPath_one+'----正在同步，进度{0}%\r'.format(pre))
			if pre==100:
				raise Exception("源目录"+paths+"----->"+disPath_one+"----同步完成，进度{0}%".format(100))
	except Exception as e:
		#print e
		if type(e)==pexpect.exceptions.EOF:
			#sys.stdout.flush()
			sys.stdout.write("源目录"+paths+"----->"+disPath_one+"----同步完成，进度{0}%\r\n".format(100))
		else:
			#sys.stdout.flush()
			sys.stdout.write(str(e)+"\r\n")
	child.close()
#开始遍历文件和目录，返回修改时间
def getMemus(path):
	f_new={}
	f_old=openOld('./log.txt')
	f=[]
	try:
		for root, dirs, files in os.walk(path, topdown=False):
			for name in files:
				contentPath=os.path.join(root, name)
				f_new.update({contentPath:os.stat(contentPath).st_mtime})
				if f_old.has_key(contentPath) == False or f_old[contentPath] != os.stat(contentPath).st_mtime:
					f.append(contentPath)
		print saveOld('./log.txt',f_new)
	except Exception as e:
		print e
		f=[]
	return f

	
	
if __name__ =='__main__':
	if '--help' in sys.argv or '-h' in sys.argv: 
		print "需要一个参数，第一个参数为源目录"
	elif len(sys.argv)<2:
		raise Exception("需要一个参数，第一个参数为源目录")
	configs=openConfig('./config.json')
	testPath=sys.argv[1]
	mkfile()
	
	'''
	#协程异步处理#copys(testPath,configs)
	tmp=[]
	for i,v in configs.items():
		tmp.append(gevent.spawn(copys,testPath,i,v))
	gevent.joinall(tmp)
	'''
	tmp=[]
	for i,v in configs.items():
		t =threading.Thread(target=copys,args=(testPath,i,v,))
		tmp.append(t)
	for t in tmp:
		t.start()
		t.join()
