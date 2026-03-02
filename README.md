Bot desenvolvido em Python utilizando discord.py, responsável por monitorar automaticamente jogadores online de um OTServer (Eagle World) e notificar no Discord sempre que houver mudança de level.

🚀 Funcionalidades
🔎 Faz scraping automático da lista de jogadores online.
📊 Consulta individualmente o perfil de cada jogador.
⬆️ Detecta level up automaticamente.
💀 Atualiza o level mesmo em caso de morte (corrige regressão de level).
💾 Armazena os níveis em arquivo JSON para persistência.
🎯 Envia mensagens personalizadas no Discord com emoji baseado na vocation:
Sorcerer
Druid
Knight
Paladin
🔁 Verificação automática em intervalo configurável (padrão: 60 segundos).

🛠️ Tecnologias Utilizadas
Python 3
discord.py
aiohttp
BeautifulSoup4
asyncio

⚙️ Como Funciona
O bot acessa a página de jogadores online.
Coleta os nomes dos personagens.
Consulta o perfil individual de cada jogador.
Compara o level atual com o level salvo anteriormente.
Caso detecte alteração:
Se aumentou → envia mensagem de level up.
Se diminuiu → apenas atualiza o banco para manter sincronizado.
Salva os dados em player_levels.json.

📂 Estrutura de Persistência
Os dados são armazenados localmente em:
player_levels.json
Isso garante que o bot não perca o histórico ao reiniciar.

🔧 Configuração
No arquivo principal, configure:
TOKEN = 'SEU_TOKEN_HERE'
CHANNEL_ID = SEU_CANAL_ID

💡 Objetivo
Automatizar notificações de progresso de jogadores dentro do servidor, ideal para:
Guilds
Comunidades
Servidores PvP

Acompanhamento competitivo
