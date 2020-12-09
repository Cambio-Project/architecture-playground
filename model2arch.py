import pickle
import argparse

from models.architecture import Architecture
from models.jaeger_trace import JaegerTrace
from models.misim_model import MiSimModel
from models.zipkin_trace import ZipkinTrace
from util.parse import bool_from_string

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts a model into an architecture representation.')

    # Models
    parser.add_argument('-m', '--model', dest='model', nargs=1, required=False,
                        help='Stores a previously converted model.')
    parser.add_argument('--misim', dest='misim', type=str, nargs='+', required=False,
                        help='Converts a MiSim model. Takes the architecture model and an optional experiment model.')
    parser.add_argument('--jaeger', dest='jaeger', type=str, nargs=1, required=False,
                        help='Converts a Jager trace.')
    parser.add_argument('--zipkin', dest='zipkin', type=str, nargs=1, required=False,
                        help='Converts a Zipkin trace.')

    # Validation
    parser.add_argument('-vm', '--validate-model', dest='validate_model', action='store_true',
                        help='Validates the model.')
    parser.add_argument('-va', '--validate-architecture', dest='validate_architecture', action='store_true',
                        help='Validates the architecture.')

    # Export
    parser.add_argument('-em', '--export-model', dest='export', action='store_true',
                        help='Exports the converted model in an intermediate format (pickle).')
    parser.add_argument('-d3', '--d3-graph', dest='d3', type=str, nargs='+', required=False,
                        help='Stores a d3 graph to the specified location.')

    args = parser.parse_args()
    model = None
    arch = None
    model_name = ''

    if args.model:
        model_name = args.model[0]
        model = pickle.load(open(model_name, 'rb'))
    elif args.misim:
        model_name = args.misim[0]
        model = MiSimModel(model_name)
    elif args.jaeger:
        model_name = args.jaeger[0]
        model = JaegerTrace(model_name)
    elif args.zipkin:
        model_name = args.zipkin[0]
        model = ZipkinTrace(model_name)

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

    if args.export:
        if model_name:
            pickle.dump(model, open(model_name + '.dat', 'wb+'))

    if args.d3:

        stop = False

        if not model:
            print('No model!')
            stop = True
        if not arch:
            print('No architecture!')
            stop = True

        if stop:
            exit(1)

        handle = open(args.d3[0], 'w+')

        # Pretty
        pretty_print = False
        if len(args.d3) > 1:
            pretty_print = bool_from_string(args.d3[1])

        # JavaScript
        if args.d3[0].endswith('.js'):
            content = 'let graph=' + arch.d3_graph(pretty_print) + ';'
        # Json
        else:
            content = arch.d3_graph(pretty_print)

        handle.write(content)
        handle.close()
