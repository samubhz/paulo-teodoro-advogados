# Paulo Teodoro Advogados Associados — protótipo do novo site

Protótipo estático (HTML/CSS) do novo site do escritório, com o conteúdo do site atual
(artigos, eventos, advogados, áreas e setores) e a nova identidade.

- **Status:** protótipo para aprovação dos sócios. Está marcado como `noindex` (não aparece em buscadores).
- **Regenerar as páginas:** `python3 build_site.py` (usa `dados/`, `img/` e `icons.py`).
- **Estrutura e decisões:** veja `ESTRUTURA_SITE_PT.md`.
- **Imagens de setores e ambientes:** ilustrativas, geradas por IA.
- Para publicar de verdade: remova `noindex` (em `build_site.py`, função `layout`) e o `robots.txt`.
