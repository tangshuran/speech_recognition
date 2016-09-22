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
    buf1 = dict_in.readlines()

with open("dict", "w") as dict_out:
    for line in buf1:
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
#!MLF!#\n"*/kino5.lab"\nich\nmoechte\nheute\nAbend\nins\nKino\ngehen\n.\n""")
with open("mkphones0.led","w+") as mkphones0:
    mkphones0.write("EX\nIS sil sil\nDE sp\n")
subprocess.call("HLEd -l * -d dict -i phones0.mlf mkphones0.led words.mlf")
with open("config", "w+") as config:
    config.write(
    """#Coding parameters\nSOURCEKIND = WAVEFORMAT\nSOURCEFORMAT = WAV\nTARGETKIND = MFCC_0_D_A
TARGETRATE = 100000.0\nSAVECOMPRESSED = T\nSAVEWITHCRC = T\nWINDOWSIZE = 250000.0\nUSEHAMMING = T
PREEMCOEF = 0.97\nNUMCHANS = 26\nCEPLIFTER = 22\nNUMCEPS = 12\nENORMALISE = F"""
    )
with open("codetr.scp","w+") as codetr:
    codetr.write(
    """train_wav/kino1.wav train_feature/kino1.mfc
train_wav/kino2.wav train_feature/kino2.mfc
train_wav/kino3.wav train_feature/kino3.mfc
train_wav/kino4.wav train_feature/kino4.mfc
train_wav/kino5.wav train_feature/kino5.mfc"""
    ) 
subprocess.call("HCopy -T 1 -C config -S codetr.scp")
with open("train.scp","w+") as train:
    train.write(
    """train_feature/kino1.mfc
train_feature/kino2.mfc
train_feature/kino3.mfc
train_feature/kino4.mfc
train_feature/kino5.mfc"""
    )
if not os.path.exists("hmm0"):
    os.makedirs("hmm0")
with open("config", "r") as config_in:
    buf2 = config_in.readlines()
with open("config", "w") as config_out:
    for line in buf2:
        if "SOURCEKIND" in line:
            line = "#"+line
        if "SOURCEFORMAT " in line:
            line = "#"+line 
        config_out.write(line)
subprocess.call("HCompV -C config -f 0.01 -m -S train.scp -M hmm0 proto")
with open("monophones1", "r") as monophones1:
    buf3 = monophones1.readlines()
with open("monophones0", "w") as monophones0:
    for line in buf3:
        if line !="sp\n":
            monophones0.write(line)
subprocess.call("java MakeHMMDefs proto monophones0")
#fix the shit format problem
with open("hmmdefs", "r") as hmmdefs_in:
    buf4 = hmmdefs_in.readlines()

with open("hmmdefs", "w") as hmmdefs_out:
    for line in buf4:
        if line != '"\n':  
            if "~h" in line:
                line = line.rstrip('\r"\n') + '"\n'
            hmmdefs_out.write(line)
os.rename("hmmdefs", "hmm0/hmmdefs")
subprocess.call("java GenerateMacros hmm0/vFloors")
os.remove("hmm0/vFloors")
os.rename("macros", "hmm0/macros")
if not os.path.exists("hmm1"):
    os.makedirs("hmm1")
subprocess.call("HERest -C config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm0/macros -H hmm0/hmmdefs -M hmm1 monophones0")