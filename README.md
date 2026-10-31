# Paulo Teodoro Advogados Associados — protótipo do novo site

Protótipo estático (HTML/CSS) do novo site do escritório, com o conteúdo do site atual
(artigos, eventos, advogados, áreas e setores) e a nova identidade.

- **Status:** protótipo para aprovação dos sócios. Está marcado como `noindex` (não aparece em buscadores).
- **Regenerar as páginas:** `python3 build_site.py` (usa `dados/`, `img/` e `icons.py`).
- **Estrutura e decisões:** veja `ESTRUTURA_SITE_PT.md`.
- **Imagens de setores e ambientes:** ilustrativas, geradas por IA.
- **SEO:** títulos, descrições, canonical, Open Graph, JSON-LD e sitemap são gerados por `seo.py`. Para publicar de verdade: em `seo.py`, troque `BASE` pelo domínio definitivo e `INDEXAR = True`, e rode `python3 build_site.py`.
- **Autores dos artigos:** `dados/autores.json`.
