def collectInput():
    try:
        while True:
            data = input()
            if not data:
                break
            yield data
    except KeyboardInterrupt:
        return


def parseInput(questions: list):
    for question in questions:
        pass


if __name__ == '__main__':
    x = list(collectInput())
    print(x)
    print('end')

