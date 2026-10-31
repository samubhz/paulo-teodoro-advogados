"""SEO do protótipo: títulos, descrições, canonical, Open Graph, dados estruturados e sitemap.

No lançamento, ajuste só estas duas linhas e rode `python3 build_site.py`:
    BASE    -> endereço definitivo do site (com barra no fim)
    INDEXAR -> True (libera os buscadores e escreve o sitemap no robots.txt)
"""
import json, re, html, datetime

BASE = 'https://samubhz.github.io/paulo-teodoro-advogados/'
INDEXAR = False
SUFFIX = ' · Paulo Teodoro'
HOJE = datetime.date.today().isoformat()
MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
SOCIAL = ['https://www.linkedin.com/company/paulo-teodoro-advogados-associados/', 'https://www.instagram.com/pauloteodoro.adv/',
          'https://www.facebook.com/pages/Paulo-Teodoro-Advogados-Associados/609407505769849']
ORG_ID = BASE + '#escritorio'
PAGES = []          # (caminho, lastmod) para o sitemap
_titulos = {}


def esc(s):
    return html.escape(s, quote=True)


def data_pt(iso):
    y, m, d = iso[:10].split('-')
    return f'{int(d)} de {MESES[int(m) - 1]} de {y}'


def fit_title(t, suffix=SUFFIX, hi=60):
    t = re.sub(r'\s+', ' ', t).strip()
    if len(t) + len(suffix) <= hi:
        return t + suffix
    if len(t) <= hi:
        return t
    return t[:hi - 1].rsplit(' ', 1)[0].rstrip(' ,;:–-') + '…'


def unique_title(t, path, extra=''):
    if t in _titulos and _titulos[t] != path:
        t2 = fit_title(t.replace(SUFFIX, '')[:48].rsplit(' ', 1)[0] + (f' ({extra})' if extra else ' (2)'), SUFFIX)
        t = t2 if t2 not in _titulos else t2 + ' '
    _titulos[t] = path
    return t


def fit_desc(d, extra=' Paulo Teodoro Advogados, em Belo Horizonte.', lo=110, hi=155):
    d = re.sub(r'\s+', ' ', d or '').strip()
    if len(d) > hi:
        d = d[:hi - 1].rsplit(' ', 1)[0].rstrip(' ,;:–-') + '…'
    elif len(d) < lo and len(d) + len(extra) <= hi:
        d = d.rstrip('.') + '.' + extra
    return d


