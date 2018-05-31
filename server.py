from socket import *
import shelve
import time
import base64
import sys
def create_socket():
	try:
		sock=socket(AF_INET,SOCK_STREAM)
		return sock
	except Exception, e:
		print "[-]There is an Error:- "+str(e)
def bind_socket(sock,host,port):
	"""Input:host and port
		binds the server to the port
		returns none
	"""
	try:
		sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		sock.bind((host,port))
		sock.listen(5)#listening for maximum 5 connections
	except Exception, e:
		print"[-]There is an error:- "+str(e)
		time.sleep(20)
		bind_socket(sock,host,port)
def Conn_accept(sock):
	try:	
		New_sock,address=sock.accept()
		print("[+]Got connection from",address[0]+':'+str(address[1]))
		send_data(New_sock)
		New_sock.close()
	except Exception, e:
		print'[-]There is an error: '+str(e)
		Conn_accept()
def send_data(New_sock):
	try:
		Header_content={'HTML':'Content-Type: text/html\n',
						'CSS':'Content-Type: text/css\n',
						'javascript':'Content-Type: application/javascript\n',
						'Image':'Content-Type: image/jpeg\n'
						}
		#remeber these new line characters			
		header="HTTP/1.1 200 OK\n"
		request=New_sock.recv(2048)
		decode_request=request.decode('utf-8')
		print decode_request
		def send_images(decode_request,header):
			try:
				if decode_request.split()[1]=='/harish.jpg':
					Response=(header+Header_content['Image'])
				#	open the imagage encode it first then save it as txt then open it and decode it then send it
					image_encoded=open('encoded.txt')
					image_read=image_encoded.read()
					image=base64.decodestring(image_read)
					New_sock.send(Response+'\n'+image)
					#New_sock.send(image)
					
			except Exception ,erro:
				print str(erro)
		def send_structure(decode_request,header):
			try:
				if decode_request.split()[1]=='/':
					header+=Header_content['HTML']
					file=open('index.html','r')
				elif decode_request.split()[1]=="/style.css":
					header+=Header_content['CSS']
					file=open('style.css')
				elif decode_request.split()[1]=='/home.html':
					header+=Header_content['HTML']
					file=open('home.html','r')	
				elif decode_request.split()[1]=='/script.js':
					header+=Header_content['javascript']
					file=open('script.js')
				else:
					header+=Header_content['HTML']
					file=open('not.html')
				content=file.read()
				Total_response=(content).encode('utf-8')	
				New_sock.send(header+'\n'+Total_response)#Remeber to send new line after the headers
			except Exception,e:
				print str(e)	
		if decode_request.split()[0]=='GET':					
				send_images(decode_request,header)
				send_structure(decode_request,header)		
		else: 
			newlist=decode_request.split('\n')
			post_data=newlist[12].split('&')
			shelf=open('data.txt','a')
			for data in post_data:
				shelf.write(data+'\n')
			shelf.close()

		New_sock.close()
	except Exception, e:
		print'[-] Error: '+str(e)
def main():
	if len(sys.argv)>1:
		port=sys.argv[1]
  	else:
  		print "Specify a port"
  		sys.exi,headert(0)
	while True:
		socket=create_socket()
		bind_socket(socket,'',int(port))
		Conn_accept(socket)

if __name__=="__main__":
	main()



	
