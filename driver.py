from DCF import DCF

def main():
    dcf = DCF()
    dcf.startFlow()
    print(dcf.getTokens())

if __name__ == "__main__":
    main()