
# coding: utf-8

# In[1]:

import numpy
import numpy as np
import matplotlib.pyplot as plot
import time as TIME
import csv
import usbtmc

#CONSTANTS
TIME_LENGTH = 600


# In[ ]:


r = usbtmc.usb_instrument()
s1 = r.sample_norm("CHAN1")
print("Sample Captured")


# In[ ]:

data = numpy.frombuffer(s1, 'B')
print(data)
voltscale = float( r.ask(":CHAN1:SCAL?", length=20))
voltageOffset = float( r.ask(":CHAN1:OFFS?", length=20))
timescale = float( r.ask(":TIM:SCAL?", length = 20))
timeOffset = float( r.ask(":TIM:OFFS?", length =20))


# In[2]:

def sample(channel="CHAN1"):
    dtemp = r.sample_norm(channel)
    if len(dtemp) < TIME_LENGTH:
        raise "Device unresponsive. Please Try again."
    voltscale = float( r.ask(":CHAN1:SCAL?", length=20))
    voltageOffset = float( r.ask(":CHAN1:OFFS?", length=20))
    timescale = float( r.ask(":TIM:SCAL?", length = 20))
    timeOffset = float( r.ask(":TIM:OFFS?", length =20))
    weird_offset = 11 
    data = data*-1+255
    data = data[weird_offset:]
    data = (data - 130.0 - voltageOffset/voltscale*25) / 25 * voltscale
    return data
    
def writeSample(filename, data, time):
    with open(filename, 'wb') as csvfile:
        cartographer = csv.writer(csvfile, delimiter = " ",
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0,len(data)):
            cartographer.writerow([str(data[i]), str(time[i])])
            
def graphSample(anex, save = False, img_name = str(TIME.strftime("%H%M%S"))): #anex=(data,time)
    
    
    data = anex[0,:]
    t = anex[1,:]
    # # See if we should use a different time axis
    if (t[599] < 1e-3):
        t = t * 1e6
        tUnit = "uS"
    elif (time[599] < 1):
        t = t * 1e3
        tUnit = "mS"
    else:
        tUnit = "S"


    # Plot the data
    newFig = plot.figure()
    plot.plot(t, data)
    plot.title("Oscilloscope Channel 1")
    plot.ylabel("Voltage (V)")
    plot.xlabel("Time (" + tUnit + ")") #Relabel tUnit if re-enabling scale
    plot.xlim(t[0], t[599])
    if(save): plot.savefig(img_name)
    plot.show()
    


# In[ ]:

weird_offset = 11 
data = data*-1+255
data = data[weird_offset:]
data = (data - 130.0 - voltageOffset/voltscale*25) / 25 * voltscale


#

# In[3]:

timescale = 1
time = numpy.arange(-300.0/50*timescale, 300.0/50*timescale, timescale/50.0)
fake_data = numpy.arange(1000.0/50*timescale, 1600.0/50*timescale, timescale/50.0)
package = np.vstack((fake_data,time))
np.savetxt("test.csv", package, delimiter=",")
# writeSample("Test.csv", fake_data, time)
new_pk = np.loadtxt("test.csv", delimiter=",")
print(new_pk)
graphSample(package, save=True)
