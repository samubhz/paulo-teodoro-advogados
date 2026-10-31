"""Conjunto de ícones de linha (grade 48x48) para o site do Paulo Teodoro.
Traço arredondado, desenhado para ser usado em dourado. Uso: icon('scale') -> <svg>…</svg>
"""
I = {
    # áreas do direito
    'id': '<rect x="6" y="11" width="36" height="26" rx="3.5"/><circle cx="17" cy="21" r="4"/><path d="M10 32c1.2-3.6 4-5 7-5s5.8 1.4 7 5"/><path d="M29 20h8M29 26h8M29 32h5"/>',
    'users': '<circle cx="18" cy="17" r="5.5"/><path d="M7 38c0-7.5 5-12 11-12s11 4.5 11 12"/><circle cx="33" cy="19" r="4.5"/><path d="M31 27c6.5-1.2 11 3 11 11"/>',
    'scale': '<path d="M24 7v33M15 40h18"/><circle cx="24" cy="7" r="2"/><path d="M10 14h28"/><path d="M10 14 4.5 27M10 14l5.5 13M38 14l-5.5 13M38 14l5.5 13"/><path d="M4.5 27h11a5.5 5.5 0 0 1-11 0zM32.5 27h11a5.5 5.5 0 0 1-11 0z"/>',
    'briefcase': '<rect x="6" y="14" width="36" height="25" rx="3.5"/><path d="M17 14v-3.5A2.5 2.5 0 0 1 19.5 8h9A2.5 2.5 0 0 1 31 10.5V14"/><path d="M6 25h36"/><path d="M21 25v4.5h6V25"/>',
    'trend': '<path d="M6 41h36"/><path d="M8 33l10-10 7 6 14-15"/><path d="M30 14h9v9"/>',
    # ações
    'shield': '<path d="M24 6l14 5v11c0 9.5-6.5 15.5-14 20-7.5-4.5-14-10.5-14-20V11z"/><path d="M17 24l5 5 9-10"/>',
    'compass': '<circle cx="24" cy="24" r="17"/><path d="M31 17l-4.5 10-10 4.5L21 21.5z"/><circle cx="24" cy="24" r="1.4"/>',
    'exchange': '<path d="M8 17h30M31 10l7 7-7 7"/><path d="M40 32H10M17 25l-7 7 7 7"/>',
    'document': '<path d="M12 5h17l9 9v29H12z"/><path d="M29 5v9h9"/><path d="M18 25h14M18 31h14M18 37h8"/>',
    'org': '<rect x="16" y="6" width="16" height="9" rx="2"/><rect x="5" y="33" width="14" height="9" rx="2"/><rect x="29" y="33" width="14" height="9" rx="2"/><path d="M24 15v9M12 33v-9h24v9"/>',
    'key': '<circle cx="16" cy="24" r="8"/><path d="M24 24h18M35 24v7M42 24v5"/>',
    'gavel': '<path d="M9 40h18"/><path d="M14 22l11 11M20 12l16 16M16 16l8-8 16 16-8 8z"/>',
    # estrutura de apoio / contato
    'monitor': '<rect x="5" y="8" width="38" height="26" rx="3"/><path d="M17 41h14M24 34v7"/><path d="M11 27l7-8 6 5 9-11"/>',
    'chart': '<path d="M6 42h36"/><rect x="9" y="25" width="6" height="14" rx="1"/><rect x="21" y="14" width="6" height="25" rx="1"/><rect x="33" y="20" width="6" height="19" rx="1"/>',
    'video': '<rect x="5" y="12" width="28" height="24" rx="3.5"/><path d="M33 21l10-6v18l-10-6z"/>',
    'mail': '<rect x="5" y="10" width="38" height="28" rx="3.5"/><path d="M7 14l17 13 17-13"/>',
    'book': '<path d="M24 14c-4-4-10-5-17-5v29c7 0 13 1 17 5 4-4 10-5 17-5V9c-7 0-13 1-17 5z"/><path d="M24 14v29"/>',
    'phone': '<path d="M15 6h6l3 9-4 3a24 24 0 0 0 10 10l3-4 9 3v6a4 4 0 0 1-4 4C22 37 11 26 11 10a4 4 0 0 1 4-4z"/>',
    'pin': '<path d="M24 43s14-12 14-23a14 14 0 0 0-28 0c0 11 14 23 14 23z"/><circle cx="24" cy="20" r="5"/>',
    'clock': '<circle cx="24" cy="24" r="17"/><path d="M24 13v11l7 5"/>',
    'check': '<circle cx="24" cy="24" r="17"/><path d="M16 24.5l6 6 11-12"/>',
    'doc-search': '<path d="M11 5h17l8 8v14"/><path d="M28 5v8h8"/><path d="M11 5v38h14"/><circle cx="33" cy="35" r="6"/><path d="M37.5 39.5L43 45"/>',
    # setores
    'truck': '<path d="M4 13h25v22H4z"/><path d="M29 20h9l6 8v7H29z"/><circle cx="13" cy="37" r="4"/><circle cx="36" cy="37" r="4"/>',
    'crane': '<path d="M8 42V20h16v22"/><path d="M13 26h6M13 32h6M13 38h6"/><path d="M33 42V8M26 8h16M40 8v9M33 8l-7 5"/><path d="M6 42h38"/>',
    'cross': '<rect x="7" y="7" width="34" height="34" rx="7"/><path d="M24 15v18M15 24h18"/>',
    'store': '<path d="M7 19l3-10h28l3 10"/><path d="M7 19c0 3 2.5 4.5 5.5 4.5S18 22 18 19c0 3 2.5 4.5 6 4.5s6-1.5 6-4.5c0 3 2.5 4.5 5.5 4.5S41 22 41 19"/><path d="M10 24v17h28V24"/><path d="M20 41V31h8v10"/>',
    'cap': '<path d="M24 9L43 19 24 29 5 19z"/><path d="M13 24v9c0 3 5 6.5 11 6.5S35 36 35 33v-9"/><path d="M43 19v12"/>',
    'factory': '<path d="M5 41V24l10 6v-6l10 6v-6l10 6V8h8v33z"/><path d="M18 41v-5M26 41v-5M34 41v-5"/>',
}


def icon(name, cls='ic', size=None):
    sz = f' width="{size}" height="{size}"' if size else ''
    return (f'<svg class="{cls}" viewBox="0 0 48 48"{sz} fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{I[name]}</svg>')


if __name__ == '__main__':
    import os
    cells = ''.join(f'<div style="text-align:center;font:11px sans-serif;color:#555"><div style="width:84px;height:84px;margin:0 auto 6px;border-radius:50%;background:#F3EAD3;border:1.5px solid #B8893A;color:#7A5A1C;display:grid;place-items:center">{icon(k, size=46)}</div>{k}</div>' for k in I)
    open('/private/tmp/claude-501/-Users-samuelaraujo-Projetos-NANAU/38d79620-9775-434d-bc48-23ed8b149d26/scratchpad/icons.html', 'w').write(f'<!doctype html><body style="margin:0;padding:24px;background:#F7F5EF;display:grid;grid-template-columns:repeat(8,1fr);gap:18px;width:1180px">{cells}</body>')
    print(len(I), 'ícones')
