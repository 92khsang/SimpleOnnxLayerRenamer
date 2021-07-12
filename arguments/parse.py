import getopt

class Parser():
    def __init__(self, argv : list):
        if not isinstance(argv, list):
            raise TypeError("Invalid Input arguments")
        self.__argv = argv

    def parse(self) -> dict:
        if self.__argv is None:
            return {}

        parsed_arguments_dict = {}

        try:
            opts, args = getopt.getopt(self.__argv, "hf:t:d:",["help=","file=","target=","dest="])
        except getopt.GetoptError:
            return parsed_arguments_dict

        if len(opts) == 0:
            return parsed_arguments_dict

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                return {}
            elif opt in ("-f", "--file"):
                parsed_arguments_dict['file'] = arg
            elif opt in ("-t", "--target"):
                parsed_arguments_dict['target'] = arg
            elif opt in ("-d", "--dest"):
                parsed_arguments_dict['dest'] = arg

        return parsed_arguments_dict