from converter import MD2HTMLConverter


def main():
    filename = "./resources/document.md"
    with MD2HTMLConverter(filename) as converter:
        print(converter.parser.html)


if __name__ == '__main__':
    main()
