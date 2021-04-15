import serial # for serial port
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import time

#define the serial port. Pick one:
port = "/dev/tty.uart-88FF466E374A1C39" #For Mac

signature=[]
lines=[]

times=[]
notes=[]

count = 0
line = 0

note_img = mpimg.imread('/Users/maxiaomei/Desktop/phys319/project/code/note.png')
#imgplot = plt.imshow(note_img)

plt.figure()
plt.xlabel("Time (s)")
plt.ylabel("Line")
#function that gets called when a key is pressed:
with serial.Serial(port,9600,timeout = 0.050) as ser:
    print(ser.name)
    while(1): #loop forever
        data = ser.read(1) # look for a character from serial port - will wait for up to 50ms (specified above in timeout)
        if len(data) > 0: #was there a byte to read?
            count = count + 1               # increment number of notes counted
        # set start time on first hit
            if count == 1:
                start = time.time()
        # read data and time
            note=ord(data)
            t=time.time()-start
            
        # record time signature using first four beats
            if count <= 4:
                signature.append(t)
                plt.axvline(x=t, lw=1)      # plot lines
                if count > 1:               # plot double lines
                    plt.axvline(x=(signature[count-1]+signature[count-2])/2, lw=0.3)
                if count == 4:
                    wait = signature[3]+signature[1]
                    signature.append(wait)
                    line = line + 1
                    lines.append(line)
                    plt.axvline(x=signature[3]+((signature[1]+signature[0])/2), lw=0.3)
                    plt.axvline(x=t+signature[1], lw=1)
                continue
        # wait for signature to settle
            if t <= signature[4]:
                continue
        # increment line based on time signature
            if t < (signature[4]*line+signature[4]):
                line = line
            else:
                line = line + 1
        # shift to appropriate time based on time signature
            t = (t % signature[4])
        # shift to appropriate line based on time
            note = note - (100 * line)
            
        # print note and time
            print(t,note)                   # print note in terminal
            
        # plot note
            plt.axhline(y=note, lw=0.2)
            plt.axhline(y=note-10, lw=0.2)
            plt.axhline(y=note-20, lw=0.2)
            plt.axhline(y=note+10, lw=0.2)
            plt.axhline(y=note+20, lw=0.2)
            plt.scatter(t,note,s=7,c='b')
#            for x in range(note, note-300, 1):
#                plt.scatter(t,x,s=4, c='b')
#                times.append(t)
#                notes.append(x)
#            for x in range(note, note-100, 50):
#                plt.scatter(t,x,s=7,c='b')
#            plt.scatter(t,note-100,s=7,c='b')
            x = note
            while x > (note-30):
                x = x-4
                plt.scatter(t-0.008,x,s=0.5,c='b')

           
            times.append(t)
            notes.append(note)
#            plt.gca().axes.get_yaxis().set_visible(False)
            plt.gca().axes.get_xaxis().set_visible(False)
            plt.pause(0.05)
            

plt.show()
