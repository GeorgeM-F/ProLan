from types import *
bind=['cyclet','let']
proc=['case','cycle','do','ouput']
func=['fun','and','join','NO','not','or','qnt','set','YES','.','_','+','-','*','/','=','<','>']
char=['newline','space']
errs=['instruction error','syntax error','definition error','argument defect error','argument type error','argument excess error','overflow error']
#instruction error: 'ERROR: no action specified'
#syntax error: 'ERROR: (***) in line (***) is incorrectly indented'
#definition error: 'ERROR: name (***) in line (***) is undefined'
#argument defect error: 'ERROR: not enough arguments for function (***) in line (***)'
#argument type error: 'ERROR: wrong type of arguments for function (***) in line (***)'
#argument excess error: 'ERROR: too many arguments for function (***) in line (***)'
#overflow error: 'ERROR: value of (***) in line (***) is too high to process'

#============ SIMPLIFIER ============#
def e(i,l):
    return l[i-1]
#============ SIMPLIFIER ============#



###============ PROGRAM BEGINS HERE ==========================================================================================================###



#============ BEGIN DECOMMENTER (removes comments) ============#
def dcmm(inp):
    outp=list(inp)   # prepare output
    for i in range(len(outp)):
        if "|" in outp[i]:
            tracker=0
            for j in range(len(outp[i])):
                if outp[i][j]=="|":
                    tracker=j
            while len(outp[i])>tracker:
                outp[i].pop(-1)
    return outp
#============ END DECOMMENTER (removes comments) ============#

#============ BEGIN FORMATTER (converts text blocks into code) ============#
def frmt(inp):
    outp=[]   # prepare output
    outpnl=[]   # prepare output line
    tracker=0
    for i in range(len(inp)):   # for each line of the input...
        for j in range(len(inp[i][0:1+tracker])):   # finishes tracker if line has new code (i.e.: at least 1 non-space character before tracker)
            if not(inp[i][j]==' '):
                tracker=0
        if not("_" in inp[i]) and tracker==0:   # copy normal lines as they are
            outp.append(inp[i])
        elif "_" in inp[i] and tracker==0:   # produces code for first text line in the block (i.e.: lines with the "_")
            outpnl=[]
            for j in range(len(inp[i])):
                if not(inp[i][j]=="_") and tracker==0:   # characters before the "_"
                    outpnl.append(inp[i][j])
                elif inp[i][j]=="_" and tracker==0:   # the "_"
                    tracker=j   # sets tracker to "_"'s position
                    outpnl.append('s')
                    outpnl.append('e')
                    outpnl.append('t')
                elif inp[i][j]==" " and inp[i][j-1]=="_" and not(tracker==0):   # space after the "_"
                    outpnl.append(' ')
                elif not(inp[i][j]=="_") and not(tracker==0) and inp[i][j-2]=="_":   # first character after the space after the "_"
                    if inp[i][j]==' ':   # exception for space
                        outpnl.append('space')
                    else:
                        outpnl.append('.')
                        outpnl.append(' ')
                        outpnl.append(inp[i][j])
                    outp.append(outpnl)
                elif not(inp[i][j]=="_") and not(tracker==0):   #other characters after the "_"
                    outpnl=[]
                    for s in range(tracker):   #add syntactic spatiator
                        outpnl.append(' ')
                    outpnl.append(' ')
                    outpnl.append(' ')
                    outpnl.append(' ')
                    outpnl.append(' ')
                    if inp[i][j]==' ':   # exception for space
                        outpnl.append('space')
                    else:
                        outpnl.append('.')
                        outpnl.append(' ')
                        outpnl.append(inp[i][j])
                    outp.append(outpnl)
        elif not("_" in inp[i]) and not(tracker==0):   # produces code for ulterior text lines in a text block (i.e.: lines without the "_")
            outpnl=[]
            for s in range(tracker):   #add syntactic spatiator
                outpnl.append(' ')
            outpnl.append(' ')
            outpnl.append(' ')
            outpnl.append(' ')
            outpnl.append(' ')
            outpnl.append('newline')
            outp.append(outpnl)
            outpnl=[]
            for j in range(len(inp[i])):
                outpnl=[]
                if j>tracker+1:
                    for s in range(tracker):   #add syntactic spatiator
                        outpnl.append(' ')
                    outpnl.append(' ')
                    outpnl.append(' ')
                    outpnl.append(' ')
                    outpnl.append(' ')
                    if inp[i][j]==' ':
                        outpnl.append('space')   #exception for space
                    else:
                        outpnl.append('.')
                        outpnl.append(' ')
                        outpnl.append(inp[i][j])
                    outp.append(outpnl)
    return outp
