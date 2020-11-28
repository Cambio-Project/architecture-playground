import json

from models.model import IModel
from typing import Union, Any, Dict

from typing.io import IO

from models.operation import Operation
from models.service import Service


class JaegerTrace(IModel):
    def __init__(self, source: Union[str, IO] = None):
        super().__init__(self.__class__.__name__, source)

    def _parse(self, model: Dict[str, Any]) -> bool:
        process_ids = {}
        traces = model['data']

        for trace in traces:
            _id = trace['traceID']

            # Identify all services (processes)
            for process_id, process in trace['processes'].items():
                service_name = process['serviceName']
                self._services[service_name] = Service(service_name)
                process_ids[process_id] = service_name

            # Add operations to the corresponding services.
            for span in trace['spans']:
                operation_name = span['operationName']
                pid = span['processID']
                service = process_ids[pid]
                self._services[service].add_operation(Operation(operation_name))

        return True

    def read(self, source: Union[str, IO] = None) -> bool:
        if isinstance(source, str):
            return self._parse(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse(json.load(source))
        return False
