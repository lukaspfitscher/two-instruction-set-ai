from random        import randint  as rnd
from bitarray      import bitarray as b		# pip3 install bitarray
from bitarray.util import ba2int,int2ba
import time
srt_tme = time.time() 

#import os; os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
#import pygame; pygame.init() #import and init pygame to draw
#screen = pygame.display.set_mode((1300,950))#create window
#rectsicz = 4;rows = 6

#   2^5=32  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
ais    = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','?','?','?','?','?']  #alphapet in string

qststr = [
'zero plus zero  ','zero plus one   ','one plus zero   ','one plus one    ','zero plus two   ','one plus two    ',
'five plus one   ','ten plus six    ','two plus four   ','two plus two    ','seven plus one  ','one plus six    ',
'color sky       ','color wood      ','color blood     ','color sun       ','color grass     ','write nothing   ',
'color glas      ','define an hour  ','your creator    ','say hi          ','firs element    ','your country    ',
'say hallo       ','say mula        ','most element air','write rocket    ','second element  ','third element   ',
'write all e     ','write all f     ','write all s     ','write all g     ','write all t     ','write all h     ',
'write all a     ','write all w     ','write all y     ','write all b     ','write all z     ','write all o     ',
'write all q     ','write all n     ','write all d     ','write all k     ','write all c     ','write all s     ',
'write all d     ','write all u     ','write all k     ','write all r     ','write all m     ','write all i     ']#string array containing questions string
awrstr = [
'zero            ','one             ','one             ','two             ','two             ','three           ',
'six             ','onesix          ','six             ','four            ','eigh            ','seven           ',
'blue            ','brown           ','red             ','yellow          ','green           ','                ',
'transparent     ','sixteen minuts  ','lukas pfitscher ','hi              ','hydrogen        ','italy           ',
'hallo           ','mula            ','nitrogen        ','rocket          ','helium          ','lithium         ',
'eeeeeeeeeeeeeeee','ffffffffffffffff','ssssssssssssssss','gggggggggggggggg','tttttttttttttttt','hhhhhhhhhhhhhhhh',
'aaaaaaaaaaaaaaaa','wwwwwwwwwwwwwwww','yyyyyyyyyyyyyyyy','bbbbbbbbbbbbbbbb','zzzzzzzzzzzzzzzz','oooooooooooooooo',
'qqqqqqqqqqqqqqqq','nnnnnnnnnnnnnnnn','dddddddddddddddd','kkkkkkkkkkkkkkkk','cccccccccccccccc','ssssssssssssssss',
'dddddddddddddddd','uuuuuuuuuuuuuuuu','kkkkkkkkkkkkkkkk','rrrrrrrrrrrrrrrr','mmmmmmmmmmmmmmmm','iiiiiiiiiiiiiiii']#string array containing answer string

amt_chg			= 10					#initial amount changes
cntbitssign		= 5						#count bits per sign
cntletrqest		= len(qststr[0])		#= 16, count letters per question
cntbitqest		= cntbitssign * len(qststr[0])	#bits per question
cntqst			= len(qststr)			#= 36, count questions, answers
cnttotqes		= cntbitssign*len(qststr[0])*len(qststr) #total bits all questions
qstbin			= [b('')]*cntqst		#questions array in bits
awrbin			= [b('')]*cntqst		#answer    array in bits
cntbitsqest		= cntletrqest*cntbitssign #16*5=80, lengh in bits of a question/answer
sec_ctr			= len(qststr)			#end section counter in bits, will increse on every new question
sec_inp			= sec_ctr				#start section input
sec_otp			= sec_inp + cntbitsqest	# 3+80 cntbitsqest = 80, start section output
sec_end			= sec_otp + cntbitsqest	#83+80=163, start section end
var_end			= 250					#end of variable section in bits
var_lgh			= var_end-sec_end

al 				= 18			#adress lenght cmd_lgh
sz 				= 2**al			#2^13=8192,2^16=65536,2^19=524288, storage size 2

