import usbtmc
import time
instr = usbtmc.Instrument("USB::0x1ab1::0x04ce::INSTR")
instr.write("RUN")
time.sleep(1)
instr.write("STOP")
time.sleep(1)
instr.write("RUN")
time.sleep(1)
instr.write("STOP")
time.sleep(1)

instr.write("RUN")
time.sleep(1)
instr.write("STOP")
time.sleep(1)

instr.write("RUN")
time.sleep(1)
instr.write("STOP")
time.sleep(1)

instr.write("RUN")
time.sleep(1)
instr.write("STOP")
time.sleep(1)

instr.write("RUN")
time.sleep(1)
instr.write("STOP")
time.sleep(1)


instr.read(50)

