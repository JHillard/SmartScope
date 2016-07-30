import usbtmc
instr = usbtmc.Instrument(0x1ab1,0x04ce)
import time
delay = .001

a = instr.ask('*IDN?'.encode('utf-8'))
print(a)
