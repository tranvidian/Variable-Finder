import tkinter as tk            #https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
from tkinter import filedialog



def main():

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    with open(file_path, "r") as f:
        LinesOfCode = f.readlines()

    GrabFileName = (file_path.split("/")[-1]).split(".")
    FileGrabbedName = GrabFileName[0]+ "_" + GrabFileName[1]
    FileOutputTitle = f"OutputCPP_{FileGrabbedName}.txt"
    try: #makes file or write to existing file
        f2 = open( FileOutputTitle, "x")
    except:
        f2 = open( FileOutputTitle , "w")

    #Debug File
    DebugFileName = f"Debug{FileOutputTitle}"
    try:
        fDebug = open(DebugFileName, "x")
    except:
        fDebug = open(DebugFileName, "w")

    PreWrite(fDebug, f2)


    LineCounter = 1
    VariableCounter = 0
    for CodeLines in LinesOfCode: #Reads Per line

        # * lazy detection
        bNoParenthesesDetect = not ( "(" in CodeLines and ")" in CodeLines)
        bDefined = ";" in CodeLines                                                         # ! checks if it atleast normal, this natrually detects for certain macro or functions
        bNoVoidCheck = not "void" in CodeLines
        bNoCheckForCurlyBrackets = not ("{" in CodeLines or "}" in CodeLines)               #! Curly brackets means function as well
        bNoComments = not ("/*" in CodeLines)                                               # ! I want pointers as varaibles to be included but comments also uses "*" so Specific case of "*" is needed
        bNoForwardDeclareShort = not ( len(CodeLines.split()) < 2 and "class" in CodeLines) # ! looking out for shortcutted forward declares like this "class Ben;" vs "class Ben Name;" (an actual varaible with forward declare)
        # * lazy detection

        # ? if there is no Parentheses, void keyword, CurlyBrackets, no stars (comments) therefore it is a varaible
        if ( bNoParenthesesDetect and bDefined and bNoVoidCheck and bNoCheckForCurlyBrackets and bNoComments):
            VariableCounter += 1
            f2.write(f"{LineCounter} {CodeLines}")

        DebugToFile(fDebug, CodeLines, LineCounter, [bNoParenthesesDetect, bDefined, bNoVoidCheck, bNoCheckForCurlyBrackets, bNoComments, bNoForwardDeclareShort] )

        LineCounter += 1

    f2.write(f"Total Variables {VariableCounter}")
    f2.close()
    fDebug.close()


    LinePrepender( FileOutputTitle, f"Total Variables {VariableCounter} \nfrom file name {FileGrabbedName} located at:\n{file_path}" )
    CommandLineOutput( FileOutputTitle )

##///////////////////////////////////

def PreWrite(DebugFile, WriteToFile):
    DebugFile.write("{0:<150} {1:}\n".format(".", "(Debug) bNoParenthesesDetect / bDefined / bNoVoidCheck / bNoCheckForCurlyBrackets / bNoComments / bNoForwardDeclareShort")) #top definition
    WriteToFile.write("Reminder that it does not work 100%, it does not work against structs defintions, forward declaring (short format), and also comments correctly\n\n\n")

def DebugToFile( fileDebug , LineOfCode, CountedLines, Booleans):
        Line = LineOfCode.removesuffix("\n")
        FormatLineCode = f"{CountedLines} {Line}"
        #DebugLineCode = f"(Debug) bNPD: {bNoParenthesesDetect} / bD: {bDefined} / bNVC {bNoVoidCheck} / bNCFCB {bNoCheckForCurlyBrackets} / bNC {bNoComments}\n"
        DebugLineCode = f"(Debug) bNPD: {Booleans[0]} / bD: {Booleans[1]} / bNVC {Booleans[2]} / bNCFCB {Booleans[3]} / bNC {Booleans[4]} / bNFDS bNoForwardDeclareShort\n"
        FinalFormat = "{0:<150} {1:}".format(FormatLineCode , DebugLineCode)
        fileDebug.write(FinalFormat)


def LinePrepender(filename, line):      #https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def CommandLineOutput(FileName):
    with open(FileName, "r") as f3:
        print("Now outputting in Command Lines\n")
        print(f3.read())

if __name__=="__main__":
    main()
