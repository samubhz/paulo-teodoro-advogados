# Site do Paulo Teodoro: nova estrutura e protótipo

Data: 2026-10-31 · Base: todo o conteúdo do site atual (pauloteodoro.adv.br, WordPress) e o LinkedIn.
O protótipo tem **164 páginas** navegáveis. Abrir `index.html` no navegador. O site real não foi alterado: não temos acesso ao WordPress.

## 1. O que muda, em uma frase

O tributário sai do Paulo Teodoro e passa a ser apresentado como **PJR Consultoria Tributária, empresa do grupo**; o escritório se reposiciona em torno do que sobra (trabalhista, sindical, cível, societário e recuperação judicial) com a nova identidade, mantendo todo o conteúdo que já existe.

## 2. O que foi aproveitado do site atual

Tudo foi extraído do site atual para `dados/conteudo_site_atual.json` e reorganizado pelo gerador `build_site.py` (rodar `python3 build_site.py` refaz as páginas).

| Conteúdo | Quantidade | Onde fica no protótipo |
|---|---|---|
| Artigos (texto completo e imagens) | 91 | `artigos.html` (busca e filtro por tema) e `artigos/*.html` |
| Eventos (texto completo e fotos) | 40 | `eventos.html` e `eventos/*.html` |
| Advogados (foto, cargo, e-mail, currículo) | 9 | `advogados.html` e `advogados/*.html` |
| Áreas do direito (5) | 5 | `areas.html` e `areas/*.html` |
| Setores (6) com foto de capa | 6 | `setores.html` e `setores/*.html` |
| Nosso escritório, história, diferenciais, compliance, trabalhe conosco | 5 | `escritorio.html`, `historia.html`, `diferenciais.html`, `compliance.html`, `trabalhe-conosco.html` |
| Imagens | 113 | `img/` (otimizadas, 6,7 MB no total) |

**Artigos e eventos tributários:** 22 artigos e 10 eventos têm tema tributário (classificação automática por palavras-chave; vale revisar). Aparecem com a etiqueta **"Tributário · PJR"**, e a página de cada artigo mostra um aviso com o selo e link para o PJR. A lista está também em `tributario.html`.

## 3. Mapa do site novo

| Página | Situação |
|---|---|
| Início | Refeita: promessa clara, áreas, faixa do PJR, setores com foto, sócios, galeria "Em campo", artigos recentes, estrutura de apoio, contato |
| Escritório (4 páginas) | Texto original mantido, em novo layout |
| Áreas do direito (5) | Texto original mantido; "advogados responsáveis" viram links para as páginas dos advogados |
| **Tributário** | **Substituída** pela página-ponte "O tributário agora é PJR". A URL antiga deve redirecionar (301) |
| Setores (6) | Texto e foto original mantidos |
| Advogados (9) | Fotos e currículos originais; Reinaldo e Aleksandra com etiqueta do PJR **[confirmar]** |
| Artigos e Eventos | Todo o acervo, com busca e filtro |
| Contato | Endereço, redes e e-mail de cada advogado; duas portas: escritório e PJR |

Elementos globais: lockup novo no cabeçalho, botão "Tributário · PJR" destacado, rodapé com lockup negativo e seção "Grupo", cores ouro como base e verde como toque.

## 4. Inconsistências e pontos a decidir

1. **"Há 16 anos no mercado"** (Nosso Escritório) contradiz a História ("fundaram o escritório em 2003") e o LinkedIn. No protótipo usei "Desde 2003". **[Confirmar]**
2. **"Mais de 20 advogados"**: o site lista 9 advogados e o LinkedIn, 28 funcionários. Não usei o número.
3. **Quem vai para o PJR?** Reinaldo Lage é "Sócio e Gerente **Tributário e Societário**" e Aleksandra Alves é advogada de Direito Tributário. Reinaldo continua responsável pelo **societário**; precisamos saber se esse trabalho fica no Paulo Teodoro ou vai para o PJR. **[Confirmar com os sócios]**
4. **O J do PJR:** a página História diz que **Paulo Teodoro e Jeferson Costa fundaram o escritório em 2003**. Reforça que o J é Jeferson Costa. **[Confirmar]** Jeferson é "Sócio e Gerente Trabalhista e Cível".
5. A página **Recuperação Judicial** repete o bloco "Planejamento Sucessório", que parece vir da página Societário (cópia).
6. Na lista **Especialidades**, o Tributário aparecia com "Preventivo Trabalhista" (cópia errada); o título das abas ainda era "Novo Site".
7. O site antigo não mostra **datas** nos artigos e eventos; a ordem do protótipo segue a lista original (mais recente primeiro).
8. A bio do Instagram fala em terceiro setor, o site, em empresas. Alinhar.

