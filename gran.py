"""Entrada local para a esteira de degravação do Gran."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="comando", required=True)
    commands.add_parser("verificar")
    for name in ("transcrever", "montar"):
        command = commands.add_parser(name)
        command.add_argument("entrada", type=Path)
        command.add_argument("saida", type=Path)
    args = parser.parse_args()

    if args.comando == "montar":
        return subprocess.call([sys.executable, ROOT / "montar_word.py", args.entrada, args.saida])

    config_path = ROOT / ".gran-ambiente.json"
    if not config_path.is_file():
        parser.error("Copie .gran-ambiente.exemplo.json para .gran-ambiente.json e preencha os caminhos locais.")
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    runtime = Path(config["transcritor"])
    model = Path(config["modelo"])
    required = [runtime / "faster_whisper" / "__init__.py"]
    required.extend(model / name for name in ("config.json", "model.bin", "tokenizer.json", "vocabulary.txt"))
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        parser.error(f"Componentes locais ausentes: {', '.join(missing)}")

    if args.comando == "transcrever":
        return subprocess.call(
            [
                sys.executable, ROOT / "transcrever_audio.py", args.entrada, args.saida,
                "--runtime", runtime, "--modelo", model,
            ]
        )
    return subprocess.call(
        [sys.executable, "-c", "import docx, pypdf, pptx; print('Ambiente Gran disponivel.')"]
    )


if __name__ == "__main__":
    sys.exit(main())

