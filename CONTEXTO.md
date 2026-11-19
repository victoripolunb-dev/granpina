# Contexto para retomar a esteira de degravação Gran

## Objetivo e estado atual

Produzir material de estudo em Word a partir das aulas do Gran, mantendo a ordem da fala, as explicações, os exemplos, as ressalvas e os termos que afetam o sentido. A redação remove oralidade e repetições dispensáveis. O Word aplica as regras específicas de exercícios, lei, observações, relógios e elementos visuais conforme o conteúdo de cada aula.

O projeto começou com o mapeamento dos manuais e dos modelos Word. A primeira implementação foi verificada com exemplos sintéticos, inclusive uma simulação de fontes de aulas diferentes. O primeiro piloto com mídia real foi Planejamento Conservacionista II. A versão 3 foi aprovada por conteúdo, formatação e coordenação. O registro identifica o arquivo final pelo hash.

## Onde começar

| Se a tarefa for | Leia ou use |
| --- | --- |
| Produzir uma aula nova | [AGENTS.md](AGENTS.md), [ESTEIRA.md](ESTEIRA.md), [ESPECIFICACAO.md](ESPECIFICACAO.md) e [PROMPT.md](PROMPT.md) |
| Conferir uma regra do Gran | [REGRAS-GRAN.md](REGRAS-GRAN.md) e os [manuais originais](acervo/referencias/) |
| Resolver uma dúvida de aparência | [MODELO-WORD.md](MODELO-WORD.md) e os [exemplos de Word](acervo/exemplos/) |
| Auditar a versão de entrega | [QUALIDADE.md](QUALIDADE.md), [REGISTRO-AULA.md](REGISTRO-AULA.md) e [DECISOES.md](DECISOES.md) |
| Trabalhar no código | [gran.py](gran.py), [montar_word.py](montar_word.py), [transcrever_audio.py](transcrever_audio.py) e [testes](testes/) |
| Repetir ou revisar o piloto | [piloto/Registro.md](piloto/Registro.md), [fontes do piloto](acervo/fontes-piloto/) e [artefatos de produção](piloto/) |

## Fluxo de trabalho para uma nova aula

1. Inventarie o áudio, a legenda, os slides, o título e os códigos do Saturno. Confirme a identidade temática por passagens específicas do início, do meio e do fim.
2. Execute a transcrição local da gravação inteira. Compare as duas transcrições por intervalos, confira lacunas e compare os slides com o que o professor ensina. Compare também as imagens, tabelas e fórmulas que precisam entrar no Word.
3. Só então redija na sequência da exposição. Vincule os blocos ao tempo da gravação. Marque cada múltiplo de cinco minutos no fim do parágrafo correspondente.
4. Execute a montagem do Word-base e acrescente elementos específicos. Confira alterações de sentido, títulos, listas, recuos, equações, imagens e gabaritos.
5. Faça as três revisões independentes de fontes, fidelidade e layout com as responsabilidades descritas em QUALIDADE.md. Depois de cada correção, repita as verificações afetadas e registre a versão exata aprovada.
6. Registre a entrega e acrescente decisões reutilizáveis. Quando restar dúvida que comprometa cobertura ou sentido, mantenha o caso em revisão e indique a evidência que falta.

## Como reproduzir as verificações

- Os comandos para instalar dependências, rodar o teste automatizado e gerar um DOCX sintético estão em [README.md](README.md). Os três testes cobrem os estilos base, a rejeição de relógio com minuto pulado e a proteção de um arquivo de saída existente.
- [testes/evidencias](testes/evidencias/) preserva os arquivos de áudio e as transcrições dos testes sintéticos. O [relatório](RELATORIO.md) explica o que cada teste comprova e seus limites.
- No piloto, [audio.json](piloto/audio.json) é a saída integral escolhida. [audio-lote.ndjson](piloto/audio-lote.ndjson) é uma tentativa alternativa interrompida e serve como histórico. A legenda extraída está em [legenda.txt](piloto/legenda.txt), e a apresentação extraída em [slides.txt](piloto/slides.txt).
- [comparar.py](piloto/comparar.py) compara as duas fontes textuais e as faixas temporais. [comparacao.txt](piloto/comparacao.txt) preserva a saída do cruzamento. Os clipes de verificação estão registrados em [fonte-clipes.json](piloto/fonte-clipes.json) e [fonte-reteste.json](piloto/fonte-reteste.json).
- [redacao.txt](piloto/redacao.txt) é o insumo editorial consolidado da versão final. [montagem.py](piloto/montagem.py) aplica os estilos existentes e adiciona a numeração nativa, duas frações editáveis e o mapa. Para repetir a montagem sem substituir o Word aprovado, execute o script em uma cópia descartável da pasta do piloto.
- [render-teste](piloto/render-teste/) preserva PDFs exportados pelo Word e imagens de revisão. O arquivo v3-word.pdf corresponde ao DOCX aprovado. As versões 1 e 2 são evidências de revisão, com os problemas e as correções descritos no registro.
- A conversa original recebeu HTTP 400 ao processar o áudio anexado, inclusive depois em mensagens de texto. A recuperação usou leitura dos arquivos locais e transcrição no computador. Consulte [Incidente de áudio](piloto/Incidente-de-audio.md).

## Limites do acervo recuperado

O histórico também menciona dois PDFs com nomes genéricos, Legenda aula.pdf e slide aula.pdf. Esses nomes já não estavam presentes nas pastas consultadas. Os PDFs com nomes completos, usados e conferidos no piloto, estão no acervo. Não foi possível confirmar se os anexos de nomes genéricos eram cópias idênticas.

O código local usa um modelo Whisper armazenado separadamente. A configuração de exemplo aponta onde inserir os caminhos do seu ambiente. Para a próxima aula, forneça as fontes e o código do Saturno, e indique qualquer alteração específica de escopo ou formato.
