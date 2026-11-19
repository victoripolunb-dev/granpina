# Erro de entrada de áudio no Codex

No chat original, o anexo MP3 de Planejamento Conservacionista II foi seguido do erro `Audio input is not available.`. O histórico registrou HTTP 400, `invalid_request_error`, parâmetro `input`. A falha se repetiu quando o usuário pediu para continuar sem áudio, enviou a legenda e os slides em PDF, e tentou mensagens simples de texto.

Uma hipótese é que o contexto daquela conversa continuou carregando uma entrada de áudio incompatível, mesmo em turnos de texto. O histórico confirma a repetição do erro, mas a causa interna não foi verificada.

A produção foi retomada em outro chat. Os arquivos foram lidos do disco e o MP3 foi processado localmente com faster-whisper, sem depender do suporte a anexos de áudio do chat. A conferência cruzou a gravação integral, a legenda e os slides. O resultado e as revisões estão no [registro do piloto](Registro.md).
