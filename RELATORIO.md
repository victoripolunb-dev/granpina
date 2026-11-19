# Relatório de implantação da esteira Gran

**19 de novembro de 2026.** Primeira versão montada e testada com conteúdo fictício. A validação com uma aula completa depende dos arquivos do primeiro piloto.

| Frente | Situação | Evidência |
|---|---|---|
| Regras editoriais e de formatação | Mapeadas | Um agente conferiu o manual, o guia de rotina e o tutorial de equações. As referências de página e as diferenças entre orientações estão em [REGRAS-GRAN.md](REGRAS-GRAN.md). |
| Modelo de entrega | Inspecionado | Um agente comparou a estrutura do Word de *Reclamação II* com o manual e identificou sete arquivos ilustrativos para consulta. O mapa está em [MODELO-WORD.md](MODELO-WORD.md). |
| Equipe e conferência | Definidas | O coordenador produz e corrige. Três subagentes verificam fontes, fidelidade e formatação. Cada achado tem origem e reteste. O procedimento está em [QUALIDADE.md](QUALIDADE.md). |
| Transcrição local | Testada com WAV e MP3 | O Whisper em CPU transcreveu uma gravação sintética de 12,632 s em português brasileiro e reproduziu as três frases esperadas, com tempos por segmento. Um agente repetiu o teste em MP3 com o mesmo resultado textual e registrou o intervalo após o último segmento. Os testes executaram com modelo local e modo offline. |
| Teste editorial | Executado | A revisão detectou seis falhas em sete verificações, incluindo alteração de sentido, omissão e conteúdo exclusivo de slide. A versão corrigida passou nas sete. |
| Geração Word-base | Testada | Três testes automatizados passaram na execução inicial e na repetição independente. O Word de uma página foi aberto no Microsoft Word a 100%. Foram vistos título, corpo, recuo, marcadores, destaque com linha e relógios. |
| Piloto com aula completa | Pendente | Validar o processamento de ponta a ponta do áudio, a integração com os slides, a cobertura da reescrita e a revisão da entrega real. Questões, tabelas, equações, imagens e peças exigem testes quando surgirem. |

O renderizador empacotado encontrou a ausência do LibreOffice neste ambiente. A inspeção da amostra foi feita no Microsoft Word instalado. O gerador aplica os estilos comuns. O coordenador monta os elementos específicos da aula e o revisor confere o documento resultante.

A transcrição usa `faster-whisper` 1.2.1, `av` 16.1.0 e o modelo multilíngue `Systran/faster-whisper-small`. Os pacotes e o modelo foram baixados, e a gravação sintética foi processada localmente. O teste confirma a geração de texto com tempos. A precisão em fala jurídica, a cobertura de gravações longas e o alinhamento com a legenda do Gran precisam ser medidos no piloto.

A revisão cruzada alinhou o fluxo ao critério de liberação e documentou a inspeção no Word como alternativa quando o renderizador estiver indisponível. As decisões provisórias de formatação, incluindo recuo de citação e encerramento institucional, estão em [DECISOES.md](DECISOES.md).

## Teste adicional de identidade das fontes

O transcritor processou uma segunda gravação sintética de 70,654 segundos em 12 segmentos. Identificou o exemplo de Ana no início, o número do processo no meio e o precedente fictício nº 12 no fim. Esses três pontos bateram com a legenda e os slides representados em texto para a aula correspondente. Em um cenário simulado de outra aula com o mesmo título e assunto próximo, nenhum dos três pontos apresentados pelas fontes trocadas apareceu na gravação. Esse cenário testa a regra de triagem com exemplos controlados.

A transcrição produziu “considerisse” no lugar de “considere-se”, entre 26 e 31 segundos, e marcou o fim da fala 0,174 segundo antes do fim do arquivo. Esses casos ficaram registrados como evidência de que a revisão precisa cruzar a legenda com o áudio e examinar os intervalos sem texto.

Para o primeiro piloto, anexe o áudio original, a transcrição ou legenda e os slides da mesma aula. Inclua o título e o código do Saturno se eles não estiverem nos arquivos. A esteira, com os pontos de aceite e o passo a passo, está em [ESTEIRA.md](ESTEIRA.md).

## Configuração para uso recorrente

O [lançador local](gran.py) usa os caminhos registrados no projeto para verificar o ambiente, transcrever áudio ou montar o Word-base. A verificação confirmou a presença do modelo local e o carregamento das bibliotecas de Word, PDF e PowerPoint. O [registro por aula](REGISTRO-AULA.md) está pronto para documentar as fontes, a cobertura e as revisões da versão entregue. As instruções da equipe ficam em [AGENTS.md](AGENTS.md).

## Atualização após o piloto

O piloto Planejamento Conservacionista II foi concluído. A gravação de 35:36,073 foi processada localmente, os 16 slides e a legenda de 33 páginas foram conferidos, e o Word final teve oito páginas revisadas. Consulte o [registro do piloto](piloto/Registro.md) e o [histórico do incidente com o anexo de áudio](piloto/Incidente-de-audio.md).