#command sections
csc_b1			= 1 			#command identification lenght
csc_b2			= csc_b1+al		#command end first adress
csc_b3			= csc_b1+2*al	#command end second adress
csc_ed			= csc_b1+3*al	#command end third adress
cmd_lgh			= csc_b1+3*al 	#13=204,16=1337,19=9039,,command lenght (2^16/(16*3+1))

cnt_cmd			= int((sz-var_end)/cmd_lgh)	#count of commands

cycles_qestion	= cntbitqest * 2#cycles per question just a rough number

print("")
print("section end counter:   "+str(len(qststr)))
print("section end in/out:    "+str(sec_end))
print("section end variabl    "+str(var_end))
print("varaible section size: "+str(var_lgh))
print("bit question:          "+str(int(cntbitqest)))
print("bit question total:    "+str(cnttotqes))
print("bit program lenght:    "+str(sz))
print("total commands:        "+str(int(cnt_cmd)))
print("commands per question: "+str(int(cnt_cmd/cntqst)))
print("cycles per question:   "+str(int(cycles_qestion)))
print("")

n1				= b('0'*sz)	#contains the net witch is currently the best
n2				= b('0'*sz)	#contains the net witch is runned but edits itself
g1				= 0			#goodness of the currently best net
g2				= 0			#goodness of the tested net
lst_awr			= b('0'*cntbitsqest) #needed to declare her cause it has to be the lengh

#print('nett architetur: ') #maby print all variables to have a better overview

'''def convstringtobits(arraystring,arraybin):
 ctr_sea = 0 #select element of the array
 while ctr_sea < cntqst:
  ctr_slt = 0 #select letter
  while ctr_slt < len(qststr[0]):
   ctr_sar==0:qstbin[ctr_sea]=qstbin[ctr_sea]+int2ba(ais.index(qststr[ctr_sea][ctr_slt]),5) 
   ctr_slt+=1
  ctr_sea+=1

convstringtobits(qststr,qstbin)# questions
convstringtobits(awrstr,awrbin)# answers'''

# convert string to bit #################################################################################
ctr_sar = 0 #select array
while ctr_sar < 2:
 ctr_sea = 0 #select element of the array
 while ctr_sea < cntqst:
  ctr_slt = 0 #select letter
  while ctr_slt < len(qststr[0]):
   if ctr_sar==0:qstbin[ctr_sea]=qstbin[ctr_sea]+int2ba(ais.index(qststr[ctr_sea][ctr_slt]),5) # questions
   if ctr_sar==1:awrbin[ctr_sea]=awrbin[ctr_sea]+int2ba(ais.index(awrstr[ctr_sea][ctr_slt]),5) # answers
   ctr_slt+=1
  ctr_sea+=1
 ctr_sar+=1

def randomcommand():  x = int2ba(rnd(0,cnt_cmd-1)*cmd_lgh+var_end,al);return x
def randomvariable(): x = int2ba(rnd(0,var_end-1),al);return x

option = input('write 1 for new, 2 for saved, 3 for testing, 4 for 200 times change:') #testing sets changes to zero

if option == '1':
 ctr_chg = 0 #counter changes in the programm
 while ctr_chg < cnt_cmd: #amount changes
  rnd_cmd = rnd(0,1) #random command
  rnd_adr = ctr_chg*cmd_lgh+var_end	#random valid adresses of a command in dec
  if rnd_cmd == 0: n2[rnd_adr:rnd_adr+cmd_lgh]=b('0')+randomvariable()+randomvariable()+randomcommand() #random move command
  if rnd_cmd == 1: n2[rnd_adr:rnd_adr+cmd_lgh]=b('1')+randomvariable()+randomcommand()+ randomcommand() #random jump command
  ctr_chg += 1
 #n1 = n2.copy()
 #print(n2)
else: #for option 2 and 3
 if option == '3': amt_chg = 0 #3 stands for testing