# ---- textos otimizados das páginas-chave (título sem sufixo, descrição) ----
PAGE_META = {
    'index.html': ('Paulo Teodoro Advogados | Trabalhista, Sindical e Cível', 'Advocacia trabalhista, sindical, cível e societária para empresas e entidades de classe, com raízes no transporte de cargas. Fale com o escritório, em BH.'),
    'areas.html': ('Áreas do direito: trabalhista, sindical e cível', 'Trabalhista, sindical, cível, societário e recuperação judicial: atuação preventiva, consultiva e contenciosa para empresas e entidades. Conheça as áreas.'),
    'areas/trabalhista.html': ('Direito trabalhista para empresas', 'Contencioso e preventivo trabalhista para empresas e entidades, com atuação nacional e experiência no transporte de cargas. Fale com o escritório.'),
    'areas/sindical.html': ('Assessoria sindical e negociação coletiva', 'Negociações coletivas, dissídios, acordos e consultoria para empresas, sindicatos e federações. Atendimento direto do escritório Paulo Teodoro, em BH.'),
    'areas/civil.html': ('Advocacia cível para empresas', 'Contencioso e consultoria cível: responsabilidade civil, contratos, sucessões e direito imobiliário para empresas e associações. Fale com o escritório.'),
    'areas/societario.html': ('Direito societário e planejamento sucessório', 'Contratos sociais, atas, reorganização societária e planejamento sucessório para empresários. Atendimento do Paulo Teodoro Advogados, em BH.'),
    'areas/recuperacao-judicial.html': ('Recuperação judicial de empresas', 'Assessoria a empresas em recuperação judicial (Lei 11.101/2005), para preservar a atividade, o emprego e os interesses dos credores. Fale conosco.'),
    'setores.html': ('Setores atendidos: transporte, saúde e indústria', 'Advocacia para transporte, construção civil, hospital, comércio, educação e metalurgia, com conhecimento do dia a dia de cada operação.'),
    'setores/transporte.html': ('Advocacia para transportadoras e transporte de cargas', 'Advocacia trabalhista, sindical e cível para transportadoras e entidades do transporte rodoviário de cargas, com atuação desde 2003. Fale conosco.'),
    'setores/construcao-civil.html': ('Advocacia para a construção civil', 'Assessoria jurídica para construtoras e empresas de obras: contratos, atrasos, trabalhista e societário, com o atendimento do Paulo Teodoro Advogados.'),
    'setores/hospital.html': ('Advocacia para hospitais e saúde', 'Assessoria jurídica para hospitais e clínicas: trabalhista, cível e contratos, com atendimento direto do escritório Paulo Teodoro, em Belo Horizonte.'),
    'setores/comercio-varejista-e-atacadista.html': ('Advocacia para o comércio varejista e atacadista', 'Assessoria jurídica para empresas do comércio varejista e atacadista: trabalhista, contratos e societário, com o atendimento do Paulo Teodoro Advogados.'),
    'setores/educacao.html': ('Advocacia para instituições de ensino', 'Assessoria jurídica para escolas e instituições de ensino: trabalhista, LGPD, contratos e societário, com atendimento do Paulo Teodoro Advogados, em BH.'),
    'setores/metalurgia.html': ('Advocacia para a metalurgia e a indústria', 'Assessoria jurídica para empresas da cadeia metalúrgica: trabalhista, sindical, cível e societário, com o atendimento do Paulo Teodoro Advogados, em BH.'),
    'advogados.html': ('Advogados e sócios do escritório', 'Conheça os sócios e advogados associados do Paulo Teodoro Advogados Associados, em Belo Horizonte: áreas de atuação, currículo e contato.'),
    'artigos.html': ('Artigos jurídicos para empresas e transportadoras', 'Análises sobre legislação trabalhista, sindical, cível e do transporte de cargas, com jurisprudência e orientação prática para empresas.'),
    'eventos.html': ('Eventos, palestras e treinamentos', 'Palestras, treinamentos e participação do escritório em entidades do setor, como o SETCEMG, na defesa das empresas de transporte e outros segmentos.'),
    'contato.html': ('Contato e endereço do escritório', 'Fale com o Paulo Teodoro Advogados Associados: endereço em Belo Horizonte, WhatsApp, redes sociais e e-mail de cada advogado.'),
    'tributario.html': ('Tributário: agora é o PJR Consultoria Tributária', 'A atuação tributária do grupo Paulo Teodoro é conduzida pelo PJR Consultoria Tributária, especializado em reforma tributária e riscos fiscais.'),
    'escritorio.html': ('O escritório', 'Escritório de abrangência nacional, fundado em 2003 em Belo Horizonte, com atuação em diversos setores e raízes no transporte rodoviário de cargas.'),
    'historia.html': ('Nossa história desde 2003', 'Paulo Teodoro e Jeferson Costa fundaram o escritório em 2003, em Belo Horizonte. Conheça a trajetória e os princípios que guiam o trabalho.'),
    'diferenciais.html': ('Por que somos diferentes', 'Diversidade, criatividade e profissionalismo: conheça a missão, a visão, os valores e a estrutura de apoio ao cliente do escritório.'),
    'compliance.html': ('Compliance e código de conduta', 'O escritório segue padrões de integridade e respeito em todas as suas relações. Conheça o compromisso e o canal para sugestões e denúncias.'),
    'trabalhe-conosco.html': ('Trabalhe conosco: advogados e estagiários', 'O Paulo Teodoro Advogados oferece oportunidades de carreira para advogados e estagiários. Saiba como se candidatar.'),
}

OG_DEFAULT = 'img/og-default.jpg'


def og_image(path):
    if path.startswith('setores/'):
        return f'img/og-{path.split("/")[1][:-5]}.jpg'
    if path.startswith('areas'):
        return 'img/og-areas.jpg'
    if path in ('escritorio.html', 'historia.html', 'diferenciais.html', 'compliance.html', 'trabalhe-conosco.html', 'advogados.html', 'contato.html'):
        return 'img/og-escritorio.jpg'
    return OG_DEFAULT


def canonical(path):
    return BASE if path == 'index.html' else BASE + path


def org_schema():
    return {'@context': 'https://schema.org', '@type': ['LegalService', 'Organization'], '@id': ORG_ID, 'name': 'Paulo Teodoro Advogados Associados',
            'alternateName': 'Paulo Teodoro Advogados', 'url': BASE, 'logo': BASE + 'img/logo-pt-512.png', 'image': BASE + OG_DEFAULT,
            'description': 'Escritório de advocacia em Belo Horizonte com atuação trabalhista, sindical, cível e societária para empresas e entidades de classe, com raízes no transporte rodoviário de cargas.',
            'foundingDate': '2003', 'telephone': '+55 31 99217-2016', 'areaServed': {'@type': 'Country', 'name': 'Brasil'}, 'priceRange': '$$',
            'address': {'@type': 'PostalAddress', 'streetAddress': 'Avenida Antônio Abrahão Caram, 728', 'addressLocality': 'Belo Horizonte', 'addressRegion': 'MG', 'postalCode': '31275-000', 'addressCountry': 'BR'},
            'knowsAbout': ['Direito do trabalho', 'Direito sindical', 'Direito cível', 'Direito societário', 'Recuperação judicial', 'Transporte rodoviário de cargas'],
            'sameAs': SOCIAL, 'inLanguage': 'pt-BR'}


