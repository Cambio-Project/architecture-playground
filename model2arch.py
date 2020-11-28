import argparse

from models.architecture import Architecture
from models.jaeger_trace import JaegerTrace
from models.misim_model import MiSimModel

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts a model into an architecture representation.')

    # Models
    parser.add_argument('-m', '--model', dest='model', nargs=1, required=False,
                        help='Stores a previously converted model.')
    parser.add_argument('--misim', dest='misim', type=str, nargs='+', required=False,
                        help='Converts a MiSim model. Takes the architecture model and an optional experiment model.')
    parser.add_argument('--jaeger', dest='jaeger', type=str, nargs=1, required=False,
                        help='Converts a Jager trace.')

    # Validation
    parser.add_argument('-vm', '--validate-model', dest='validate_model', action='store_true',
                        help="Validates the model.")
    parser.add_argument('-va', '--validate-architecture', dest='validate_architecture', action='store_true',
                        help="Validates the architecture.")

    # Other
    parser.add_argument('--d3-graph', dest='d3', type=str, nargs=1, required=False,
                        help="Stores a d3 graph to the specified location.")

    args = parser.parse_args()
    model = None
    arch = None

    if args.model:
        model = model
    elif args.misim:
        model = MiSimModel(args.misim[0])
    elif args.jaeger:
        model = JaegerTrace(args.jaeger[0])

    if model:
        arch = Architecture(model)

        if args.validate_model:
            success, exceptions = model.validate(True)
            success &= model.valid
            print('Validation of {} model: {} {}'.format(
                model.type,
                'Successful' if success else 'Failed',
                '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))

    if arch:
        if args.validate_architecture:
            success, exceptions = arch.validate()
            print('Validation of architecture: {} {}'.format(
                'Successful' if success else 'Failed',
                '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))

    if args.d3:
        handle = open(args.d3[0], 'w+')
        if args.d3[0].endswith('.js'):
            handle.write('let graph=' + arch.d3_graph() + ';')
        else:
            handle.write(arch.d3_graph(True))
        handle.close()
