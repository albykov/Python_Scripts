fname = r'D:\TEMP\test15m\test2\t2_source_Strength_draft.txt'
fnameOut = r'D:\TEMP\test15m\test2\t2_source_Strength_draft_'

fnameOuts = {}
splitter = 1400000
#text_file = open(fnameOut, "a")

i = 0
current_fn_postf = 0
text_file = open(fnameOut+str(current_fn_postf), "a")
with open(fname) as f:
    for line in f:
        if i > 0:
            if i//splitter+1 > current_fn_postf:
                print ('----------------'+str(splitter))
                text_file.close()
                text_file = open(fnameOut+str(current_fn_postf)+'.csv', "a")
                current_fn_postf = i//splitter+1
            #z = round(float(line.split(',')[2].strip()), 3)
            #x = round(float(line.split(',')[3].strip()), 3)
            #y = round(float(line.split(',')[4].strip()), 3)
            id_text = line.split(',')[0].strip()
            val_text = round(float(line.split(',')[2].strip()), 3)
            #outp = str(x) + ' ' + str(y) + ' ' + str(z)+ "\n"
            outp = str(id_text) + ' ' + str(val_text) + "\n"
            print i, outp
            text_file.write(outp)
        i = i + 1

f.close()
text_file.close()