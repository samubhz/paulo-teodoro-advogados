"""Gera o protótipo do novo site do Paulo Teodoro a partir do conteúdo do site atual.
Uso: python3 build_site.py   (lê dados/*.json e img/, escreve as páginas em ./)
"""
import json, os, re, html, shutil
from icons import icon

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
C = json.load(open('dados/conteudo_site_atual.json', encoding='utf-8'))
ORD = json.load(open('dados/ordem_listas.json', encoding='utf-8'))
WA = 'https://api.whatsapp.com/send?phone=5531992172016'
PJR_URL = 'https://samubhz.github.io/pjr-consultoria-tributaria/'
UP = 'https://pauloteodoro.adv.br/wp-content/uploads/'
esc = html.escape


# ---------- utilidades ----------
def local_img(url):
    base = os.path.splitext(url.replace(UP, '').replace('/', '_'))[0]
    f = f'img/{base}.webp'
    return f if os.path.exists(f) else None


def strip(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def excerpt(d, n=190):
    for b in d['blocks']:
        if b['t'] == 'html':
            t = strip(b['h'])
            if len(t) > 40:
                return t[:n].rsplit(' ', 1)[0] + '…' if len(t) > n else t
    return ''


def thumb(d):
    from PIL import Image
    for b in d['blocks']:
        if b['t'] == 'img':
            f = local_img(b['src'])
            if not f:
                continue
            try:
                w, h = Image.open(f).size
            except Exception:
                continue
            if w >= 380 and 0.55 <= w / h <= 2.4:
                return f
    return None


def title_case(t):
    """Títulos em caixa alta viram caixa de frase."""
    t = t.strip()
    if t.isupper() and len(t) > 12:
        t = t.capitalize()
        t = re.sub(r'\bPjs\b', 'PJs', t)
        for w in ['Adi', 'Pec', 'Tst', 'Irr', 'Icms', 'Pis', 'Cofins', 'Itcmd', 'Antt', 'Ntc', 'Lgpd']:
            t = re.sub(rf'\b{w}\b', w.upper(), t)
    return t


def tag_of(title, ex=''):
    s = (title + ' ' + ex).lower()
    if re.search(r'tribut|icms|pis\b|cofins|itcmd|imposto|fiscal|lucro presumido|ipi\b|\biss\b|reforma tribut|dctf|ecf|sped', s):
        return 'Tributário'
    if re.search(r'sindic|convenç|negocia[çc]|dissídio|acordo coletivo', s):
        return 'Sindical'
    if re.search(r'trabalh|jornada|motorista|empregad|rescis|horas extras|aviso|acidente|justiça do trabalho|disciplinar|pejot', s):
        return 'Trabalhista'
    if re.search(r'contrat|civil|cobran|consumidor|holding|sucess|lgpd|responsabilidade|obras|imobili', s):
        return 'Cível e contratos'
    return 'Geral'


SECTORS = [('transporte', 'Transporte', 'transporte'), ('construcao-civil', 'Construção civil', 'construcao-civil'),
           ('hospital', 'Hospital', 'hospital'), ('comercio-varejista-e-atacadista', 'Comércio varejista e atacadista', 'comercio-varejista-e-atacadista'),
           ('educacao', 'Educação', 'educacao'), ('metalurgia', 'Metalurgia', 'metalurgia')]
AREAS = [('trabalhista', 'Trabalhista'), ('sindical', 'Sindical'), ('civil', 'Cível'), ('societario', 'Societário'),
         ('recuperacao-judicial', 'Recuperação judicial')]
LAW = [('paulo-teodoro', 'Paulo Teodoro'), ('jeferson-costa', 'Jeferson Costa'), ('reinaldo-lage', 'Reinaldo Lage'),
       ('aleksandra-alves', 'Aleksandra Alves'), ('isabela-cunha', 'Isabela Cunha'), ('leticia-lacerda', 'Letícia Lacerda'),
       ('luiz-talhas', 'Luiz Talhas'), ('marcio-mata', 'Marcio Mata'), ('nathalia-galvao', 'Nathália Galvão')]
LAW_BY_NAME = {n: s for s, n in LAW}
LAW_BY_NAME['Nathalia Galvão'] = 'nathalia-galvao'
SECTOR_LIST = ['Transporte', 'Construção Civil', 'Hospital', 'Comércio Varejista e Atacadista', 'Educação', 'Metalurgia']
PJR_LAW = {'reinaldo-lage': 'Sócio do PJR', 'aleksandra-alves': 'Tributário · PJR'}  # [confirmar com os sócios]

# ---------- layout ----------
CSS = open('css/style.css', encoding='utf-8').read() if os.path.exists('css/style.css') else ''


def layout(path, title, desc, body, depth=0, active='', og=None):
    p = '../' * depth
    nav = [('escritorio', 'Escritório', 'escritorio.html'), ('areas', 'Áreas', 'areas.html'), ('setores', 'Setores', 'setores.html'),
           ('advogados', 'Advogados', 'advogados.html'), ('conteudos', 'Conteúdos', 'artigos.html'), ('contato', 'Contato', 'contato.html')]
    nav_html = ''.join(f'<li><a href="{p}{h}"{" aria-current=page" if k == active else ""}>{n}</a></li>' for k, n, h in nav)
    out = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#1C1409"><meta name="robots" content="noindex,nofollow">
<link rel="icon" href="{p}img/avatar-pt.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}css/style.css"></head><body>
<a class="skip" href="#main">Pular para o conteúdo</a>
<div class="topbar"><div class="wrap"><span>Belo Horizonte · atuação nacional</span><span><a href="{WA}">WhatsApp (31) 99217-2016</a> <i>·</i> <a href="https://www.linkedin.com/company/paulo-teodoro-advogados-associados/">LinkedIn</a> <i>·</i> <a href="{p}tributario.html">PJR Consultoria Tributária</a></span></div></div>
<header class="site"><div class="wrap"><a class="brand" href="{p}index.html" aria-label="Paulo Teodoro Advogados Associados, página inicial"><img src="{p}img/lockup-pt-positivo.svg" alt="Paulo Teodoro Advogados Associados" height="56"></a>
<nav aria-label="Principal"><ul>{nav_html}<li><a class="pjr" href="{p}tributario.html">Tributário · PJR</a></li></ul></nav></div></header>
<main id="main">{body}</main>
<footer><div class="wrap"><div class="grid"><div><img class="flogo" src="{p}img/lockup-pt-negativo.svg" alt="Paulo Teodoro Advogados Associados" height="70"><p>Assessoria jurídica para empresas, entidades de classe e terceiro setor, desde 2003, em Belo Horizonte.</p></div>
<div><h4>Escritório</h4><ul><li><a href="{p}escritorio.html">Sobre nós</a></li><li><a href="{p}historia.html">Nossa história</a></li><li><a href="{p}compliance.html">Compliance</a></li><li><a href="{p}trabalhe-conosco.html">Trabalhe conosco</a></li></ul></div>
<div><h4>Conteúdo</h4><ul><li><a href="{p}areas.html">Áreas do direito</a></li><li><a href="{p}artigos.html">Artigos</a></li><li><a href="{p}eventos.html">Eventos</a></li><li><a href="{p}contato.html">Contato</a></li></ul></div>
<div><h4>Grupo</h4><ul><li><a href="{p}tributario.html">PJR Consultoria Tributária</a></li><li><a href="{WA}">WhatsApp</a></li><li><a href="https://www.linkedin.com/company/paulo-teodoro-advogados-associados/">LinkedIn</a></li><li><a href="https://www.instagram.com/pauloteodoro.adv/">Instagram</a></li></ul></div></div>
<div class="legal"><span>© 2026 Paulo Teodoro — Advogados Associados. Todos os direitos reservados.</span><span>O conteúdo deste site tem caráter informativo e não constitui promessa de resultado. A publicidade jurídica observa o Código de Ética e Disciplina da OAB e o Provimento 205/2021 do Conselho Federal. As imagens de setores e ambientes são ilustrativas, geradas por inteligência artificial.</span></div></div></footer></body></html>'''
    full = os.path.join(path)
    os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
    open(full, 'w', encoding='utf-8').write(out)


def banner(p, eyebrow, title, img=None, sub=''):
    st = f' style="background-image:linear-gradient(90deg,rgba(28,20,9,.9) 0%,rgba(28,20,9,.42) 100%),url({p}{img})"' if img else ''
    return f'<section class="pagehero"{st}><div class="wrap"><p class="eyebrow">{esc(eyebrow)}</p><h1>{title}</h1>{f"<p class=sub>{sub}</p>" if sub else ""}</div></section>'


def crumbs(p, items):
    return '<nav class="crumbs wrap" aria-label="Você está em"><a href="%sindex.html">Início</a>' % p + ''.join(f' <span>/</span> {i}' for i in items) + '</nav>'


def render_blocks(blocks, p, skip_titles=()):
    """Converte blocos do site antigo em HTML limpo (conteúdo corrido)."""
    out = ''
    names_mode = False
    for b in blocks:
        t = b['t']
        if t == 'img':
            continue
        if t == 'h':
            h = b['h'].strip().replace('​', '')
            if h in ('Setores Econômicos', 'Especialidades do Escritório', 'Nosso Escritório', 'Áreas do Direito') or h in skip_titles:
                continue
            if h == 'Advogados Responsáveis':
                names_mode = True
                out += '<h3 class="resp">Advogados responsáveis</h3>'
                continue
            names_mode = False
            out += f'<h2>{esc(h.capitalize() if h.isupper() else h)}</h2>'
        elif t == 'html':
            out += b['h']
        elif t == 'list':
            items = b['items']
            if items == SECTOR_LIST or items == ['Nossa História', 'Porque Somos Diferentes', 'Compliance'] or items == ['Enviar e-mail']:
                continue
            if names_mode:
                chips = ''
                for it in items:
                    s = LAW_BY_NAME.get(it)
                    chips += f'<a class="chip" href="{p}advogados/{s}.html">{esc(it)}</a>' if s else f'<span class="chip">{esc(it)}</span>'
                if out.endswith('</div>') and '<div class="chips">' in out[-4000:] and out.rstrip().rsplit('<div class="chips">', 1)[-1].count('<h') == 0 and out.rstrip().endswith('</div>') and not out.rstrip().endswith('</p></div>') and out.rsplit('<div class="chips">', 1)[0].endswith('</h3>'):
                    out = out[:-6] + chips + '</div>'
                elif out.endswith('</div>') and out.rsplit('<div class="chips">', 1)[0].endswith('</h3>') and '<div class="chips">' in out:
                    out = out[:-6] + chips + '</div>'
                else:
                    out += f'<div class="chips">{chips}</div>'
            else:
                out += '<ul class="check">' + ''.join(f'<li>{esc(i)}</li>' for i in items) + '</ul>'
    return out


# ---------- dados derivados ----------
posts = []
for kind in ('artigos', 'eventos'):
    for i, s in enumerate(ORD[kind]):
        d = C.get(s)
        if not d:
            continue
        ttl = title_case(d['title'] or s.replace('-', ' ').capitalize())
        ex = excerpt(d)
        posts.append(dict(kind=kind, slug=s, title=ttl, ex=ex, thumb=thumb(d) if kind == 'eventos' else None, tag=tag_of(ttl, ex), d=d, pos=i))
ART = [x for x in posts if x['kind'] == 'artigos']
EV = [x for x in posts if x['kind'] == 'eventos']


def cut(t, n):
    t = t.rstrip('…')
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0].rstrip(',;:.') + '…'


def card(x, p):
    href = f'{p}{x["kind"]}/{x["slug"]}.html'
    cls = {'Trabalhista': 'trab', 'Sindical': 'sind', 'Cível e contratos': 'civ', 'Tributário': 'trib', 'Geral': 'ger'}[x['tag']]
    img = f'<img src="{p}{x["thumb"]}" alt="" loading="lazy">' if x['thumb'] else f'<div class="ph {cls}"><img src="{p}img/simbolo-pt.svg" alt=""><span>{x["tag"] if x["kind"] == "artigos" else "Evento"}</span></div>'
    badge = '<span class="badge pjr">Tributário · PJR</span>' if x['tag'] == 'Tributário' else f'<span class="badge">{x["tag"]}</span>'
    return f'<a class="post" href="{href}" data-t="{esc((x["title"] + " " + x["ex"]).lower())}" data-tag="{x["tag"]}"><div class="pimg">{img}</div><div class="pbody">{badge}<h3>{esc(x["title"])}</h3><p>{esc(cut(x["ex"], 140))}</p></div></a>'


SELO = '<img class="selo" src="%simg/selo-pjr-positivo.svg" alt="PJR Consultoria Tributária, uma empresa do grupo Paulo Teodoro Advogados Associados">'
SELO_N = '<img class="selo" src="%simg/selo-pjr-negativo.svg" alt="PJR Consultoria Tributária, uma empresa do grupo Paulo Teodoro Advogados Associados">'


# ---------- componentes com ícones ----------
SECTOR_ICON = {'transporte': 'truck', 'construcao-civil': 'crane', 'hospital': 'cross', 'comercio-varejista-e-atacadista': 'store', 'educacao': 'cap', 'metalurgia': 'factory'}
AREA_META = {
    'trabalhista': ('id', [('scale', 'Contencioso trabalhista'), ('shield', 'Preventivo trabalhista')]),
    'sindical': ('users', [('exchange', 'Negociações coletivas'), ('compass', 'Consultoria e assessoria')]),
    'civil': ('scale', [('scale', 'Contencioso cível'), ('compass', 'Consultoria cível')]),
    'societario': ('briefcase', [('document', 'Contratos e atas societárias'), ('org', 'Planejamento sucessório')]),
    'recuperacao-judicial': ('trend', [('document', 'Lei 11.101/2005'), ('shield', 'Preservação da empresa e do emprego')]),
}


def ibadge(name, cls=''):
    return f'<span class="ibadge {cls}">{icon(name)}</span>'


def acard(s, n, p):
    ic, subs = AREA_META[s]
    lis = ''.join(f'<li><span class="si">{icon(i)}</span>{esc(t)}</li>' for i, t in subs)
    return f'<a class="acard" href="{p}areas/{s}.html"><span class="wm">{icon(ic)}</span>{ibadge(ic, "lg")}<h3>{n}</h3><ul class="subs">{lis}</ul><span class="more">Ver detalhes →</span></a>'


def tax_card(p):
    lis = ''.join(f'<li><span class="si">{icon(i)}</span>{t}</li>' for i, t in [('scale', 'Contencioso tributário'), ('compass', 'Consultivo e compliance'), ('doc-search', 'Revisões fiscais')])
    return f'<a class="acard tax" href="{p}tributario.html"><span class="wm">{icon("scale")}</span>{ibadge("chart", "lg")}<h3>Tributário · PJR</h3><ul class="subs">{lis}</ul><span class="more">Conhecer o PJR →</span></a>'


def sector_card(p, s, n):
    return (f'<a class="sector" href="{p}setores/{s}.html" style="background-image:linear-gradient(0deg,rgba(28,20,9,.9),rgba(28,20,9,.1) 66%),url({p}img/ia-{s}.webp)">'
            f'{ibadge(SECTOR_ICON[s])}<span class="t">{n}</span></a>')


def pjrband(p):
    return f'''<section class="pjrband"><div class="wrap"><div class="pjrgrid"><div><p class="eyebrow">Tributário</p><h2>A área tributária agora tem casa própria: o PJR.</h2>
<p>Toda a atuação tributária, consultiva e contenciosa, passa a ser conduzida pelo PJR Consultoria Tributária, empresa do grupo Paulo Teodoro, com foco total na reforma tributária e na redução de riscos fiscais.</p>
<div class="pfeat"><div>{ibadge("scale")}<b>Contencioso tributário</b><span>Preventivo, administrativo e judicial</span></div><div>{ibadge("compass")}<b>Consultivo tributário</b><span>Compliance, planejamento e consultas</span></div><div>{ibadge("doc-search")}<b>Revisões fiscais</b><span>Apurações e obrigações acessórias</span></div></div>
<a class="btn gold" href="{p}tributario.html">Conhecer o PJR</a></div>
<div class="pframe"><img src="{p}img/selo-pjr-negativo.svg" alt="PJR Consultoria Tributária, uma empresa do grupo Paulo Teodoro Advogados Associados"><small>PJR Consultoria Tributária · uma empresa do grupo Paulo Teodoro</small></div></div></div></section>'''


SUPPORT = [('monitor', 'Plataforma web', 'Acompanhamento em tempo real dos processos e da movimentação financeira.'),
           ('chart', 'Relatórios', 'Quantitativos, analíticos e qualitativos de processos, passivo e riscos.'),
           ('video', 'Atendimento', 'Presencial ou por videoconferência, em estrutura moderna.'),
           ('mail', 'Informativos', 'Mudanças legislativas de interesse da empresa, direto por e-mail.'),
           ('book', 'Cursos e palestras', 'Treinamentos nas diversas áreas do direito.')]


def support_section():
    items = ''.join(f'<div>{ibadge(i, "dark lg")}<b>{t}</b><p>{d}</p></div>' for i, t, d in SUPPORT)
    return f'<section class="support"><div class="wrap"><div class="head"><p class="eyebrow">Estrutura de apoio ao cliente</p><h2>Acompanhamento de perto, em tempo real.</h2></div><div class="sup">{items}</div></div></section>'


def lawyer_photo(slug):
    for b in C[slug]['blocks']:
        if b['t'] == 'img' and 'logo' not in b['src'] and local_img(b['src']):
            return local_img(b['src'])


def panel_icon(t):
    t = (t or '').lower()
    for k, v in (('contenc', 'scale'), ('prevent', 'shield'), ('consult', 'compass'), ('negoc', 'exchange'), ('sucess', 'org'), ('societ', 'briefcase'), ('recupera', 'trend')):
        if k in t:
            return v
    return 'document'


def area_page(s, n):
    d = C[s]
    skip = {n.lower(), 'civil', dict(AREAS)[s].lower(), 'áreas do direito', 'setores econômicos', 'especialidades do escritório', 'nosso escritório'}
    panels, cur, intro, resp, mode = [], None, '', [], None
    for b in d['blocks']:
        t = b['t']
        if t == 'h':
            h = b['h'].strip().replace('\u200b', '')
            if h.lower() in skip:
                continue
            if h == 'Advogados Responsáveis':
                mode = 'resp'
                continue
            mode = 'panel'
            cur = {'title': h.capitalize() if h.isupper() else h, 'items': []}
            panels.append(cur)
        elif t == 'list':
            items = b['items']
            if items == SECTOR_LIST:
                mode = None
                continue
            if items == ['Enviar e-mail']:
                continue
            if mode == 'resp':
                resp += items
            elif mode is not None or cur is not None or True:
                if cur is None:
                    cur = {'title': None, 'items': []}
                    panels.append(cur)
                cur['items'] += items
        elif t == 'html' and mode != 'resp':
            intro += b['h']
    for p_ in panels:
        if not p_['title']:
            p_['title'] = {'societario': 'Atuação societária', 'recuperacao-judicial': 'Recuperação judicial'}.get(s, f'Atuação em direito {n.lower()}')
    ic = AREA_META[s][0]
    over = ''.join(f'<a href="#p{i}">{ibadge(panel_icon(p_["title"]) if p_["title"] not in ("Atuação societária", "Recuperação judicial") else ic, "sm")}{esc(p_["title"])}</a>' for i, p_ in enumerate(panels))
    pan = ''
    for i, p_ in enumerate(panels):
        pi = ic if p_['title'] in ('Atuação societária', 'Recuperação judicial') else panel_icon(p_['title'])
        lis = ''.join(f'<li>{icon("check", "ck")}<span>{esc(x)}</span></li>' for x in p_['items'])
        pan += f'<article class="panel" id="p{i}"><div class="phead">{ibadge(pi)}<div><small>{i + 1:02d}</small><h3>{esc(p_["title"])}</h3></div></div><ul class="ilist">{lis}</ul></article>'
    rl = ''
    for name in resp:
        sl = LAW_BY_NAME.get(name)
        if sl:
            rl += f'<a href="../advogados/{sl}.html"><img src="../{lawyer_photo(sl)}" alt="">{esc(name)}</a>'
    secs = ''.join(f'<a href="../setores/{a}.html">{ibadge(SECTOR_ICON[a], "sm")}{b}</a>' for a, b, _ in SECTORS)
    body = banner('../', 'Áreas do direito', n, 'img/ia-biblioteca.webp') + '<section><div class="wrap">'
    body += (f'<div class="prose" style="margin-bottom:34px">{intro}</div>' if intro.strip() else '')
    body += f'<div class="over">{over}</div><div class="panels">{pan}</div>'
    body += (f'<h3 class="resp">Advogados responsáveis</h3><div class="rlaw">{rl}</div>' if rl else '')
    body += f'<h3 class="resp">Setores atendidos</h3><div class="rsec">{secs}</div></div></section>'
    body += f'<section class="band"><div class="wrap"><div class="in" style="grid-template-columns:1fr"><div><p class="eyebrow">Contato</p><h2>Converse com os advogados responsáveis.</h2><p>Atendimento direto, com resposta ágil e foco no resultado que a sua empresa precisa.</p><a class="btn solid" href="{WA}">Chamar no WhatsApp</a></div></div></div></section>'
    layout(f'areas/{s}.html', f'{n} · Paulo Teodoro Advogados Associados', f'Atuação em direito {n.lower()}.', body, 1, 'areas')


def fix_dl(h):
    ICO = {'Endereço': 'pin', 'Redes': 'users', 'Tributário': 'scale'}

    def one(m):
        out = ''
        for k, v in re.findall(r'<div><dt>(.*?)</dt><dd>(.*?)</dd></div>', m.group(0), re.S):
            out += f'<div>{ibadge(ICO.get(k, "check"), "sm")}<div><dt>{k}</dt><dd>{v}</dd></div></div>'
        return f'<dl>{out}</dl>'
    return re.sub(r'<dl>.*?</dl>', one, h, flags=re.S)


# ---------- home ----------
H = lambda f: f
home = f'''<section class="hero2"><div class="wrap"><div class="in"><p class="eyebrow">Paulo Teodoro Advogados Associados · Belo Horizonte</p>
<h1>Soluções jurídicas ágeis para o que o seu negócio precisa decidir.</h1>
<p class="lead">Assessoria trabalhista, sindical, cível e societária para empresas e entidades de classe, com raízes no transporte rodoviário de cargas e atuação em diversos setores da economia.</p>
<a class="btn gold" href="{WA}">Fale com o escritório</a><a class="btn line" href="areas.html">Conheça as áreas</a></div></div>
<div class="wrap"><div class="facts2"><div><b>Desde 2003</b><span>fundado por Paulo Teodoro e Jeferson Costa</span></div><div><b>Abrangência nacional</b><span>empresas e entidades de classe</span></div><div><b>6 setores</b><span>atendidos de perto</span></div><div><b>9 advogados</b><span>em Belo Horizonte</span></div></div></div></section>
<section id="areas"><div class="wrap"><div class="head"><p class="eyebrow">Áreas do direito</p><h2>Do contencioso ao preventivo, o escritório cuida do dia a dia jurídico da empresa.</h2><p>Atuação consultiva e contenciosa, com foco em reduzir riscos e evitar passivo.</p></div>
<div class="acards">'''
AREA_SUB = {'trabalhista': ['Contencioso trabalhista', 'Preventivo trabalhista'], 'sindical': ['Negociações coletivas', 'Consultoria e assessoria'],
            'civil': ['Contencioso cível', 'Consultoria cível'], 'societario': ['Contratos e atas societárias', 'Planejamento sucessório'],
            'recuperacao-judicial': ['Lei 11.101/2005', 'Preservação da empresa e do emprego']}
for s, n in AREAS:
    home += acard(s, n, '')
home += tax_card('')
home += f'''</div></div></section>
{pjrband("")}
<section class="sectors" id="setores"><div class="wrap"><div class="head"><p class="eyebrow">Setores</p><h2>Quem conhece o setor decide melhor.</h2><p>Nossos clientes vêm de segmentos que exigem respostas rápidas e conhecimento do dia a dia da operação.</p></div><div class="sgrid">'''
for s, n, imgn in SECTORS:
    home += sector_card('', s, n)
home += '</div></div></section><section class="quote"><div class="wrap"><blockquote>Viabilizar os projetos dos clientes, atuando de forma ágil, com soluções focadas nos resultados por eles desejados.</blockquote><cite>Nossa missão</cite></div></section><section><div class="wrap"><div class="head"><p class="eyebrow">Sócios</p><h2>Quem está à frente do escritório.</h2></div><div class="lawyers trio">'
for s in ['paulo-teodoro', 'jeferson-costa', 'reinaldo-lage']:
    d = C[s]; ph = [b for b in d['blocks'] if b['t'] == 'img' and local_img(b['src']) and 'logo' not in b['src']]
    role = d['blocks'][2]['items'][0] if len(d['blocks']) > 2 and d['blocks'][2]['t'] == 'list' else ''
    nm = dict(LAW)[s]
    home += f'<a class="lcard" href="advogados/{s}.html"><img src="{local_img(ph[0]["src"])}" alt="{nm}"><h3>{nm}</h3><p>{esc(role)}</p></a>'
home += '</div><p style="margin-top:22px"><a class="more" href="advogados.html">Ver todos os advogados →</a></p></div></section>'
home += '''<section class="gallery"><div class="wrap"><div class="head"><p class="eyebrow">Em campo</p><h2>Presença constante junto ao setor.</h2><p>Palestras, treinamentos, negociações coletivas e eventos das entidades que representamos.</p></div>
<div class="gal">'''
for f, alt in [('2024_06_53806781041_771a9b3e60_k', 'Plateia em palestra no SETCEMG'), ('2024_06_53807026098_98276737ba_k', 'Palestra no SETCEMG'),
               ('2024_05_Negociacao-Coletiva-NTC-em-Brasilia', 'Negociação coletiva em Brasília'), ('2026_03_cc3f1255-02ca-491f-b9b3-bd3d08661ca7', 'Equipe em evento')]:
    home += f'<img src="img/{f}.webp" alt="{alt}" loading="lazy">'
home += '</div><p style="margin-top:22px"><a class="more" href="eventos.html">Ver todos os eventos →</a></p></div></section>'
home += '<section class="sectors"><div class="wrap"><div class="head"><p class="eyebrow">Artigos</p><h2>Análises sobre o que muda para o seu setor.</h2></div><div class="posts">' + ''.join(card(x, '') for x in ART[:6]) + '</div><p style="margin-top:22px"><a class="more" href="artigos.html">Ver todos os artigos →</a></p></div></section>'
home += f'''{support_section()}
<section><div class="wrap contact"><div><p class="eyebrow">Contato</p><h2>Vamos conversar sobre a sua empresa?</h2><p style="color:var(--ink-soft)">Fale direto com o escritório. Para assuntos tributários, o atendimento é do PJR.</p><a class="btn solid" href="{WA}">Chamar no WhatsApp</a><a class="btn ghost" href="contato.html">Todos os contatos</a></div>
<dl><div><dt>Endereço</dt><dd>Av. Antônio Abrahão Caram, 728 · Belo Horizonte, MG · 31275-000</dd></div><div><dt>Redes</dt><dd><a href="https://www.linkedin.com/company/paulo-teodoro-advogados-associados/">LinkedIn</a> · <a href="https://www.instagram.com/pauloteodoro.adv/">Instagram</a></dd></div><div><dt>Tributário</dt><dd><a href="tributario.html">PJR Consultoria Tributária</a></dd></div></dl></div></section>'''
home = fix_dl(home)
layout('index.html', 'Paulo Teodoro Advogados Associados', 'Assessoria jurídica trabalhista, sindical, cível e societária para empresas e entidades de classe, em Belo Horizonte.', home)


# ---------- páginas institucionais ----------
def hero_of(slug):
    return 'img/ia-reuniao.webp'


def simple(slug, out, eyebrow, ttl, active, extra_after=''):
    d = C[slug]
    body = banner('', eyebrow, ttl, hero_of(slug)) + f'<section><div class="wrap"><div class="prose">{render_blocks(d["blocks"], "", (ttl,))}{extra_after}</div></div></section>'
    layout(out, f'{ttl} · Paulo Teodoro Advogados Associados', excerpt(d, 150), body, 0, active)


simple('nosso-escritorio', 'escritorio.html', 'Nosso escritório', 'O escritório', 'escritorio',
       '<p><a class="more" href="historia.html">Nossa história →</a> &nbsp; <a class="more" href="diferenciais.html">Por que somos diferentes →</a> &nbsp; <a class="more" href="compliance.html">Compliance →</a></p>')
simple('nossa-historia', 'historia.html', 'Nosso escritório', 'Nossa história', 'escritorio')
simple('porque-somos-diferentes', 'diferenciais.html', 'Nosso escritório', 'Por que somos diferentes', 'escritorio')
simple('compliance', 'compliance.html', 'Nosso escritório', 'Compliance', 'escritorio')
simple('trabalhe-conosco', 'trabalhe-conosco.html', 'Nosso escritório', 'Trabalhe conosco', 'escritorio')

# áreas
FLOW = '<div class="flow">' + ''.join(f'<div class="step">{ibadge(i, "lg")}<span class="n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for i, n, t, d in [
    ('shield', '01', 'Preventivo', 'Orientação e prevenção de passivo, com avaliação de riscos e rotina em dia.'),
    ('compass', '02', 'Consultivo', 'Pareceres e orientação para decidir com segurança, com informativos das mudanças.'),
    ('scale', '03', 'Contencioso', 'Defesa em todas as esferas, judicial e administrativa, com acompanhamento de perto.')]) + '</div>'
areas_body = banner('', 'Áreas do direito', 'Áreas do direito', 'img/ia-biblioteca.webp', 'Atuação consultiva e contenciosa para empresas e entidades.') + '<section><div class="wrap"><div class="acards">'
for s, n in AREAS:
    areas_body += acard(s, n, '')
areas_body += tax_card('') + '</div><div class="head" style="margin:70px 0 0;max-width:none"><p class="eyebrow">Como atuamos</p><h2>Três frentes em cada área do direito.</h2></div>' + FLOW + '</div></section>'
layout('areas.html', 'Áreas do direito · Paulo Teodoro Advogados Associados', 'Trabalhista, sindical, cível, societário e recuperação judicial.', areas_body, 0, 'areas')
for s, n in AREAS:
    area_page(s, n)

# setores
sec_body = banner('', 'Setores', 'Setores atendidos', 'img/ia-transporte.webp', 'Conhecimento do dia a dia de cada operação.') + '<section><div class="wrap"><div class="sgrid">'
for s, n, imgn in SECTORS:
    sec_body += sector_card('', s, n)
    d = C[s]
    body = banner('../', 'Setores', n, f'img/ia-{s}.webp') + f'<section><div class="wrap"><div class="prose">{render_blocks(d["blocks"], "../", (n,))}<h3 class="resp">Áreas de atuação para o setor</h3><div class="rsec">' + ''.join(f'<a href="../areas/{a}.html">{ibadge(AREA_META[a][0], "sm")}{b}</a>' for a, b in AREAS) + f'<a href="../tributario.html">{ibadge("chart", "sm")}Tributário · PJR</a></div><p style="margin-top:28px"><a class="more" href="../setores.html">← Todos os setores</a></p></div></div></section>'
    layout(f'setores/{s}.html', f'{n} · Paulo Teodoro Advogados Associados', excerpt(d, 150), body, 1, 'setores')
sec_body += '</div></div></section>'
layout('setores.html', 'Setores · Paulo Teodoro Advogados Associados', 'Transporte, construção civil, hospital, comércio, educação e metalurgia.', sec_body, 0, 'setores')

# advogados
adv = banner('', 'Advogados', 'Nossa equipe', 'img/ia-reuniao.webp', 'Sócios e advogados associados.')
adv += '<section><div class="wrap"><div class="lawyers">'
for s, n in LAW:
    d = C[s]; ph = [b for b in d['blocks'] if b['t'] == 'img' and local_img(b['src']) and 'logo' not in b['src']]
    roles = next((b['items'] for b in d['blocks'] if b['t'] == 'list'), [])
    bdg = f'<span class="badge pjr">{PJR_LAW[s]}</span>' if s in PJR_LAW else ''
    adv += f'<a class="lcard" href="advogados/{s}.html"><img src="{local_img(ph[0]["src"])}" alt="{n}"><h3>{n}</h3><p>{esc(" · ".join(roles))}</p>{bdg}</a>'
    email = next((b['items'][0] for b in d['blocks'] if b['t'] == 'list' and '@' in b['items'][0]), '')
    bio = ''.join(b['h'] if b['t'] == 'html' else '' for b in d['blocks']) or ''
    if not bio.startswith('<'):
        bio = '<p>' + bio + '</p>'
    bio_html = ''.join(b['h'] if b['h'].startswith('<') else f'<p>{b["h"]}</p>' for b in d['blocks'] if b['t'] == 'html')
    note = f'<p class="note">{PJR_LAW[s]}: atua na PJR Consultoria Tributária, empresa do grupo. <a href="../tributario.html">Saiba mais</a></p>' if s in PJR_LAW else ''
    page = banner('../', 'Advogados', n, None, esc(' · '.join(roles))) + f'<section><div class="wrap lawpage"><img class="lphoto" src="../{local_img(ph[0]["src"])}" alt="{n}"><div class="prose">{bio_html}{note}' + (f'<p><a class="btn solid" href="mailto:{email}">Enviar e-mail</a></p>' if email else '') + '<p><a class="more" href="../advogados.html">← Todos os advogados</a></p></div></div></section>'
    layout(f'advogados/{s}.html', f'{n} · Paulo Teodoro Advogados Associados', f'{n}, {" · ".join(roles)}.', page, 1, 'advogados')
adv += '</div></div></section>'
layout('advogados.html', 'Advogados · Paulo Teodoro Advogados Associados', 'Sócios e advogados associados do escritório.', adv, 0, 'advogados')

# artigos
tags = ['Todos', 'Trabalhista', 'Sindical', 'Cível e contratos', 'Tributário', 'Geral']
fil = ''.join(f'<button type="button" class="fbtn{" on" if t == "Todos" else ""}" data-f="{t}">{t}</button>' for t in tags)
art = banner('', 'Conteúdos', 'Artigos', 'img/2024_04_hero-artigos.webp', f'{len(ART)} análises sobre legislação, jurisprudência e a rotina das empresas.')
art += f'''<section><div class="wrap"><div class="tools"><input id="q" type="search" placeholder="Buscar por tema, lei ou setor" aria-label="Buscar artigos"><div class="fbar">{fil}</div></div>
<p class="count" id="cnt"></p><div class="posts" id="list">''' + ''.join(card(x, '') for x in ART) + '''</div></div></section>
<script>(function(){var q=document.getElementById('q'),L=[].slice.call(document.querySelectorAll('#list .post')),b=[].slice.call(document.querySelectorAll('.fbtn')),f='Todos',c=document.getElementById('cnt');
function r(){var s=q.value.toLowerCase().trim(),n=0;L.forEach(function(e){var ok=(f==='Todos'||e.dataset.tag===f)&&(!s||e.dataset.t.indexOf(s)>-1);e.style.display=ok?'':'none';if(ok)n++});c.textContent=n+' artigo'+(n===1?'':'s')}
q.addEventListener('input',r);b.forEach(function(x){x.addEventListener('click',function(){f=x.dataset.f;b.forEach(function(y){y.classList.toggle('on',y===x)});r()})});r()})();</script>'''
layout('artigos.html', 'Artigos · Paulo Teodoro Advogados Associados', 'Artigos sobre direito trabalhista, sindical, cível e outros temas de interesse das empresas.', art, 0, 'conteudos')
for k, lst, label, hero in (('artigos', ART, 'Artigo', 'img/2024_04_hero-artigos.webp'), ('eventos', EV, 'Evento', 'img/2024_04_hero-noticias.webp')):
    for i, x in enumerate(lst):
        d = x['d']
        blocks = [b for b in d['blocks'] if not (b['t'] == 'img' and 'logo' in b['src'])]
        body = ''
        for b in blocks:
            if b['t'] == 'img':
                f = local_img(b['src'])
                body += f'<figure><img src="../{f}" alt="{esc(b.get("alt") or x["title"])}" loading="lazy"></figure>' if f else ''
            elif b['t'] == 'html':
                body += b['h'] if b['h'].startswith('<') else f'<p>{b["h"]}</p>'
            elif b['t'] == 'h':
                if b['h'].strip() and b['h'].strip() not in ('Nosso Escritório', 'Setores Econômicos'):
                    body += f'<h2>{esc(b["h"].strip())}</h2>'
            elif b['t'] == 'list' and b['items'] != SECTOR_LIST:
                body += '<ul class="check">' + ''.join(f'<li>{esc(t)}</li>' for t in b['items']) + '</ul>'
        pj = ''
        if x['tag'] == 'Tributário':
            pj = f'<aside class="pjrbox"><div><b>Conteúdo tributário</b><p>A atuação tributária do grupo agora é conduzida pelo PJR Consultoria Tributária.</p><a class="btn solid" href="../tributario.html">Conhecer o PJR</a></div>{SELO_N % "../"}</aside>'
        nav = ''
        if i > 0:
            nav += f'<a href="{lst[i-1]["slug"]}.html">← {esc(lst[i-1]["title"][:70])}</a>'
        if i < len(lst) - 1:
            nav += f'<a class="r" href="{lst[i+1]["slug"]}.html">{esc(lst[i+1]["title"][:70])} →</a>'
        page = crumbs('../', [f'<a href="../{"artigos" if k == "artigos" else "eventos"}.html">{"Artigos" if k == "artigos" else "Eventos"}</a>']) + f'<article class="wrap art"><span class="badge{" pjr" if x["tag"] == "Tributário" else ""}">{label if k == "eventos" else x["tag"]}</span><h1>{esc(x["title"])}</h1><div class="prose">{body}</div>{pj}<div class="pn">{nav}</div></article>'
        layout(f'{k}/{x["slug"]}.html', f'{x["title"]} · Paulo Teodoro Advogados Associados', x['ex'][:155], page, 1, 'conteudos')

# eventos (lista)
ev = banner('', 'Conteúdos', 'Eventos', 'img/2024_04_hero-noticias.webp', 'Palestras, treinamentos, negociações coletivas e participação em entidades.') + '<section><div class="wrap"><div class="posts">' + ''.join(card(x, '') for x in EV) + '</div></div></section>'
layout('eventos.html', 'Eventos · Paulo Teodoro Advogados Associados', 'Palestras, treinamentos e participação do escritório em eventos do setor.', ev, 0, 'conteudos')

# contato
ct = banner('', 'Contato', 'Fale com o escritório', 'img/2024_04_contato.webp', 'Belo Horizonte · atuação nacional')
ct += f'<section><div class="wrap contact"><div><h2>Atendimento direto</h2><p style="color:var(--ink-soft)">Para assuntos tributários, o atendimento é do PJR Consultoria Tributária.</p><a class="btn solid" href="{WA}">Chamar no WhatsApp</a><a class="btn ghost" href="tributario.html">Falar com o PJR</a></div><dl><div><dt>Endereço</dt><dd>Av. Antônio Abrahão Caram, 728 · Belo Horizonte, MG · 31275-000</dd></div><div><dt>Redes</dt><dd><a href="https://www.linkedin.com/company/paulo-teodoro-advogados-associados/">LinkedIn</a> · <a href="https://www.instagram.com/pauloteodoro.adv/">Instagram</a> · <a href="https://www.facebook.com/pages/Paulo-Teodoro-Advogados-Associados/609407505769849">Facebook</a></dd></div></dl></div></section><section class="sectors"><div class="wrap"><div class="head"><h2>Nossos advogados</h2></div><div class="lawyers">'
for s, n in LAW:
    d = C[s]; email = next((b['items'][0] for b in d['blocks'] if b['t'] == 'list' and '@' in b['items'][0]), '')
    roles = next((b['items'] for b in d['blocks'] if b['t'] == 'list'), [])
    ct += f'<div class="lcard flat"><h3>{n}</h3><p>{esc(" · ".join(roles))}</p><a href="mailto:{email}">{email}</a></div>'
ct += '</div></div></section>'
ct = fix_dl(ct)
layout('contato.html', 'Contato · Paulo Teodoro Advogados Associados', 'Endereço, redes e e-mails dos advogados do escritório.', ct, 0, 'contato')

# tributário (ponte)
def info_card(ic, title, items):
    lis = ''.join(f'<li><span class="si">{icon("check")}</span>{esc(i)}</li>' for i in items)
    return f'<article class="acard"><span class="wm">{icon(ic)}</span>{ibadge(ic, "lg")}<h3>{title}</h3><ul class="subs">{lis}</ul></article>'


tb = f'''<section class="pjrband"><div class="wrap"><div class="pjrgrid"><div><p class="eyebrow">Tributário</p><h1 style="color:#fff;font-size:clamp(2.4rem,5vw,3.8rem)">O tributário agora é PJR.</h1>
<p>Toda a atuação tributária do grupo Paulo Teodoro, consultiva e contenciosa, é conduzida pelo PJR Consultoria Tributária, empresa do grupo, especializada na reforma tributária e na redução de riscos fiscais.</p>
<a class="btn gold" href="{PJR_URL}">Ir para o site do PJR</a><a class="btn line" href="index.html">Voltar ao escritório</a></div>
<div class="pframe"><img src="img/selo-pjr-negativo.svg" alt="PJR Consultoria Tributária, uma empresa do grupo Paulo Teodoro Advogados Associados"><small>PJR Consultoria Tributária · uma empresa do grupo Paulo Teodoro</small></div></div></div></section>
<section><div class="wrap"><div class="head"><p class="eyebrow">O que passa a ser do PJR</p><h2>O que antes estava na página Tributário agora está no PJR.</h2></div><div class="acards">
{info_card('scale', 'Contencioso tributário', ['Preventivo, administrativo e judicial', 'Estratégias e teses para redução da carga tributária'])}
{info_card('compass', 'Consultivo tributário', ['Tax compliance e planejamento tributário', 'Regimes especiais e consultas formais', 'Avaliação do risco tributário'])}
{info_card('doc-search', 'Revisões fiscais', ['Apurações de IRPJ, CSLL, PIS, COFINS, ICMS e IPI', 'Obrigações acessórias (SPED, ECF, DCTF e outras)'])}</div></div></section>
<section class="sectors"><div class="wrap"><div class="head"><p class="eyebrow">Conteúdo tributário</p><h2>Artigos e eventos sobre tributário publicados aqui.</h2></div><div class="posts">''' + ''.join(card(x, '') for x in (ART + EV) if x['tag'] == 'Tributário') + f'''</div></div></section>
<section class="band"><div class="wrap in"><div><p class="eyebrow">Um grupo, todas as frentes</p><h2>Você continua com quem já conhece o seu negócio.</h2><p>Se a sua demanda envolve também trabalhista, sindical, cível ou societário, o Paulo Teodoro segue com você. Os dois escritórios trabalham de forma integrada.</p><a class="btn solid" href="{WA}">Falar com o escritório</a></div><div>{ibadge("users", "lg dark")}</div></div></section>'''
layout('tributario.html', 'Tributário · Paulo Teodoro Advogados Associados', 'A atuação tributária do grupo Paulo Teodoro agora é conduzida pelo PJR Consultoria Tributária.', tb, 0, '')
print('páginas:', sum(len(f) for _, _, f in os.walk('.') if False) or '', 'artigos', len(ART), 'eventos', len(EV))