def breadcrumb(path, names):
    """names: lista de (nome, caminho) do segundo nível em diante; o primeiro é sempre Início."""
    items = [('Início', 'index.html')] + names
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': canonical(p)} for i, (n, p) in enumerate(items)]}


def head(path, title, desc, meta=None):
    """Devolve (título, descrição, bloco de <meta>/<link>/<script> do <head>)."""
    meta = meta or {}
    if path in PAGE_META:
        t0, d0 = PAGE_META[path]
        title = t0 if path == 'index.html' else fit_title(t0)
        desc = d0
    else:
        title = fit_title(re.sub(r'\s*·\s*Paulo Teodoro Advogados Associados$', '', title))
        desc = fit_desc(desc)
    title = unique_title(title, path, meta.get('titulo_extra', ''))
    desc = fit_desc(desc)
    url = canonical(path)
    img = BASE + (meta.get('og') or og_image(path))
    typ = 'article' if meta.get('tipo') == 'article' else ('profile' if meta.get('tipo') == 'person' else 'website')
    robots = 'index,follow,max-image-preview:large' if INDEXAR else 'noindex,nofollow'
    h = [f'<meta name="robots" content="{robots}">', f'<link rel="canonical" href="{url}">',
         f'<meta property="og:site_name" content="Paulo Teodoro Advogados Associados"><meta property="og:locale" content="pt_BR"><meta property="og:type" content="{typ}">',
         f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">',
         f'<meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
         f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{img}">']
    if typ == 'article':
        meta['publicado'] = meta['publicado'] + '-03:00' if len(meta['publicado']) == 19 else meta['publicado']
        meta['modificado'] = meta['modificado'] + '-03:00' if len(meta['modificado']) == 19 else meta['modificado']
        h.append(f'<meta property="article:published_time" content="{meta["publicado"]}"><meta property="article:modified_time" content="{meta["modificado"]}"><meta property="article:section" content="{esc(meta.get("secao", ""))}">')
    schemas = []
    if path == 'index.html':
        schemas.append(org_schema())
        schemas.append({'@context': 'https://schema.org', '@type': 'WebSite', '@id': BASE + '#site', 'url': BASE, 'name': 'Paulo Teodoro Advogados Associados', 'inLanguage': 'pt-BR', 'publisher': {'@id': ORG_ID}})
    else:
        crumbs_ = meta.get('crumbs')
        if not crumbs_:
            nome = (PAGE_META.get(path, (title,))[0]).replace(SUFFIX, '')
            sec = {'areas/': ('Áreas do direito', 'areas.html'), 'setores/': ('Setores', 'setores.html')}
            pre = next((k for k in sec if path.startswith(k)), None)
            crumbs_ = ([sec[pre], (nome, path)] if pre else [(nome, path)])
        schemas.append(breadcrumb(path, crumbs_))
    if typ == 'article':
        autor = ({'@type': 'Person', 'name': meta['autor_nome'], 'url': BASE + meta['autor_url']} if meta.get('autor_url')
                 else {'@type': 'Organization', 'name': 'Paulo Teodoro Advogados Associados', '@id': ORG_ID})
        schemas.append({'@context': 'https://schema.org', '@type': 'Article', 'headline': meta['headline'][:110], 'description': desc, 'inLanguage': 'pt-BR',
                        'datePublished': meta['publicado'], 'dateModified': meta['modificado'], 'articleSection': meta.get('secao', ''),
                        'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'image': [img], 'author': autor,
                        'publisher': {'@type': 'Organization', 'name': 'Paulo Teodoro Advogados Associados', '@id': ORG_ID, 'logo': {'@type': 'ImageObject', 'url': BASE + 'img/logo-pt-512.png'}}})
    if typ == 'profile':
        p = {'@context': 'https://schema.org', '@type': 'Person', 'name': meta['nome'], 'jobTitle': meta['cargo'], 'url': url, 'inLanguage': 'pt-BR',
             'worksFor': {'@type': 'LegalService', 'name': 'Paulo Teodoro Advogados Associados', '@id': ORG_ID}}
        if meta.get('foto'):
            p['image'] = BASE + meta['foto']
        if meta.get('email'):
            p['email'] = meta['email']
        schemas.append(p)
    for s in schemas:
        h.append('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False, separators=(',', ':')) + '</script>')
    PAGES.append((path, (meta.get('modificado') or HOJE)[:10]))
    return title, desc, '\n'.join(h)


def write_sitemap_robots():
    urls = ''.join(f'<url><loc>{canonical(p)}</loc><lastmod>{lm}</lastmod></url>' for p, lm in sorted(PAGES))
    open('sitemap.xml', 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    rb = f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n' if INDEXAR else 'User-agent: *\nDisallow: /\n'
    open('robots.txt', 'w', encoding='utf-8').write(rb)
    return len(PAGES)
