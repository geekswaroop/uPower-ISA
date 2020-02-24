import sys
import getopt

from InstructionParser import InstructionParser


class Assembler(object):
    def __init__(self, infilenames, outfilename):
        self.infilenames = infilenames
        self.outfilename = outfilename

    def stripComments(self, line):
        if not line:
            return ''

        cleaned = line
        if line.find('#') != -1:
            cleaned = line[0:line.find('#')]  # Get rid of anything after a comment.

        return cleaned

    def buildLabelsMap(self, lines):
        labelsMap = {}
        initializedMap = {}

        text_base_address = int('400000', 16)
        offset = 0
        data_base_address = int('10000000', 16)
        currentp = 0

        flag = 0
        if lines[0] == '.text':
            for i in range(0, len(lines) - 1):
                if lines[i] == '.text':
                    continue
                if lines[i] == '.data':
                    flag = i
                    break
                split = lines[i].split(':', 1)
                if len(split) > 1:
                    label = split[0]
                    labelsMap[label] = hex(text_base_address + (4 * offset))
                else:
                    offset = offset + 1

            for i in range(flag, len(lines)):
                if lines[i] == '.data':
                    continue
                split = lines[i].split(':', 1)
                label = split[0]
                y = split[1].split()
                if len(y) > 2:
                    y[1] = y[1].strip('\'')
                    y[len(y) - 1] = y[len(y) - 1].strip('\'')
                    value = ''
                    for j in range(1, len(y)):
                        value = value + y[j] + ' '
                    dataval = value[0:len(dataval) - 2]
                else:
                    dataval = y[1]

                if y[0] == '.word':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    arr = dataval.split()
                    if len(arr) > 1:
                        for i in range(0, len(arr)):
                            initializedMap[addressc] = arr[i].strip(',')
                            addressc = hex(int(addressc, 16) + 4)
                        currentp += (4 * len(arr))
                    else:
                        initializedMap[addressc] = dataval
                        currentp += 4

                if y[0] == '.halfword':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    initializedMap[addressc] = dataval
                    currentp += 2

                if y[0] == '.double':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    initializedMap[addressc] = dataval
                    currentp += 8

                if y[0] == '.byte':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    initializedMap[addressc] = dataval
                    currentp += 1

                if y[0] == '.asciiz':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    initializedMap[addressc] = dataval
                    currentp += len(dataval)

        if lines[0] == '.data':
            for i in range(0, len(lines) - 1):
                if lines[i] == '.data':
                    continue
                if lines[i] == '.text':
                    flag = i
                    break
                split = lines[i].split(':', 1)
                label = split[0]
                y = split[1].split()
                if len(y) > 2:
                    y[1] = y[1].strip('\'')
                    y[len(y) - 1] = y[len(y) - 1].strip('\'')
                    value = ''
                    for j in range(1, len(y)):
                        value = value + y[j] + ' '
                    dataval = value[0:len(value) - 1]
                else:
                    dataval = y[1]

                if y[0] == '.word':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    arr = dataval.split()
                    if len(arr) > 1:
                        for i in range(0, len(arr)):
                            initializedMap[addressc] = arr[i].strip(',')
                            addressc = hex(int(addressc, 16) + 4)
                        currentp += (4 * len(arr))
                    else:
                        initializedMap[addressc] = dataval
                        currentp += 4

                if y[0] == '.halfword':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    initializedMap[addressc] = dataval
                    currentp += 2

                if y[0] == '.double':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    initializedMap[addressc] = dataval
                    currentp += 8

                if y[0] == '.byte':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    initializedMap[addressc] = dataval
                    currentp += 1

                if y[0] == '.asciiz':
                    addressc = hex(data_base_address + currentp)
                    labelsMap[label] = addressc
                    initializedMap[addressc] = dataval
                    currentp += len(dataval)

            for i in range(flag, len(lines)):
                if lines[i] == '.text':
                    continue
                split = lines[i].split(':', 1)
                if len(split) > 1:
                    label = split[0]
                    labelsMap[label] = hex(text_base_address + (4 * offset))
                else:
                    offset = offset + 1

        return labelsMap, initializedMap

    def mergeInputFiles(self):
        outlines = []

        for filename in self.infilenames:
            with open(filename) as f:
                outlines += f.readlines()

            f.close()

        return outlines

    def AssemblyToHex(self):
        '''given an ascii assembly file , read it in line by line and convert each line of assembly to machine code
        then save that machinecode to an outputfile'''
        inlines = self.mergeInputFiles()
        outlines = []

        lines = map(lambda line: self.stripComments(line.rstrip()), inlines)  # get rid of \n whitespace at end of line
        lines = filter(lambda line: line, lines)

        # print lines

        labelsMap, initializedMap = self.buildLabelsMap(lines)
        parser = InstructionParser(labelsMap=labelsMap)

        outlines = map(lambda line: parser.convert(line, format='binary'), lines)
        outlines = filter(lambda line: line, outlines)

        with open(self.outfilename, 'w') as of:
            of.write('v0.1 raw\n')
            for outline in outlines:
                of.write(outline)
                of.write("\n")
        of.close()

        return labelsMap, initializedMap, outlines


if __name__ == "__main__":
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if (len(sys.argv) < 4) or ('-i' not in sys.argv) or ('-o' not in sys.argv):
        print('Usage: python Assembler.py -i <inputfile.asm>[ <inputfile2.asm> <inputfile3.asm> ...] -o <outputfile.hex>')
        sys.exit(2)

    inputfiles = sys.argv[sys.argv.index('-i') + 1: sys.argv.index('-o')]
    outputfile = sys.argv[sys.argv.index('-o') + 1]

    assembler = Assembler(inputfiles, outputfile)
    labelsMap, initializedMap, outlines = assembler.AssemblyToHex()

    def printmaps():
        print "\n"
        print "LABELS MAP"
        for key in sorted(labelsMap.keys()):
            print key + ":" + str(labelsMap[key])
        print "\n"
        print "DATA MAP"
        for key in sorted(initializedMap.keys()):
            print key + ":" + str(initializedMap[key])
        print "\n"

    printmaps()

    ##################################################################################################
    # END OF ASSEMBLER WHICH RETURNS 2 TABLES AND ARRAY OF BINARY LINES(OUTLINE)
    ##################################################################################################
