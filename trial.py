import os
import subprocess
import numpy as np
gram=open("gram","w+")
gram.write("$word = ich | moechte | heute | Abend | ins | Kino | gehen;\n(SENT-START <$word> SENT-END)")
gram.close()
subprocess.call('HParse gram wdnet')
#os.system('HParse gram wdnet')
wlist=open("wlist","w+")
wlist.write("Abend\ngehen\nheute\nich\nins\nKino\nmoechte")
wlist.close()
subprocess.call('HDMan -m -w wlist -n monophones1 -l dlog dict german_lexicon.lex')
with open("dict", "r") as dict_in:
    buf = dict_in.readlines()

with open("dict", "w") as dict_out:
    for line in buf:
        if line == "Kino            k i n O sp\n":
            line = line + "SENT-END        sil\nSENT-START      sil\n"
        if line == "moechte         m OE C t at sp\n":
            line = line +  "silence         sil\n"            
        dict_out.write(line)
phones=["sil","sp"]
def check_phones(string_list,text):
    result=[]    
    for string in string_list:
        found=False
        with open(text) as f:
            for line in f:
                if string in line:
                    found=True                    
                    break
        result.append(found)
    result=np.array(result)
    return result
existance=check_phones(phones,"monophones1")
with open("monophones1", "a") as monophones1:
    monophones1.write(str(np.array(phones)[~existance][0])+"\n")
with open("words.mlf","w+") as words:
    words.write(
"""#!MLF!#\n"*/kino1.lab"\nich\nmoechte\nheute\nAbend\nins\nKino\ngehen\n.
#!MLF!#\n"*/kino2.lab"\nich\nmoechte\nheute\nAbend\nins\nKino\ngehen\n.
#!MLF!#\n"*/kino3.lab"\nich\nmoechte\nheute\nAbend\nins\nKino\ngehen\n.
#!MLF!#\n"*/kino4.lab"\nich\nmoechte\nheute\nAbend\nins\nKino\ngehen\n.
#!MLF!#\n"*/kino5.lab"\nich\nmoechte\nheute\nAbend\nins\nKino\ngehen\n.""")
with open("mkphones0.led","w+") as mkphones0:
    mkphones0.write("EX\nIS sil sil\nDE sp\n")
subprocess.call("HLEd -l '*' -d dict -i phones0.mlf mkphones0.led words.mlf")
with open("config", "w+") as config:
    config.write(
    """#Coding parameters\nSOURCEKIND = WAVEFORMAT\nSOURCEFORMAT = WAV\nTARGETKIND = MFCC_0_D_A
TARGETRATE = 100000.0\nSAVECOMPRESSED = T\nSAVEWITHCRC = T\nWINDOWSIZE = 250000.0\nUSEHAMMING = T
PREEMCOEF = 0.97\nNUMCHANS = 26\nCEPLIFTER = 22\nNUMCEPS = 12\nENORMALISE = F"""
    )