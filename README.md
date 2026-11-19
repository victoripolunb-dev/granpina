# Esteira de degravação Gran

Fluxo para transformar aulas em material de estudo editável em Word. A esteira inventaria as fontes, confere a gravação integral e os slides, adapta a fala para leitura e revisa o DOCX antes da entrega.

## Navegação

| Assunto | Documento |
| --- | --- |
| Fluxo completo e pontos de aceite | [Esteira](ESTEIRA.md) |
| Escopo editorial e instruções de redação | [Especificação](ESPECIFICACAO.md) e [prompt](PROMPT.md) |
| Padrão Gran e formatação do DOCX | [Regras](REGRAS-GRAN.md) e [modelo](MODELO-WORD.md) |
| Coordenação, revisores e retestes | [Instruções](AGENTS.md) e [qualidade](QUALIDADE.md) |
| Modelos de acompanhamento | [Registro de aula](REGISTRO-AULA.md) e [relatório de implantação](RELATORIO.md) |
| Ajustes aplicáveis às próximas aulas | [Decisões](DECISOES.md) |
| Piloto Planejamento Conservacionista II | [Produção e revisão](piloto/Registro.md) e [incidente de áudio no Codex](piloto/Incidente-de-audio.md) |

## Testar a montagem do Word

Com Python 3.12, execute na raiz do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m unittest discover -s testes -v
New-Item -ItemType Directory -Force saida
.\.venv\Scripts\python gran.py montar testes/amostra.json saida/amostra.docx
```

O JSON sintético exercita título, citações, marcadores, destaques e relógios. O gerador produz a base do Word. Equações, mapas e outros elementos específicos são montados e revisados conforme a aula. Use um nome de saída novo a cada execução.

## Transcrever áudio localmente

1. Obtenha o modelo multilíngue [Systran/faster-whisper-small](https://huggingface.co/Systran/faster-whisper-small) em uma pasta local.
2. Copie `.gran-ambiente.exemplo.json` para `.gran-ambiente.json`. Aponte `transcritor` para o diretório que contém a pasta do pacote `faster_whisper` (em um ambiente virtual do Windows, normalmente `.venv/Lib/site-packages`, com caminho absoluto). Aponte `modelo` para os arquivos locais do modelo.
3. Rode `python gran.py verificar` e `python gran.py transcrever caminho/para/aula.mp3 saida/transcricao.json` com o Python do ambiente virtual. Confira as lacunas e divergências com a legenda e os slides.

## Retomar em outra IDE

Clone este repositório e abra a pasta inteira na IDE. Comece por [AGENTS.md](AGENTS.md) e pelo [guia de retomada](CONTEXTO.md). O [inventário](INVENTARIO.md) identifica os arquivos preservados, com tamanho e SHA-256.

- [Acervo](acervo/) reúne os manuais, os exemplos de Word e as fontes originais recuperadas.
- [Piloto](piloto/) reúne a entrega, as transcrições, a redação, a montagem e as evidências das três revisões.
- [Testes](testes/) reúne a amostra editável em JSON, os testes automatizados e as evidências dos testes sintéticos anteriores.

