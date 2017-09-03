from argparse import ArgumentParser


def args():
    parser = ArgumentParser(description='Piecewise content-triggered hash')

    parser.add_argument('-W', '--ignore-whitespace', action='store_true')

    parser.add_argument('-H', '--ignore-headers', action='store_true',
        help='e-mail headers')

    parser.add_argument('-d', '--dbname', action='store',
        help='db of hashes for match')

    parser.add_argument('-B', '--block-size', action='store', type=int)

    parser.add_argument('-T', '--threshold', action='store', type=int,
        help='stop search db when score above threshold is found')

    parser.add_argument('-c', action='store', dest='spamsum_hash',
        help='spamsum hash for db search (like: 24:AVP/6Lo8e5y:X09y)')

    parser.add_argument('-C', action='store', dest='path_for_hash',
        help='path to file for hashing and db search')

    return parser.parse_args()


if __name__ == '__main__':
    print args()