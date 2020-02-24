import re
import sys
from InstructionLookup import InstructionLookup
from Utils import Utils


class BaseInstruction(object):
    def __init__(self, instrRegex):
        self.instrRegex = re.compile(instrRegex)

    def parseInstr(self, instr):
        match = self.instrRegex.match(instr)
        if not match:
            return '', ()

        groups = filter(lambda x: x is not None, match.groups())
        operator = groups[0]
        operands = groups[1:]

        return operator, operands


class XOTypeInstruction(BaseInstruction):
    def __init__(self):
        XOTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(R\d+)'
        super(XOTypeInstruction, self).__init__(XOTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(XOTypeInstruction, self).parseInstr(instr)
        if operator == 'add':
            return operator, (operands[0], operands[1], operands[2], '0', '266', '0')
        if operator == 'subf':
            return operator, (operands[0], operands[1], operands[2], '0', '40', '0')


class XTypeInstruction(BaseInstruction):
    def __init__(self):
        XTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(R\d+)'
        super(XTypeInstruction, self).__init__(XTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(XTypeInstruction, self).parseInstr(instr)
        if operator == 'and':
            return operator, (operands[1], operands[0], operands[2], '28', '0')
        if operator == 'nand':
            return operator, (operands[1], operands[0], operands[2], '476', '0')
        if operator == 'or':
            return operator, (operands[1], operands[0], operands[2], '444', '0')
        if operator == 'xor':
            return operator, (operands[1], operands[0], operands[2], '316', '0')
        if operator == 'sld':
            return operator, (operands[1], operands[0], operands[2], '27', '0')
        if operator == 'srd':
            return operator, (operands[1], operands[0], operands[2], '539', '0')
        if operator == 'srad':
            return operator, (operands[1], operands[0], operands[2], '794', '0')


class DTypeInstruction(BaseInstruction):
    def __init__(self):
        DTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(\S+)'
        super(DTypeInstruction, self).__init__(DTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(DTypeInstruction, self).parseInstr(instr)
        if operator == 'addi':
            return operator, (operands[0], operands[1], operands[2])
        if operator == 'addis':
            return operator, (operands[0], operands[1], operands[2])
        if operator == 'andi':
            return operator, (operands[0], operands[1], operands[2])
        if operator == 'ori':
            return operator, (operands[0], operands[1], operands[2])
        if operator == 'xori':
            return operator, (operands[0], operands[1], operands[2])


class XSTypeInstruction(BaseInstruction):
    def __init__(self):
        XSTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(\d+)'
        super(XSTypeInstruction, self).__init__(XSTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(XSTypeInstruction, self).parseInstr(instr)
        if operator == 'sradi':
            return operator, (operands[1], operands[0], operands[2], '413', '0', '0')


class DSTypeInstruction(BaseInstruction):
    def __init__(self):
        DSTypeRegex = r'(\w+)\s+(R\d+)\W\s+(\d+)\W(R\d+)\W'
        super(DSTypeInstruction, self).__init__(DSTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(DSTypeInstruction, self).parseInstr(instr)
        if operator == 'ld':
            return operator, (operands[0], operands[2], operands[1], '0')
        if operator == 'std':
            return operator, (operands[0], operands[2], operands[1], '0')


class MTypeInstruction(BaseInstruction):
    def __init__(self):
        MTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(\d+)\W\s+(\d+)\W\s+(\d+)'
        super(MTypeInstruction, self).__init__(MTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(MTypeInstruction, self).parseInstr(instr)
        if operator == 'rlwinm':
            return operator, (operands[1], operands[0], operands[2], operands[3], operands[4], '0')


class BTypeInstruction(BaseInstruction):
    def __init__(self):
        BTypeRegex = r'(\w+)\s+(\d+)\W\s+(\d+)\W\s+(\w+)'
        super(BTypeInstruction, self).__init__(BTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(BTypeInstruction, self).parseInstr(instr)
        if operator == 'bc':
            return operator, (operands[0], operands[1], operands[2], '0', '0')
        if operator == 'bca':
            return operator, (operands[0], operands[1], operands[2], '1', '0')


class ITypeInstruction(BaseInstruction):
    def __init__(self):
        ITypeRegex = r'(\w+)\s+(\w+)'
        super(ITypeInstruction, self).__init__(ITypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(ITypeInstruction, self).parseInstr(instr)
        if operator == 'b':
            return operator, (operands[0], '0', '0')
        if operator == 'ba':
            return operator, (operands[0], '1', '0')
        if operator == 'bl':
            return operator, (operands[0], '0', '1')

#################################################################################
# Following are custom defined parsing formats
#################################################################################


class X2TypeInstruction(BaseInstruction):
    def __init__(self):
        X2TypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)'
        super(X2TypeInstruction, self).__init__(X2TypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(X2TypeInstruction, self).parseInstr(instr)
        if operator == 'extsw':
            return operator, (operands[1], operands[0], '0', '986', '0')


class X3TypeInstruction(BaseInstruction):
    def __init__(self):
        X3TypeRegex = r'(\w+)\s+(\d+)\W\s+(\d+)\W\s+(R\d+)\W\s+(R\d+)'
        super(X3TypeInstruction, self).__init__(X3TypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(X3TypeInstruction, self).parseInstr(instr)
        if operator == 'cmp':
            return operator, ('0', operands[2], operands[3], '0', '0')


class D2TypeInstruction(BaseInstruction):
    def __init__(self):
        D2TypeRegex = r'(\w+)\s+(R\d+)\W\s+(\d+)\W(R\d+)\W'
        super(D2TypeInstruction, self).__init__(D2TypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(D2TypeInstruction, self).parseInstr(instr)
        if operator == 'lwz':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'stw':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'stwu':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'lhz':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'lha':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'sth':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'lbz':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'stb':
            return operator, (operands[0], operands[2], operands[1])


class D3TypeInstruction(BaseInstruction):
    def __init__(self):
        D3TypeRegex = r'(\w+)\s+(\d+)\W\s+(\d+)\W\s+(R\d+)\W\s+(\d+)'
        super(D3TypeInstruction, self).__init__(D3TypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(D3TypeInstruction, self).parseInstr(instr)
        if operator == 'cmpi':
            return operator, ('0', operands[2], operands[3])


class LATypeInstruction(BaseInstruction):
    def __init__(self):
        LATypeRegex = r'(\w+)\s+(R\d+)\W\s+(\w+)'
        super(LATypeInstruction, self).__init__(LATypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(LATypeInstruction, self).parseInstr(instr)
        return operator, (operands[0], '0', operands[1])


class InstructionParser:
    def __init__(self, labelsMap={}):
        self.instrObjMap = {
            'XO-TYPE': XOTypeInstruction,
            'X-TYPE': XTypeInstruction,
            'D-TYPE': DTypeInstruction,
            'XS-TYPE': XSTypeInstruction,
            'DS-TYPE': DSTypeInstruction,
            'M-TYPE': MTypeInstruction,
            'B-TYPE': BTypeInstruction,
            'I-TYPE': ITypeInstruction,
            # Following are custom defined parsing formats which ultimately
            # result in standard encoding formats only
            'D2-TYPE': D2TypeInstruction,
            'D3-TYPE': D3TypeInstruction,
            'X2-TYPE': X2TypeInstruction,
            'X3-TYPE': X3TypeInstruction,
            'LA-TYPE': LATypeInstruction

        }

        self.formatFuncMap = {
            'binary': lambda s, n: Utils.int2bs(s, n),
            'hex': lambda s, n: Utils.bs2hex(Utils.int2bs(s, n))
        }

        self.labelsMap = labelsMap

        self.instrLookup = InstructionLookup()
        self.instrObj = None

    def extractLabels(self, instr):
        if not instr:
            return '', ''

        split = instr.split(':', 1)

        if len(split) < 2:
            return '', instr

        return split[0], split[1].strip()

    def parse(self, instr):
        label, instr = self.extractLabels(instr)
        if not instr:
            return '', '', None

        operator = instr.split(' ')[0]
        instrType = self.instrLookup.type(operator)
        if not instrType:
            return '', '', None
            #sys.exit("Undefined Label")

        instrObj = self.instrObjMap[instrType]()
        operator, operands = instrObj.parseInstr(instr)

        operands = list(operands)
        if operator == 'bc':
            operands[2] = str(int(self.labelsMap[operands[2]], 16) - int('400000', 16))
        if operator == 'bca':
            operands[2] = str(int(self.labelsMap[operands[2]], 16) - int('400000', 16))
        if operator == 'b':
            operands[0] = str(int(self.labelsMap[operands[0]], 16) - int('400000', 16))
        if operator == 'ba':
            operands[0] = str(int(self.labelsMap[operands[0]], 16) - int('400000', 16))
        if operator == 'bl':
            operands[0] = str(int(self.labelsMap[operands[0]], 16) - int('400000', 16))
        if operator == 'la':
            operands[2] = str(int(self.labelsMap[operands[2]], 16) - int('10000000', 16))
        operands = tuple(operands)

        if label:
            operands = list(operands)
            if label not in self.labelsMap:
                operands[-1] = None

            operands[-1] = str(self.labelsMap[label])
            operands = tuple(operands)

        return instrType, operator, operands

    def convert(self, instr, format='binary', formatFunc=None, instrFieldSizes=(6, 26)):
        if not instr:
            return ''

        if formatFunc is None:
            formatFunc = self.formatFuncMap[format]

        instrType, operator, operands = self.parse(instr)
        if not operator:
            return ''

        if instrType == 'XO-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 1, 9, 1)
        if instrType == 'X-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 10, 1)
        if instrType == 'D-TYPE':
            instrFieldSizes = (6, 5, 5, 16)
        if instrType == 'XS-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 9, 1, 1)
        if instrType == 'DS-TYPE':
            instrFieldSizes = (6, 5, 5, 14, 2)
        if instrType == 'M-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 5, 5, 1)
        if instrType == 'B-TYPE':
            instrFieldSizes = (6, 5, 5, 14, 1, 1)
        if instrType == 'I-TYPE':
            instrFieldSizes = (6, 24, 1, 1)

        # Following are for custom defined parsing formats
        if instrType == 'X2-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 10, 1)
        if instrType == 'X3-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 10, 1)
        if instrType == 'D2-TYPE':
            instrFieldSizes = (6, 5, 5, 16)
        if instrType == 'D3-TYPE':
            instrFieldSizes = (6, 5, 5, 16)
        if instrType == 'LA-TYPE':
            instrFieldSizes = (6, 5, 5, 16)

        opcode = self.instrLookup.opcode(operator)
        convertedOpcode = formatFunc(opcode, instrFieldSizes[0])
        operands = map(lambda op: op.strip('R'), operands)
        convertedOperands = map(lambda (i, s): formatFunc(s, instrFieldSizes[i + 1]), enumerate(operands))

        convertedOutput = convertedOpcode + ''.join(convertedOperands)
        return convertedOutput


if __name__ == '__main__':
    # Test
    ip = InstructionParser()
    print ip.convert('add $6 $2 $4')
    print ip.convert('addi $2 $0 2', format='binary')
    print hex(int(ip.convert('addi $2 $0 2', format='binary'), 2))
