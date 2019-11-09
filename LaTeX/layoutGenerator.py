from os import system, name
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
    system('cls' if name == 'nt' else 'clear')


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

        letters = [let.strip() for let in question[1].split(',')]       # Separates out each individual problem letter
        for letter in letters:
            if len(letter) == 1:
                print('\\subsection*{' + letter + '.}')
            else:                                                       # Runs if there's a set of problem letters, ex: a-d
                letterSection = ascii_lowercase[ascii_lowercase.find(letter[0]):ascii_lowercase.find(letter[-1]) + 1]
                for let in letterSection:
                    print('\\subsection*{' + let + '.}')
        print('\\pagebreak\n')
        num += 1

    # Closing
    print('\\end{document}')


if __name__ == '__main__':
    q = list(collectInput())
    clearScreen()
    printLayout(parseInput(q))