## 5. Fotos e imagens

- **Imagens geradas por IA (Higgsfield, modelo GPT Image 2.5, 8 imagens, cerca de 22 créditos):** os 6 setores (transporte, construção civil, hospital, comércio, educação, metalurgia), mais uma biblioteca jurídica (início e áreas) e uma sala de reuniões (escritório e citação da missão). Sem pessoas, logos nem texto, **em tons dourados e âmbar** (segunda geração, a pedido: o site não usa mais verde). Ficam em `img/ia-*.webp`. O rodapé informa que as imagens de setores e ambientes são ilustrativas e geradas por IA.

- **Usadas:** fotos de eventos (SETCEMG, negociação coletiva em Brasília, Dia da Mulher, equipe), capas de setores, retratos dos 9 advogados, imagens dos artigos.
- **Limitação:** os retratos do site antigo têm só 302 px de largura. Funcionam nos cartões, mas ficam moles em tamanho maior. Recomendo **sessão de fotos** com os sócios e o escritório (fachada, recepção, reunião), que é o que mais falta para o site parecer à altura do escritório.
- Os banners dos artigos (com texto) foram mantidos dentro dos artigos, mas não nos cartões; os cartões usam capas de marca por tema.

## 6. Como publicar no WordPress

1. Criar as páginas no tema atual (ou novo) usando o protótipo como referência de seções, ordem e textos; o conteúdo está em `dados/conteudo_site_atual.json`.
2. Subir os SVGs de `img/` (lockups, símbolo, selo) e as imagens otimizadas.
3. Criar `/tributario/` como página-ponte e redirecionar a URL antiga.
4. Remover o Tributário do menu e da lista de Especialidades.
5. Trocar os títulos das abas ("Novo Site") e conferir meta tags.

## 7. Pendências

- Confirmações dos sócios: itens 1, 3 e 4 da seção 4, e a redação da faixa do PJR.
- Sessão de fotos.
- Fontes: o protótipo agora usa **Cormorant Garamond** (títulos) e **Inter** (texto), ambas livres (licença OFL) e carregadas do Google Fonts; para publicar sem depender da internet, hospedar os arquivos no próprio site.
- URL definitiva do PJR (o protótipo aponta para `samubhz.github.io/pjr-consultoria-tributaria`).
- Formulário de contato e "Trabalhe conosco": o protótipo usa e-mail e WhatsApp; o formulário precisa ser refeito no WordPress.

## 8. Direção visual v3 (dourado, ícones e infográficos)

- **Paleta:** dourado como base (`#B8893A`, `#D9AE5B`), marrom-escuro `#1C1409` no lugar do verde (topo, rodapé, textos e botões) e creme `#FAF6EC`. **O verde aparece só na parte do PJR**, que usa a identidade do PJR.
- **Banners:** todas as imagens em tons dourados e âmbar (biblioteca no início e nas áreas, sala de reunião nas páginas do escritório, um cenário por setor).
- **Ícones:** conjunto próprio de 28 ícones de linha (`icons.py`) para áreas, ações, estrutura de apoio, contato e setores. Podem ser trocados por um conjunto desenhado à mão: basta substituir os traçados do arquivo.
- **Áreas de serviço:** cartões com ícone grande, subáreas com ícone e marca-d'água; páginas de área em painéis numerados, com visão geral clicável, lista com marcadores, advogados com foto e setores atendidos. A página de áreas ganhou o infográfico "Três frentes em cada área" (preventivo, consultivo, contencioso).
- **Estrutura de apoio:** infográfico em linha com cinco ícones (plataforma web, relatórios, atendimento, informativos, cursos).
- **PJR:** faixa em fundo verde com a foto do site do PJR, o grafismo do PJR, os três serviços com ícone e o selo "uma empresa do grupo" em moldura dourada. Repetida na página Tributário e nos avisos dos artigos tributários.