#copy saved array to internal array####################################################
 f = open("program.txt","r")
 savdpogm = f.read()[10:-2]
 cntrsvdprog = 0 #counter saved program
 while cntrsvdprog < sz: #sz: storage size
  if savdpogm[cntrsvdprog] == '0': n2[cntrsvdprog] = 0
  else: n2[cntrsvdprog] = 1
  cntrsvdprog += 1
  
 if option == '4':
  amtchanglocalmin = 0
  while amtchanglocalmin < 200:
   print("hallo")
   rnd_cmd = rnd(0,1)							#random command
   rnd_adr = rnd(0,cnt_cmd-1)*cmd_lgh+var_end	#random valid adresses of a command in dec
   if rnd_cmd == 0: n2[rnd_adr:rnd_adr+cmd_lgh]=b('0')+randomvariable()+randomvariable()+randomcommand() #random move command
   if rnd_cmd == 1: n2[rnd_adr:rnd_adr+cmd_lgh]=b('1')+randomvariable()+randomcommand()+randomcommand() #random jump command
   amtchanglocalmin += 1

#inputs ################################################################################
ctr_pgm = 0 #counter program
while True: #main loop
 cp = var_end #comandpointer, program start where the variable section ends, always reset it when calculating new program
 ctr_pgm += 1
 ctr_ipt  = 0 #input counter
 

 while ctr_ipt < cntqst:
  n2[      0:sec_ctr] = int2ba(ctr_ipt,sec_ctr)	#ctr_ipt = inputcounter
  n2[sec_inp:sec_otp] = qstbin[ctr_ipt]			#input question
  n2[sec_otp:sec_end] = b('0')*cntbitsqest

  #cp = var_end #reset after every question, not needed just for testing if its runns better

#kernl ##################################################################################
  ctr_cpi = 0 #counter command per input
  while ctr_cpi < cycles_qestion: #cycles per question

#   if option == '3': #comment out for speed
#    print('%8s'%str(cp)+'%3s'%str(n2[cp])+'%4s'%str(ba2int(n2[cp+csc_b1:cp+csc_b2]))+'%3s'%str(n2[ba2int(n2[cp+csc_b1:cp+csc_b2])])+
#    '%8s'%str(ba2int(n2[cp+csc_b2:cp+csc_b3]))+'%3s'%str(n2[ba2int(n2[cp+csc_b2:cp+csc_b3])])+'%8s'%str(ba2int(n2[cp+csc_b3:cp+csc_ed]))+
#    '%3s'%str(n2[ba2int(n2[cp+csc_b3:cp+csc_ed])]))
#    print(str(n2[0:sec_end])[10:-2])
#    time.sleep(0.5)

   tgt = n2[ba2int(n2[cp+csc_b1:cp+csc_b2])]
   if n2[cp] == 0: #move_bit_command
    n2[ba2int(n2[cp+csc_b2:cp+csc_b3])]=tgt 		#destiny = target
    cp=ba2int(n2[cp+csc_b3:cp+csc_ed])				#jump
   else: #jump_bit_command
    if tgt == 0:cp=ba2int(n2[cp+csc_b2:cp+csc_b3])	#jumpifzero
    else:cp=ba2int(n2[cp+csc_b3:cp+csc_ed])			#jumpifone
   ctr_cpi += 1
   
#"""
  if option == '3': #comment out for speed
   asw = '' #answer
   ctrlaw = 0 #counter last answer
   while ctrlaw < cntletrqest: #ais: alphapet in string
    asw = asw + ais[ba2int(n2[sec_otp+ctrlaw*cntbitssign:sec_otp+(ctrlaw+1)*cntbitssign])] #length letter input, cntbitssign=5, len(lst_awr)=16*5
    ctrlaw+=1
   print("%3s"%str(ctr_ipt)+' question : '+str(qststr[ctr_ipt])+' '+str(qstbin[ctr_ipt])[10:-2])
   print("%3s"%str(ctr_ipt)+' answr bst: '+str(awrstr[ctr_ipt])+' '+str(awrbin[ctr_ipt])[10:-2])
   print("%3s"%str(ctr_ipt)+' answr net: '+str(asw)+' '+str(n2[sec_otp:sec_end])[10:-2])
   print('################################################################################################################')
   time.sleep(1)
#"""

#calc goodness
  ctr_gns = 0
  while ctr_gns < cntbitsqest:
   if n2[sec_otp+ctr_gns] == awrbin[ctr_ipt][ctr_gns]: g2 +=1
   ctr_gns+=1
  ctr_ipt+=1
 
