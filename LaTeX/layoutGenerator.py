from os import name
from subprocess import call
from string import ascii_lowercase


def collectInput():
    """Generator that collects multi-line user input"""
    print("Enter the list of questions and press \'Enter\' twice: ")
    try:
        while True:
            data = input()
            if not data:
                break
            yield data
    except KeyboardInterrupt:
        return


def parseInput(questions: list) -> list:
    """Separates question into problem number and problem letters"""
    parsedQuestions = []
    for question in questions:
        numIndex = question.find(')')
        problemNum = question[numIndex + 2:question.find(' ', numIndex + 2)]        # Isolates problem number
        problemLetters = question[question.find(' ', numIndex + 2) + 1:]            # Isolates problem letters
        parsedQuestions.append((problemNum, problemLetters))
    return parsedQuestions


def clearScreen():
    """Clears screen to allow for copy-pasting"""
    _ = call('clear' if name =='posix' else 'cls')


def printLayout(parsedQuestions: list):
    """Prints document layout with question formatting"""
    # Header
    header = ['\\documentclass[letterpaper]{article}', '\\usepackage[margin=1in]{geometry}', '\\usepackage{amssymb}',
              '\\usepackage{amsthm, amsmath, times, graphicx}', '\\graphicspath{{./images/}}', '\\hbadness=99999',
              '\\renewcommand{\\qedsymbol}{$\\blacksquare$}', '\\begin{document}\n', '\\title{Homework x}',
              '\\author{Minhduc Cao\\\\', '        ICS 6B - Lecture B\\\\', '        Professor Irene Gassko}',
              '\\date{\\today}', '\\maketitle\n']
    for item in header:
        print(item)

    # Questions
    num = 1
    for question in parsedQuestions:
        print('% QUESTION', num)
        print('\\section*{\\#' + str(num) + ':', question[0] + '}')

        letters = [let.strip() for let in question[1].split(',')]
        for letter in letters:
            if len(letter) == 1:
                print('\\subsection*{' + letter + '.}')
            else:
                letterSection = ascii_lowercase[ascii_lowercase.find(letter[0]):ascii_lowercase.find(letter[-1]) + 1]
                for let in letterSection:
                    print('\\subsection*{' + let + '.}')
        print('\\pagebreak\n')
        num += 1

    # Closing
    print('\\end{document}')


if __name__ == '__main__':
    y = ['1) 5.1.1 a', '2) 5.1.2 a-c', '3) 5.1.3 a, b-d', '4) 5.2.2 c', '5) 5.3.1 g']
    printLayout(parseInput(y))
    print('end')

