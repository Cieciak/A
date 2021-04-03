import A



while True:
    text = input('A Shell >>> ')
    lexer = A.Lexer(text)
    tokens, error = lexer.analyze_code()

    if error: print(error)
    else:
        parser = A.Parser(tokens)
        out, error = parser.run()

        if error: print(error)
        else:
#            for pos, token in zip(range(len(tokens)), tokens):
#                print(pos, ': ', token, end="; ", sep='')
#            print('\n')
            for i in out:
                print(i, '\n')