#decid which net ###############################################################################
 if g2 >= g1: #calculated programm is equal or better than old one 
  n2[0:var_end] = b('0')*var_end #resets variable section, set all to zero
  n1 = n2.copy() #copy arrays n1 = n2 does not work
  g1 = g2 #update goodness
 else: n2 = n1.copy() #calculated program is worse than old one
 g2output = g2 #for output, goodness of the calculated nett
 g2 = 0 #set it at last so it can print it out

#random command #################################################################################
 ctr_chg = 0 #counter changes in the programm
 while ctr_chg < amt_chg: #amount changes
  rnd_cmd = rnd(0,1)							#random command
  rnd_adr = rnd(0,cnt_cmd-1)*cmd_lgh+var_end	#random valid adresses of a command in dec
  if rnd_cmd == 0: n2[rnd_adr:rnd_adr+cmd_lgh]=b('0')+randomvariable()+randomvariable()+randomcommand() #random move command
  if rnd_cmd == 1: n2[rnd_adr:rnd_adr+cmd_lgh]=b('1')+randomvariable()+randomcommand()+randomcommand() #random jump command
  ctr_chg += 1

# user interface ################################################################################
 if ctr_pgm % 10 == 0: #command line update increse number for efficiency
  print("%6s"%str(int(time.time()-srt_tme))+"%10s"%str(ctr_pgm)+' g1:'+str(cntbitsqest*cntqst)+'/'+str(g1)+"%10s"%str(g2output))
  if ctr_pgm % 100 == 0: #saving nett, if programm counter is divideable by 100
   textfile = open("program.txt","w")
   textfile.write(str(n1))
   textfile.close()
   

'''
  screen.fill((0,0,0))
  cdraw = 0
  while cdraw < sz:
   xcord =    (cdraw % (cmd_lgh*rows))*rectsicz
   ycord = int(cdraw / (cmd_lgh*rows))*rectsicz #int necesary to round down
   if n1[cdraw] == 1:
    pygame.draw.rect(screen,(255,255,255),(xcord,ycord,rectsicz,rectsicz))#cross flat 249 is the half -1 cause its 2 thick
   cdraw += 1
  ctr_arw = 0
  while ctr_arw < 20:
   arw_srt = rnd(0,cnt_cmd-1)*cmd_lgh+var_end
   arw_end = ba2int(n1[arw_srt+csc_b3:arw_srt+csc_ed])
   arw_srt_x =    (arw_srt % (cmd_lgh*rows))*rectsicz+0.5*rectsicz
   arw_end_x =    (arw_end % (cmd_lgh*rows))*rectsicz+0.5*rectsicz
   arw_srt_y = int(arw_srt / (cmd_lgh*rows))*rectsicz+0.5*rectsicz #int necesary to round down
   arw_end_y = int(arw_end / (cmd_lgh*rows))*rectsicz+0.5*rectsicz #int necesary to round down
   pygame.draw.line(screen,(0,0,255),(arw_srt_x,arw_srt_y),(arw_end_x,arw_end_y),5)
   arw_srt = rnd(0,cnt_cmd-1)*cmd_lgh+var_end
   arw_end = ba2int(n1[arw_srt+csc_b1:arw_srt+csc_b2])
   arw_srt_x =    (arw_srt % (cmd_lgh*rows))*rectsicz+0.5*rectsicz
   arw_end_x =    (arw_end % (cmd_lgh*rows))*rectsicz+0.5*rectsicz
   arw_srt_y = int(arw_srt / (cmd_lgh*rows))*rectsicz+0.5*rectsicz #int necesary to round down
   arw_end_y = int(arw_end / (cmd_lgh*rows))*rectsicz+0.5*rectsicz #int necesary to round down
   pygame.draw.line(screen,(0,255,0),(arw_srt_x,arw_srt_y),(arw_end_x,arw_end_y),5)
   #arw_srt = arw_end
   #arowmovestrt = ba2int(n1[arw_srt+csc_b3:arw_srt+csc_ed])
   ctr_arw +=1
  pygame.display.flip() #updates the screen
'''
