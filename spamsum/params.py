from argparse import ArgumentParser


def args():
    parser = ArgumentParser(description='Piecewise content-triggered hash')

    parser.add_argument('-W', '--ignore-whitespace', action='store_true')
    parser.add_argument('-H', '--ignore-headers', action='store_true',
        help='e-mail headers')

    return parser.parse_args()


if __name__ == '__main__':
    print args()
