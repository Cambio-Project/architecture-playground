import argparse

from models.architecture import Architecture
from models.misim_model import MiSimModel

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts a model into an architecture representation.')
    parser.add_argument('-m', '--model', dest='model', nargs=1, required=False,
                        help='Stores a previously converted model.')
    parser.add_argument('-vm', '--validate-model', dest='validate_model', action='store_true',
                        help="Validates the model.")
    parser.add_argument('-va', '--validate-architecture', dest='validate_architecture', action='store_true',
                        help="Validates the architecture.")

    parser.add_argument('--misim', dest='misim', type=str, nargs='+', required=False,
                        help='Converts a MiSim model. Takes the architecture model and an optional experiment model.')

    args = parser.parse_args()
    model = None
    arch = None

    if args.model:
        model = model
    elif args.misim:
        model = MiSimModel(args.misim[0])

    if model:
        arch = Architecture(model)

        if args.validate_model:
            print(model.validate(True))

    if arch:
        if args.validate_architecture:
            print(arch.validate())
