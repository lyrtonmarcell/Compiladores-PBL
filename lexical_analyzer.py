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
            file_name = os.path.splitext(file_input)[0]  # Remove a extensão do arquivo de entrada
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


    # Método que inicia o analisador léxico.
    def start(self):
        files_programs = self.openPrograms()

        # Laço de repetição que percorre todos os arquivos encontrados na
        # pasta de entrada (entradaX.txt).
        for file_program in files_programs:
            read_file = self.openFiles(file_program)[0]
            write_file = self.openFiles(file_program)[1]

            line_file = read_file.readline()
            line_index = 1


            erros = []
            # Laço de repetição que percorre todas as linhas do arquivo de entrada.
            while(line_file):
                index = 0
                length_line = len(line_file)

                # Laço de repetição que percorre todos os índices da linha.
                while(index < length_line):
                    current_index = line_file[index]
                    next_index = None

                    # Caso ainda haja um próximo indíce a ser lido, ele é lido e
                    # atribuído a variável next_index.
                    if((index + 1) < length_line):
                        next_index = line_file[index+1]

                    # Verifica se o caracter é um delimitador e escreve no arquivo de saída respectivo
                    if(self.isDelimiter(current_index)):
                        write_file.write('{}|DEL {} \n'.format(str(line_index).zfill(2), current_index))

                    # Verifica se é um comentário simples
                    elif(current_index == '/' and next_index == '/'):
                        index = length_line

                    # Verifica se é um comentário em bloco
                    elif(current_index == '/' and next_index == '*'):
                        check = True # Variavel responsável por controlar se o comentário de bloco
                                     # foi fechado adequadamente.

                        first_line = line_index

                        # Percorre o restante da linha e das próximas linhas atrás do */ que fecha
                        # o comentário de bloco, caso não encontre é lançado um erro.
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

                    # Verifica se o caracter é uma aspas duplas
                    elif(current_index == string.punctuation[1]):
                        index += 1
                        check = False  # Variavel de controle
                        index_last_quotes = 0
                        navigator = index

                        # Percorre o restante da linha atrás da próxima aspas duplas
                        while(navigator < length_line):
                            index_last_quotes += 1
                            if(line_file[navigator] == string.punctuation[1]):
                                check = True
                                break
                            navigator += 1

                        # Verifica se é a cadeia de caractere é fechado corretamente com aspa dupla
                        if(not check):
                            error = '{} [ERRO] Coluna: {} | CMF - Cadeia mal formada\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)
                            index -= 1
                        # Caso esteja tudo ok, é verificado dentro da aspas duplas
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

                    # Verifica se o índíce é uma aspa simples
                    elif(current_index == string.punctuation[6]):
                        navigator = index + 1
                        check = False

                        # Percorre o restante da linha atrás da próxima aspas simples
                        while(navigator < length_line):
                            if(line_file[navigator] == string.punctuation[6]):
                                check = True
                                break
                            navigator += 1

                        # Caso as aspas simples não tenham sido fechada corretamente
                        # ou caso o indíce contido dentro das aspas simples seja um \n
                        if((not check) or line_file[index + 1] == '\n'):
                            error = '{} [ERRO] Coluna: {} | CrMF - Caractere mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)
                            index = length_line
                        # Escrevendo Caracter Reservado valido no arquivo
                        # Nesse caso foi apenas a abertura e fechamento das aspas simples
                        elif(line_file[index + 1] == string.punctuation[6]):
                            write_file.write('{}|CRV {} \n'.format(str(line_index).zfill(2), "''"))
                            index += 1
                        # Caso o indíce contido dentro das aspas simples seja outra '
                        elif((line_file[index + 1] == string.punctuation[6]) and (line_file[index + 2] == string.punctuation[6])):
                            error = '{} [ERRO] Coluna: {} | TMF - Token mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)
                            index += 2
                        # Caso o simbolo contido dentro das aspas simples seja válido
                        elif(self.isSymbol(line_file[index + 1]) and line_file[index + 2] == string.punctuation[6]):
                            write_file.write('{}|SIM {} \n'.format(str(line_index).zfill(2), next_index))
                            index += 2
                        # Caso o tamanho exceda o de 1 da aspas simples
                        else:
                            error = '{} [ERRO] Coluna: {} | TCI - Tamanho do caractere invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)
                            navigator = index + 1
                            # Percorre até o final da cadeia para pular e ir para os próximos índices
                            while(navigator < length_line):
                                if(string.punctuation[6] == line_file[navigator]):
                                    index = navigator + 1
                                    break
                                navigator += 1

                    # Verifica se o caracter é uma letra
                    elif(self.isLetter(current_index)):
                        check = False
                        current_character = current_index
                        index += 1
                        goBreak = False

                        # Percorre a linha do arquivo para pegar toda a palavra
                        while(index < length_line):
                            next_index = None
                            current_index = line_file[index]

                            # Caso haja um próximo índice depois do atual
                            if(index + 1 < length_line):
                                next_index = line_file[index]

                            # Verifica se o caracter atual é uma letra e se o caracter seguinte é um digito ou um traço 
                            if(self.isLetter(current_index) or self.isDigit(current_index) or current_index == "_"):
                                current_character += current_index
                            elif(current_index == '.'):
                                if(current_character == 'global' or current_character == 'local'):
                                    write_file.write('{}|PRE {} \n'.format(str(line_index).zfill(2), current_character))
                                else:
                                    write_file.write('{}|IDE {} \n'.format(str(line_index).zfill(2), current_character))

                                write_file.write('{}|DEL {} \n'.format(str(line_index).zfill(2), current_index))
                                #index += 1
                                goBreak = True
                                break

                            # Verifica se o caracter atual é um delimitador
                            elif(self.isDelimiter(current_index) or current_index == ' ' or current_index == '\t' or current_index == '\r'):
                                index -= 1
                                break
                            # Verifica Se o caracter atual e seguinte é um operador
                            # Caso o próximo lexema não seja vazio
                            elif(next_index != None and self.isOperator(current_index + next_index)) or self.isOperator(current_index):
                                index -=1
                                break
                              # Caso não seja nenhum dos casos acima e for diferente de um saldo de linha, é lançado um erro
                            elif current_index != '\n':
                                error = '{} [ERRO] Coluna: {} | IMF - Identificador mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                                erros.append(error)
                                check = True
                                break

                            index += 1

                        # Caso tenha ocorrido o erro acima, o ponteiro irá pular a palavra e seguirá seu fluxo
                        if(check):
                            while((index + 1) < length_line):
                                index += 1
                                current_index = line_file[index]
                                # Verifica se é um delimitador espaço, \t, \r ou uma /
                                if(self.isDelimiter(current_index) or current_index == ' ' or current_index == '\t' or current_index == '\r' or current_index == '/'):
                                    index -= 1
                                    break
                        # Caso não tenha ocorido nenhum erro
                        elif(not goBreak):
                            # Escreve no arquivo caso a palavra seja reservada
                            if(self.isReserved(current_character)):
                                write_file.write('{}|PRE {} \n'.format(str(line_index).zfill(2), current_character))
                            # Escreve no arquivo caso seja identificador
                            else:
                                write_file.write('{}|IDE {} \n'.format(str(line_index).zfill(2), current_character))

                    # Verifica se é um digito
                    elif(self.isDigit(current_index)):
                        current_character = current_index
                        maybe_signal = ''

                        # Verifica se o dígito é precedido de sinal negativo ou positivo
                        if(line_file[index - 1] in ['-', '+']):
                            maybe_signal = line_file[index - 1]

                        index += 1
                        check_index = 0 # Variável responsável por guarda a quantidade de casas caso o numero seja decimal (float)
                        current_index = next_index
                        valid = False # Variável de controle para verificar se o digito é valido

                        # Laço que captura toda a sequencia de digitos
                        while (self.isDigit(current_index) and (index + 1 < length_line)):
                            current_character += current_index
                            index += 1
                            current_index = line_file[index]

                        # Verifica se após o digito capturado acima, o proximo indice é um ponto decimal
                        if(current_index == '.'):
                            if((index + 1) < length_line):
                                current_character += current_index
                                index += 1
                                current_index = line_file[index]
                                # Laço que captura toda a outra parte do numero após o ponto
                                while(self.isDigit(current_index) and index < length_line - 1):
                                    check_index += 1
                                    current_character += current_index
                                    index += 1
                                    current_index = line_file[index]

                                # Caso não tenha entrado no while acima, é porque não há número após o ponto
                                if(current_index == '.'):
                                    check_index = 0
                                    # Verifica se há um delimitar ou um espaço no restante da linha
                                    while(index < length_line - 1):
                                        index += 1
                                        current_index = line_file[index]
                                        if(self.isDelimiter(current_index) or current_index == string.punctuation[13]):
                                            index -= 1 # Caso haja, volta uma casa (índice) da linha
                                            break
                            # Caso haja um ponto após o número e depois desse ponto a linha acabe
                            else:
                                valid = False
                            # Caso tenha digito(s) após o ponto
                            if(check_index > 0):
                                valid = True
                            # Caso não tenha digito(s) após o ponto
                            else:
                                valid = False
                            index -= 1
                        # Caso o digito não seja decimal (float)
                        else:
                            valid = True
                            if(not self.isDigit(current_index)):
                                index -= 1

                        # Caso o digito esteja integro
                        if(valid):
                            write_file.write('{}|NRO {} \n'.format(str(line_index).zfill(2), maybe_signal + current_character))
                        # Caso tenha ocorrido alguma inconsistência na sua verificação
                        else:
                            error = '{} [ERRO] Coluna: {} | NMF - Numero mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            erros.append(error)


                    # Caso o próximo lexema não seja vazio e seja um operador aritimetico duplo (com dois simbolos operacionais)
                    elif(next_index != None and self.isOperatorArithmetic(current_index + next_index)):
                        write_file.write('{}|ART {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    # Caso seja um operador aritimetico simples (com apenas um simbolo operacional)
                    elif(self.isOperatorArithmetic(current_index)):
                        # Caso o próximo índice seja um número ele não grava, pois o sinal junto com o simbolo irá passar pelo analisador de digitos
                        if((not self.isDigit(next_index)) and current_index in ['-', '+']):
                            write_file.write('{}|ART {} \n'.format(str(line_index).zfill(2), current_index))
                    # Caso seja um operador relacional duplo
                    elif(next_index != None and self.isOperatorRelational(current_index + next_index)):
                        write_file.write('{}|REL {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    # Caso seja um operador relacional simples
                    elif(self.isOperatorRelational(current_index)):
                        write_file.write('{}|REL {} \n'.format(str(line_index).zfill(2), current_index))
                    # Caso seja um operador lógico duplo
                    elif(next_index != None and self.isOperatorLogical(current_index + next_index)):
                        write_file.write('{}|LOG {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    # Caso seja um operador lógico simples
                    elif(self.isOperatorLogical(current_index)):
                        write_file.write('{}|LOG {} \n'.format(str(line_index).zfill(2), current_index))
                    # Caso não caia em nenhum dos casos acima e não seja nenhum espaçador ou pulador de linha
                    elif current_index != '\n' and current_index != ' ' and current_index != '\t' and current_index != '\r':
                        error = '{} [ERRO] Coluna: {} | TMF - Token mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                        erros.append(error)

                    index += 1

                # Lê a próxima linha
                line_file = read_file.readline()
                line_index += 1

                # Escrevendo os erros no final do arquivo de saída
            if not erros:
                write_file.write("sucesso\n")
            else:
                for erro in erros:
                    write_file.write(erro)

            # Fechando os arquivos
            read_file.close()
            write_file.close()
        return
