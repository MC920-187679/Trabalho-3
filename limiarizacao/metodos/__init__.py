from argparse import ArgumentTypeError
from scipy.ndimage import generic_filter
from locais import limiariza_fn
import numpy as np

from typing import Dict, Optional
from scipy import LowLevelCallable
from tipos import Image, Metodo, AddSubParser, Namespace



class MetodoGlobal(Metodo):
    def limiariza(self, img: Image, tam: int, params: Namespace) -> Image:
        limite = params.L
        if limite is None:
            limite = np.mean(img)

        min, max = np.uint8(0), np.uint8(255)
        return np.where(img > limite, max, min)

    def add_arg_parser(self, parser: AddSubParser) -> None:
        subparser = parser('global', 'Método Global')
        subparser.add_argument('-T', type=float,
            help='Limiar fixo. Usa a intensidade média da imagem, se não for definido.')
        subparser.set_defaults(metodo=self)


def tamanho(entrada: str) -> int:
    try:
        tam = int(entrada, base=10)
        if tam < 0 or tam % 2 != 1:
            raise ValueError()
    except ValueError:
        raise ArgumentTypeError(f'tamanho inválido: {entrada}')


class MetodoLocal(Metodo):
    def __init__(self, name: str, description: str, **params: float):
        self.name = name
        self.description = description
        self.params = params

    def fn(self, tam: int, params: Namespace) -> LowLevelCallable:
        args = []
        for key, default in self.params:
            value = getattr(params, key, None)
            if value is None:
                args.append(default)
            else:
                args.append(value)

        return limiariza_fn(self.name, tam//2, *args)

    def limiariza(self, img: Image, tam: int, params: Namespace) -> Image:
        fn = self.fn(tam, params)
        size = 2 * tam + 1
        return generic_filter(img, fn, size=size, mode='mirror')

    def add_arg_parser(self, parser: AddSubParser) -> None:
        subparser = parser(self.name, self.description)
        subparser.add_argument('-t', '--tamanho', type=tamanho, default=5,
            help='Tamanho da vizinhança de limiarização.')

        if self.params:
            params = subparser.add_argument_group('Parâmetros')
        for key in self.params.keys():
            params.add_argument(f'-{key}', type=float, required=True)
        subparser.set_defaults(metodo=self)


METODO: Dict[str, Metodo] = {
    'global': MetodoGlobal(),
    'bernsen': MetodoLocal('bernsen', 'Método de Bernsen')
}