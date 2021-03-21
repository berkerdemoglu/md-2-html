from converter import MD2HTMLConverter


def main():
    filename = "../resources/document.md"
    converter = MD2HTMLConverter(filename)
    converter.convert()


if __name__ == '__main__':
    main()
