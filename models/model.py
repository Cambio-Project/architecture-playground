from typing import Union, Dict, Tuple, List
from typing.io import IO

from models.operation import Operation
from models.service import Service


class NoDependenciesException(BaseException):
    def __init__(self):
        super().__init__('No dependencies found')


class WrongFormatException(BaseException):
    def __init__(self):
        super().__init__('Wrong format')


class UnknownOperation(BaseException):
    def __init__(self, service: str, operation: str):
        super().__init__('Unknown Operation: {}/{}'.format(service, operation))


class OperationSelfDependency(BaseException):
    def __init__(self, operation: Operation):
        if operation.service:
            operation = '{}/{}'.format(operation.service.name, operation.name)
        super().__init__('Self Dependency: {}'.format(operation))


class CyclicOperationDependency(BaseException):
    def __init__(self, operation1: Operation, operation2: Operation):
        if operation1.service:
            operation1 = '{}/{}'.format(operation1.service.name, operation1.name)
        if operation2.service:
            operation2 = '{}/{}'.format(operation2.service.name, operation2.name)
        super().__init__('Circular Dependency: {} <-> {}'.format(operation1, operation2))


class IModel:
    """
    Interface for all models.
    All derived classes must implement the read method.
    The read method is responsible to check the syntax of the model.

    IModel provides a validation method that checks for validity of the model.
    This validation checks the semantic of the model.
    """
    def __init__(self, model_type: str):
        self._model_type = model_type
        self._services = {}

    def __iter__(self):
        return iter(self._services)

    @property
    def model(self) -> str:
        return self._model_type

    @property
    def services(self) -> Dict[str, Service]:
        return self._services

    def validate(self, check_everything=False) -> Tuple[bool, List[BaseException]]:
        valid = True
        stack = []

        try:
            for _, service in self._services.items():
                for _, operation in service.operations.items():

                    # Check self dependency
                    if operation in operation.dependencies:
                        stack.append(OperationSelfDependency(operation))

                    for dependency in operation.dependencies:
                        # Check circular dependencies
                        if operation in dependency.dependencies:
                            stack.append(CyclicOperationDependency(operation, dependency))
                            continue

                        try:
                            _ = self._services[dependency.service.name].operations[dependency.name]

                        # Service or operation is not known.
                        except AttributeError:
                            if not check_everything:
                                return False, [UnknownOperation(service.name, operation.name)]
                            else:
                                valid = False
                                stack.append(UnknownOperation(service.name, operation.name))

        # Unknown exception has occurred.
        except BaseException as e:
            stack.append(e)
            return False,  stack
        return valid, stack

    def print(self):
        for _, service in self._services.items():
            service.print()

    def read(self, source: Union[str, IO]) -> bool:
        raise NotImplementedError('read() method must be implemented!')
