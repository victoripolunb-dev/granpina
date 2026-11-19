# Esteira de produção

## Entrada no dia a dia

Anexe o áudio, a transcrição ou PDF de legendas do Gran e os slides da mesma aula neste chat do Codex. Informe o título e o código do Saturno se eles não constarem nos arquivos. Você pode usar a mensagem abaixo.

> Produza o Word desta aula no padrão Gran. Os arquivos são da mesma aula. Título no Saturno: [título]. Código para o nome do arquivo: [código].

O download fica com você. A pasta do projeto guarda o padrão e o registro dos testes. O Codex usa ferramentas locais para transcrever, ler as fontes e gerar o Word. O processamento de uma gravação completa foi validado no piloto documentado em [piloto/Registro.md](piloto/Registro.md). Qualquer integração nova que implique transferir os áudios a um serviço será discutida antes do envio.

## Sequência por aula

| Ordem | Responsável | Evidência para avançar |
|---|---|---|
| 1. Receber e inventariar | Coordenador | Identidade da aula, arquivos, formatos, duração medida, páginas da legenda, quantidade de slides e metadados conhecidos. |
| 2. Cobrir as fontes | Coordenador e subagente A | Registro de processamento do áudio de ponta a ponta com intervalos e lacunas, transcrição com referências de tempo e inventário de todos os slides. Revisar também imagens, tabelas, diagramas e fórmulas. |
| 3. Redigir e montar o Word | Coordenador | Versão por blocos cronológicos com referências internas às fontes e primeira versão do DOCX. Aplicar o prompt e a especificação só após a etapa anterior. |
| 4. Conferir o conteúdo | Subagente B | Comparação independente do DOCX com as fontes. Cada desvio tem bloco, tempo ou página e evidência. |
| 5. Inspecionar o Word | Subagente C | Verificação estrutural e inspeção visual de todas as páginas do mesmo DOCX, em paralelo com a etapa 4. O teste visual inclui elementos que quebram entre páginas. |
| 6. Corrigir e entregar | Coordenador | Corrigir os achados, retestar o que mudou e entregar o DOCX após cumprir os critérios de aceite. Registrar separadamente as pendências que não comprometam a entrega. |
| 7. Refinar | Coordenador | Registrar decisões reutilizáveis e retestar os casos afetados. |

Abra um [registro de andamento](REGISTRO-AULA.md) por aula com os campos do protocolo de qualidade. Use o tempo da gravação para os cortes de cinco minutos. Se uma legenda terminar antes do áudio, por exemplo, a etapa 2 precisa identificar o trecho descoberto e processá-lo. Conferir a duração e ler a legenda fornece evidência de cobertura textual, mas ainda exige processamento integral do áudio.

Na triagem, use o título, o código, a duração e pontos reconhecíveis do início, do meio e do fim da fala. Compare passagens específicas, como um exemplo, uma questão ou um precedente. Considere que uma aula pode aproveitar só parte dos slides. Se o áudio corresponder a outra aula, interrompa a redação, informe quais passagens mostraram a divergência e peça a substituição do arquivo divergente. Se a correspondência ainda for incerta, registre onde comparar antes de concluir a triagem.

O Word entregue de *Reclamação II* serve de referência editorial e visual. Os manuais definem as regras comuns, e o conteúdo da aula determina os componentes a aplicar. Quando uma página do manual mostrar uma aparência específica, confira a página visualmente antes de reproduzi-la.

## Material do projeto

- [ESPECIFICACAO.md](ESPECIFICACAO.md) registra as condições de produção e aceite.
- [REGRAS-GRAN.md](REGRAS-GRAN.md) vincula as regras às páginas das fontes.
- [MODELO-WORD.md](MODELO-WORD.md) registra as evidências e limitações do exemplo disponível.
- [PROMPT.md](PROMPT.md) orienta a redação e a montagem.
- [QUALIDADE.md](QUALIDADE.md) define papéis, evidências, reteste e teste sintético.
- [DECISOES.md](DECISOES.md) registra escolhas e dúvidas que afetam futuras aulas.
- [transcrever_audio.py](transcrever_audio.py) processa o áudio localmente e gera segmentos com tempos para a conferência.
- [montar_word.py](montar_word.py) monta o Word-base com os estilos comuns a partir de blocos revisados. O coordenador complementa no Word os elementos específicos da aula e verifica o resultado com o subagente C.

## Uso técnico

Na pasta do projeto, execute `python gran.py verificar` para checar a configuração local. Em produção, use `python gran.py transcrever arquivo.mp3 transcricao.json` e `python gran.py montar blocos.json entrega.docx`. Fora do ambiente original, configure o Python e os caminhos do transcritor e do modelo conforme o [README.md](README.md).

Para gerar a segunda transcrição da gravação, execute `python transcrever_audio.py arquivo-de-audio saida.json --runtime pasta-do-transcritor --modelo pasta-do-modelo`. Use o diretório local do pacote e o diretório do modelo indicados em sua configuração. O script abre a gravação inteira, executa o Whisper multilíngue em CPU e grava a duração e os segmentos reconhecidos. A duração do arquivo e o fim do último segmento podem diferir por conta de silêncio ou material perdido pelo reconhecedor. O agente de fontes cruza os segmentos com a legenda e verifica os intervalos sem texto antes de liberar a redação. Quando as duas transcrições divergirem em um ponto que mude o conteúdo, localize o minuto para conferência direta na gravação. Se o ponto continuar indeterminado, registre a pendência antes de aprovar a aula.

Use o Python do ambiente de documentos do Codex. Execute `python montar_word.py caminho/dos/blocos.json caminho/da/entrega.docx` com um caminho de saída novo. [A amostra](testes/amostra.json) mostra os tipos de bloco e como anexar o minuto ao parágrafo e encerrar uma caixa de destaque. O programa valida a ordem dos relógios informados. Os revisores ainda conferem a posição de cada relógio na gravação e a cobertura até o último intervalo.

Monte no Word os tipos que precisam de tratamento próprio, como questões numeradas e suas alternativas, gabaritos, equações editáveis, tabelas, imagens e peças. Use as referências específicas de cada tipo e registre a inspeção da versão final. Para rodar os testes do gerador, execute `python -B -m unittest discover -s testes -v` com o mesmo Python.

Tente renderizar com a ferramenta da habilidade de documentos. Se o renderizador estiver indisponível no Windows, abra o DOCX no Microsoft Word, confira todas as páginas a 100% e registre o que observou. Verifique em especial se cada caixa de destaque termina com sua linha, inclusive quando houver caixas próximas.