#============ END FORMATTER (converts text blocks into code) ============#

#============ BEGIN LEXER (recognizes words and assigns ariety to them) ============#
def lex(inp):
    outp=[]   #create output
    wrdnm=-1
    for i in range(len(inp)):
        for j in range(len(inp[i])):
            if not(inp[i][j]==' '):   #is this character a letter?
                if j==0 or (inp[i][j-1]==' '):   #is this character the first letter of a word?
                    wrdnm=wrdnm+1
                    outp.append([])   #add a new word to the output
                outp[wrdnm].append(inp[i][j])   #add this character to the last word
                try:   #ariety introduction
                    if (inp[i][j+1]==' ') and not (inp[i][j+2]==' '):   #is next char a space? and the next a letter?
                        ari=1
                        k=1
                        while True:   #read downwards to search for
                            try:
                                if (inp[i+k][j]==' '):   #is the character under it a space?
                                    if (inp[i+k][j+1]==' ') and not (inp[i+k][j+2]==' '):   #is next char a space? and the next a letter?
                                        ari=ari+1
                                    k=k+1
                                else:
                                    break
                            except:   #ERROR! last line of the text: there's nothing over
                                break
                        outp[wrdnm].append(ari)
                except:   #ERROR! last word of the line: there's nothing more
                    ari=0
                    outp[wrdnm].append(ari)
    inp.append([])   #put back the finisher
    return outp
#============ END LEXER (recognizes words and assigns ariety to them) ============#

#============ BEGIN CYPHRER (recognizes numbers and puts them together) ============#
def cyph(inp):
    outp=[]
    wrdnm=-1
    for i in range(len(inp)):
        check=True
        for j in range(len(inp[i])-1):
            check=check and (inp[i][j] in ['0','1','2','3','4','5','6','7','8','9','.'])
        if not check:
            outp.append(inp[i])
        elif check:
            num=''
            for j in range(len(inp[i])-1):
                num=str(num+inp[i][j])
            num=[num]
            num.append(inp[i][-1])
            outp.append(num)
    return outp
#============ END CYPHRER (recognizes numbers and puts them together) ============#

