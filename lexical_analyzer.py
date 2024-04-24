#importação das bibliotecas
import sys
import string
import os

class LexicalAnalyzer():
    # Lista de palavras reservadas da linguagem
    reservedWords = ['algoritmo', 'principal', 'variaveis', 'constantes', 'registro', 'funcao', 'retorno', 'vazio', 'se', 'senao', 'enquanto', 'leia', 'escreva', 'inteiro', 'real', 'booleano', 'char', 'cadeia', 'verdadeiro', 'falso']
    # Símbolos da linguagem (pontuação e espaço)
    symbols = string.punctuation.replace("_", "") + " "
    # Letras do alfabeto
    letters = string.ascii_letters
    # Operadores aritméticos
    operatorsArithmetic = ['+', '-', '*', '/', '++', '--']
    # Operadores relacionais
    operatorsRelational = ['==', '!=', '>', '>=', '<', '<=', '=']
    # Operadores lógicos
    operatorsLogical = ['&&', '||', '!']
    # Dígitos
    digits = string.digits
    # Delimitadores
    delimiters = [';', ',', '(', ')', '{', '}', '[', ']', '.']
    # Diretório dos arquivos de entrada.
    dir_input = 'files/input_lexical'
    # Diretório dos arquivos de saída.
    dir_output = 'files/output_lexical'

    def __init__(self):
        pass

    def isReserved(self, index):
        # Verifica se o índice está presente na lista de palavras reservadas da linguagem
        return index in self.reservedWords

    def isSymbol(self, index):
        # Verifica se o índice está presente na lista de símbolos da linguagem
        return index in self.symbols

    def isLetter(self, index):
        # Verifica se o índice é uma letra do alfabeto
        return index in self.letters

    def isOperatorArithmetic(self, index):
        # Verifica se o índice está presente na lista de operadores aritméticos
        return index in self.operatorsArithmetic

    def isOperatorRelational(self, index):
        # Verifica se o índice está presente na lista de operadores relacionais
        return index in self.operatorsRelational

    def isOperatorLogical(self, index):
        # Verifica se o índice está presente na lista de operadores lógicos
        return index in self.operatorsLogical

    def isOperator(self, index):
        # Verifica se o índice está presente em qualquer uma das listas de operadores
        return any(index in op_list for op_list in [self.operatorsArithmetic, self.operatorsRelational, self.operatorsLogical])

    def isDigit(self, index):
        # Verifica se o índice é um dígito
        return index in self.digits

    def isDelimiter(self, index):
        # Verifica se o índice está presente na lista de delimitadores da linguagem
        return index in self.delimiters

    def openFiles(self, file_input):
        try:
            read_file_path = os.path.join(os.getcwd(), self.dir_input, file_input)
            read_file = open(read_file_path, 'r')
            file_name = os.path.splitext(file_input)[0]  
            write_file_path = os.path.join(os.getcwd(), self.dir_output, file_name + '-saida.txt')  # Adiciona -saida.txt ao nome do arquivo de entrada
            write_file = open(write_file_path, 'w')
            return [read_file, write_file]
        except FileNotFoundError:
            write_file = open(os.getcwd() + self.dir_input + str(file_input).replace('entrada_lexica', 'saida_lexica'), 'w')
            write_file.write("(ERRO) Arquivo de entrada não lido '{}'.".format(self.dir_input + file_input))
            sys.exit()

    def openPrograms(self):
        input_dir = os.path.join(os.getcwd(), self.dir_input)
        if not os.path.isdir(input_dir):
            print("(ERRO) Diretório de entrada não encontrado '{}'.".format(self.dir_input))
            sys.exit()

        output_dir = os.path.join(os.getcwd(), self.dir_output)
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        files_programs = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        if not files_programs:
            print('(WARNING) Não tem arquivos para a leitura')
            sys.exit()
        return files_programs


  
    def start(self):
        files_programs = self.openPrograms()

      
        for file_program in files_programs:
            read_file = self.openFiles(file_program)[0]
            write_file = self.openFiles(file_program)[1]

            line_file = read_file.readline()
            line_index = 1


            erros = []
           
            while(line_file):
                index = 0
                length_line = len(line_file)

           
                while(index < length_line):
                    current_index = line_file[index]
                    next_index = None

 
                    if((index + 1) < length_line):
                        next_index = line_file[index+1]

   
                    if(self.isDelimiter(current_index)):
                        write_file.write('{}|DEL {} \n'.format(str(line_index).zfill(2), current_index))

          
                    elif(current_index == '/' and next_index == '/'):
                        index = length_line

        
                    elif(current_index == '/' and next_index == '*'):
                        check = True 

                        first_line = line_index


                        while(check and not(current_index == '*' and next_index == '/')):
                            if((index +2 ) < length_line):
                                index += 1
                                current_index = line_file[index]
                                next_index = line_file[index+1]
                            else:
                                line_file = read_file.readline()
                                length_line = len(line_file)
                                line_index += 1
                                index = - 1
                                if(not line_file):
                                    error = ('{} [ERRO] Coluna: {} | CoMF - Comentario mal formado\n'.format(first_line, str(index + 1).zfill(2)))
                                    erros.append(error)
                                    check = False

            
                    elif(current_index == string.punctuation[1]):
                        index += 1
                        check = False
                        index_last_quotes = 0
                        navigator = index

                     
                        while(navigator < length_line):
                            index_last_quotes += 1
                            if(line_file[navigator] == string.punctuation[1]):
                                check = True
                                break
                            navigator += 1

                       
                        if(not check):
                            error = '{} [ERRO] Coluna: {} | CMF - Cadeia mal formada\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)
                            index -= 1
                        
                        else:
                            index_last_quotes += index
                            inside_quotes = ''''''
                            navigator = index
                            index = index_last_quotes
                            while(navigator < index_last_quotes - 1):
                                inside_quotes += (line_file[navigator])
                                navigator += 1
                            for iterator in inside_quotes:
                                if(not self.isSymbol(iterator)):
                                    error = '{} [ERRO] Coluna: {} | CMF - Cadeia mal formada\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                                    erros.append(error)
                                    check = False
                                    break
                            if(check):
                                write_file.write('{}|CAD {} \n'.format(str(line_index).zfill(2), inside_quotes))
                                index -= 1

                   
                    elif(current_index == string.punctuation[6]):
                        navigator = index + 1
                        check = False

                      
                        while(navigator < length_line):
                            if(line_file[navigator] == string.punctuation[6]):
                                check = True
                                break
                            navigator += 1

                       
                        if((not check) or line_file[index + 1] == '\n'):
                            error = '{} [ERRO] Coluna: {} | CMF - Cadeia mal formada\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)
                            index = length_line
                       
                        elif(line_file[index + 1] == string.punctuation[6]):
                            write_file.write('{}|CRV {} \n'.format(str(line_index).zfill(2), "''"))
                            index += 1
                        
                        elif((line_file[index + 1] == string.punctuation[6]) and (line_file[index + 2] == string.punctuation[6])):
                            error = '{} [ERRO] Coluna: {} | TMF - Token mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)
                            index += 2
                        
                        elif(self.isSymbol(line_file[index + 1]) and line_file[index + 2] == string.punctuation[6]):
                            write_file.write('{}|SIM {} \n'.format(str(line_index).zfill(2), next_index))
                            index += 2
                        
                        else:
                            error = '{} [ERRO] Coluna: {} | TCI - Tamanho do caractere invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)
                            navigator = index + 1
                           
                            while(navigator < length_line):
                                if(string.punctuation[6] == line_file[navigator]):
                                    index = navigator + 1
                                    break
                                navigator += 1

                    
                    elif(self.isLetter(current_index)):
                        check = False
                        current_character = current_index
                        index += 1
                        goBreak = False

                        
                        while(index < length_line):
                            next_index = None
                            current_index = line_file[index]

                         
                            if(index + 1 < length_line):
                                next_index = line_file[index]

                            
                            if(self.isLetter(current_index) or self.isDigit(current_index) or current_index == "_"):
                                current_character += current_index
                            elif(current_index == '.'):
                                if(current_character == 'global' or current_character == 'local'):
                                    write_file.write('{}|PRE {} \n'.format(str(line_index).zfill(2), current_character))
                                else:
                                    write_file.write('{}|IDE {} \n'.format(str(line_index).zfill(2), current_character))

                                write_file.write('{}|DEL {} \n'.format(str(line_index).zfill(2), current_index))
                              
                                goBreak = True
                                break

                            
                            elif(self.isDelimiter(current_index) or current_index == ' ' or current_index == '\t' or current_index == '\r'):
                                index -= 1
                                break
                            
                            elif(next_index != None and self.isOperator(current_index + next_index)) or self.isOperator(current_index):
                                index -=1
                                break
                              
                            elif current_index != '\n':
                                error = '{} [ERRO] Coluna: {} | IMF - Identificador mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                                erros.append(error)
                                check = True
                                break

                            index += 1

                       
                        if(check):
                            while((index + 1) < length_line):
                                index += 1
                                current_index = line_file[index]
                                
                                if(self.isDelimiter(current_index) or current_index == ' ' or current_index == '\t' or current_index == '\r' or current_index == '/'):
                                    index -= 1
                                    break
                        elif(not goBreak):
                            if(self.isReserved(current_character)):
                                write_file.write('{}|PRE {} \n'.format(str(line_index).zfill(2), current_character))
                            else:
                                write_file.write('{}|IDE {} \n'.format(str(line_index).zfill(2), current_character))

                    elif(self.isDigit(current_index)):
                        current_character = current_index
                        maybe_signal = ''

                        if(line_file[index - 1] in ['-', '+']):
                            maybe_signal = line_file[index - 1]

                        index += 1
                        check_index = 0 
                        current_index = next_index
                        valid = False 

                        
                        while (self.isDigit(current_index) and (index + 1 < length_line)):
                            current_character += current_index
                            index += 1
                            current_index = line_file[index]

                       
                        if(current_index == '.'):
                            if((index + 1) < length_line):
                                current_character += current_index
                                index += 1
                                current_index = line_file[index]
                                
                                while(self.isDigit(current_index) and index < length_line - 1):
                                    check_index += 1
                                    current_character += current_index
                                    index += 1
                                    current_index = line_file[index]

                             
                                if(current_index == '.'):
                                    check_index = 0
                                   
                                    while(index < length_line - 1):
                                        index += 1
                                        current_index = line_file[index]
                                        if(self.isDelimiter(current_index) or current_index == string.punctuation[13]):
                                            index -= 1 
                                            break
                            
                            else:
                                valid = False 
                            if(check_index > 0):
                                valid = True
                            else:
                                valid = False
                            index -= 1
                       
                        else:
                            valid = True
                            if(not self.isDigit(current_index)):
                                index -= 1

                        
                        if(valid):
                            write_file.write('{}|NRO {} \n'.format(str(line_index).zfill(2), maybe_signal + current_character))
                        else:
                            error = '{} [ERRO] Coluna: {} | NMF - Numero mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)


                    elif(next_index != None and self.isOperatorArithmetic(current_index + next_index)):
                        write_file.write('{}|ART {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    elif(self.isOperatorArithmetic(current_index)):
                        if((not self.isDigit(next_index)) and current_index in ['-', '+']):
                            write_file.write('{}|ART {} \n'.format(str(line_index).zfill(2), current_index))
                    elif(next_index != None and self.isOperatorRelational(current_index + next_index)):
                        write_file.write('{}|REL {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    elif(self.isOperatorRelational(current_index)):
                        write_file.write('{}|REL {} \n'.format(str(line_index).zfill(2), current_index))
                    elif(next_index != None and self.isOperatorLogical(current_index + next_index)):
                        write_file.write('{}|LOG {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    elif(self.isOperatorLogical(current_index)):
                        write_file.write('{}|LOG {} \n'.format(str(line_index).zfill(2), current_index))
                    elif current_index != '\n' and current_index != ' ' and current_index != '\t' and current_index != '\r':
                        error = '{} [ERRO] Coluna: {} | TMF - Token mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                        erros.append(error)

                    index += 1

                line_file = read_file.readline()
                line_index += 1

            if not erros:
                write_file.write("sucesso\n")
            else:
                for erro in erros:
                    write_file.write(erro)

            read_file.close()
            write_file.close()
        return
