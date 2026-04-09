from argparse import ArgumentParser
import importlib

from Uxor.main import StandardUxor


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('other', nargs='+')
    parser.add_argument('--config')
    args = parser.parse_args()
    print(args)
    config_module = importlib.import_module(f".{args.config}", "Uxor.configs")
    init_kwargs = {k: v for k, v in vars(args).items()
                   if k not in {'config', 'text'}}
    text = " ".join(args.text)
    uxor: StandardUxor = config_module.from_cli(**init_kwargs)
    print(uxor(text))
