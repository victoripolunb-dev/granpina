"""Gere uma transcrição local com tempos a partir da gravação completa."""

import argparse
import json
import os
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", type=Path, help="Gravação da aula")
    parser.add_argument("saida", type=Path, help="Caminho de um novo JSON")
    parser.add_argument("--runtime", required=True, type=Path, help="Pasta local do faster-whisper")
    parser.add_argument("--modelo", required=True, type=Path, help="Pasta do modelo multilíngue local")
    args = parser.parse_args()

    if not args.audio.is_file():
        parser.error("O arquivo de áudio não está disponível.")
    if args.saida.suffix.lower() != ".json" or args.saida.exists():
        parser.error("A saída deve ser um caminho JSON novo.")
    model_files = ("config.json", "model.bin", "tokenizer.json", "vocabulary.txt")
    if not (args.runtime / "faster_whisper").is_dir() or not all(
        (args.modelo / name).is_file() for name in model_files
    ):
        parser.error("O transcritor e o modelo precisam estar disponíveis no computador.")

    os.environ["HF_HUB_OFFLINE"] = "1"
    sys.path.insert(0, str(args.runtime.resolve()))
    from faster_whisper import WhisperModel

    model = WhisperModel(str(args.modelo.resolve()), device="cpu", compute_type="int8", local_files_only=True)
    segments, info = model.transcribe(str(args.audio.resolve()), language="pt", vad_filter=False)
    result = {
        "arquivo": args.audio.name,
        "duracao_segundos": round(info.duration, 3),
        "idioma": info.language,
        "segmentos": [
            {
                "inicio_segundos": round(segment.start, 3),
                "fim_segundos": round(segment.end, 3),
                "texto": segment.text.strip(),
                "probabilidade_sem_fala": round(segment.no_speech_prob, 3),
            }
            for segment in segments
        ],
    }
    with args.saida.open("x", encoding="utf-8") as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
        output.write("\n")


if __name__ == "__main__":
    main()