#============ BEGIN CHARACTERIZER (recognizes words and puts them together) ============#
def char(inp):
    outp=[]
    wrdnm=-1
    for i in range(len(inp)):
        check=True
        for j in range(len(inp[i])-1):
            check=check and (inp[i][j] in ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z'])
        if not check:
            outp.append(inp[i])
        elif check:
            word=''
            for j in range(len(inp[i])-1):
                word=str(word+inp[i][j])
            word=[word]
            word.append(inp[i][-1])
            outp.append(word)
    return outp
#============ END CHARACTERIZER (recognizes words and puts them together) ============#

#============ BEGIN PARSER (recognizes phrases) ============#
def parse(inp):
    outp=list(inp)
    while len(outp)>1:   # as long input has >1 elements
        for i in range(len(outp)):
            ari=outp[i][-1]
            if ari==0:
                continue
            arisum=0   # check next elements' ariety
            for j in range(ari):
                    arisum=arisum+outp[i+j+1][-1]
            if arisum==0:   # if next arguments have 0 ariety...
                express=[]   # start building inp[i]'s expression
                for j in range(ari+1):
                    express.append(outp[i+j])   # place arguments inside expression
                express.append(0)
                outp[i]=express   # replace inp[i] with corresponding expression
                for j in range(ari+1):
                    if j>0:
                        del outp[i+1]   # now that the arguments are placed within the expression, delete them ("inp[i+1]" is used instead of "inp[i+j]" because deletion decreases indexes)
                break
    return outp[0]
#============ END PARSER (recognizes phrases) ============#

#============ BEGIN DE-ARIETIZER (removes ariety from arguments) ============#
def dertcycle(inp):   # implicit inner cycle
    try:
        inp.remove(inp[len(inp)-1])
        for i in range(len(inp)):
            dertcycle(inp[i])
    except:
        pass

def dert(inp):   # explicit outer command
    outp=list(inp)
    dertcycle(outp)
    return outp
#============ END DE-ARIETIZER (removes ariety from arguments) ============#

#============ BEGIN COLLAPSER (removes useless parenthesis) ============#
def clpscycle(inp):   # implicit inner cycle
    for i in range(len(inp)):
        if len(inp[i])==1:
            inp[i]=inp[i][0]
        else:
            try:
                clpscycle(inp[i])
            except:
                pass

def clps(inp):   # explicit outer command
    outp=list(inp)
    clpscycle(outp)
    return outp
#============ END COLLAPSER (removes useless parenthesis) ============#



###============ UNFINISHED PART BEGINS HERE ============================================================================================================###





def eva(inp):   # EVALUATER (evaluates functions)
    try:
        if type(int(inp))==type(2):   # NUMBERS
            return float(inp)
    except:
        pass
    for i in range(len(inp)-1):   # loops if required (this piece of code must be placed after NUMBERS and before everything else)
        if inp[i+1][0] in func or inp[i+1] in func:
            inp[i+1]=eva(inp[i+1])
    if inp=='YES':   # TRUTH
        return True
    if inp=='NO':   # FALSEHOOD
        return False
    if inp[0]=='not':   # NEGATION
        return not(inp[1])
    if inp[0]=='and':   # CONJUNCTION
        res=True
        for i in range(len(inp)-1):
            res=res and (inp[i+1])
        return res
    if inp[0]=='or':   # DISJUNCTION
        res=False
        for i in range(len(inp)-1):
            res=res or (inp[i+1])
        return res
    if inp[0]=='=':   # EQUALITY
        res=True
        for i in range(len(inp)-2):
            res=res and (inp[i+1]==inp[i+2])
        return res
    if inp[0]=='<':   # INCREASE
        res=True
        for i in range(len(inp)-2):
            res=res and (inp[i+1]<inp[i+2])
        return res
    if inp[0]=='>':   # DECREASE
        res=True
        for i in range(len(inp)-2):
            res=res and (inp[i+1]>inp[i+2])
        return res
    if inp[0]=='-':   # OPPOSITE
        return -float(inp[1])
    if inp[0]=='/':   # INVERSE
        return 1/float(inp[1])
    if inp[0]=='+':   # SUM
        res=0
        for i in range(len(inp)-1):
            res=res+float(inp[i+1])
        return res
    if inp[0]=='*':   # PRODUCT
        res=1
        for i in range(len(inp)-1):
            res=res*float(inp[i+1])
        return res
    if inp[0]=='qnt':   # QUANTITY 
        return len(inp[1])
    if inp[0]=='set':   # SET 
        res=[]
        for i in range(len(inp)-1):
            res.append(inp[i+1])
        return res
    if inp[0]=='join':   # JOIN
        res=[]
        for i in range(len(inp)-1):
            for j in range(len(inp[i+1])):
                res.append(inp[i+1][j])
        return res
    if inp[0]=='.':   # CHARACTER
        return '.'+' '+inp[1]
    if inp[0]=='fun':   # FUNCTION (LAMBDA)
        return inp
#    if inp[0][0]=='fun':   # FUNCTION (LAMBDA)
#        function=list(inp[0][-1])
#        for i in inp[0]:
#            if i=0 or i=len(inp[0])-1:
#                pass
#            else:
#                repl(function,function[i],inp[i])
#        return function

def repl(inp,dnm,dfn):   # REPLACER (replaces every instance of dnm with inp)
    for i in range(len(inp)):
        if inp[i]==dnm:
            inp[i]=dfn
        try:
            repl(inp[i],dnm,dfn)
        except:
            pass

def goto(inp,dnm,dfn):   # JUMPER (for every instance of dnm in inp, does dfn)
    for i in range(len(inp)):
        if inp[i]==dnm:
            exe(dfn)
        else:
            exe(inp[i])
        try:
            goto(inp[i],dnm,dfn)
        except:
            pass

def exe(inp):   # EXECUTER (executes procedures)
    for i in range(len(inp)-1):
        if inp[i+1][0] in func:   # EVALUATER (evaluates functions)
            inp[i+1]=eva(inp[i+1])
    if inp[0]=='let':   # BLOCK
        for i in range(int((len(inp)-1)/2)):
            repl(inp[len(inp)-1],inp[(i+1)*2-1],inp[(i+1)*2])
        exe(inp[len(inp)-1])
    if inp[0]=='do':   # SEQUENTIAL
        for i in range(len(inp)-1):
            exe(inp[i+1])
    if inp[0]=='case':   # CONDITIONAL
        for i in range(int((len(inp)-1)/2)):
            if inp[(i+1)*2-1]:
                exe(inp[(i+1)*2])
    if inp[0]=='cycle':   # CYCLE
        while inp[1]:
            exe(inp[2])
    if inp[0]=='cyclet':   # BLOCK
        for i in range(int((len(inp)-1)/3)):
                repl(inp[len(inp)-1],inp[(i+1)*3-2],inp[(i+1)*3-1])
        while True:
            exe(inp[len(inp)-1])
            for i in range(int((len(inp)-1)/3)):
                repl(inp[len(inp)-1],inp[(i+1)*3-2],inp[(i+1)*3])
    if inp[0]=='output':   # DATA OUTPUT
        if inp[1]==True:   #show format for boolean values
            print('YES')
        elif inp[1]==False:
            print('NO')
        else:   #show format for other things
            print(eva(inp[1]))



###============ UNFINISHED PART ENDS HERE ==========================================================================================================###



print("DEMO   (by: GMF)")   # PROMPT (shell)
while True:
    print("ENTER PROGRAM:")
    code=[]
    while True:   # start entering
        line=list(input())
        code.append(line)
        if line==[]:
            break   # finish entering
    code.remove([])   # remove finisher
    print("CODE:")
    print(code)   # show code
    print()
    print("DECOMMENTED:")
    print(dcmm(code))   # show decommented
    print()
    print("FORMATTED:")
    print(frmt(dcmm(code)))   # show formatted
    print()
    print("LEXED:")
    print(lex(frmt(dcmm(code))))   # show lexed
    print()
    print("CYPHERED:")
    print(cyph(lex(frmt(dcmm(code)))))   # show cyphered
    print()
    print("CHARACTERIZED:")
    print(char(cyph(lex(frmt(dcmm(code))))))   # show characterized
    print()
    print("PARSED:")
    print(parse(char(cyph(lex(frmt(dcmm(code)))))))   # show parsed
    print()
    print("DEARIETIZED:")
    print(dert(parse(char(cyph(lex(frmt(dcmm(code))))))))   # show dearietized
    print()
    print("COLLAPSED:")
    print(clps(dert(parse(char(cyph(lex(frmt(dcmm(code)))))))))   # show collapsed
    print()
    print("PROGRAM RESULT:")
    exe(clps(dert(parse(char(cyph(lex(frmt(dcmm(code)))))))))   # executes program
    print()



###============ PROGRAM ENDS HERE ============================================================================================================###
