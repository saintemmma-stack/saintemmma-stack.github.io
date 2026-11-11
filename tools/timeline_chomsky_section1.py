# Generates the inline SVG timeline for section I (1944-1978).
import html
X0, X1, Y0, Y1 = 40, 720, 1944, 1978
def x(y): return X0 + (y - Y0) * (X1 - X0) / (Y1 - Y0)
AX = 170
out = []
W, H = 760, 312
out.append(f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="tl-title tl-desc" xmlns="http://www.w3.org/2000/svg">')
out.append('<title id="tl-title">Timeline, 1944 to 1977</title>')
out.append('<desc id="tl-desc">From the Liberation to the new philosophers: the fellow-travelling years 1944 to 1956, the shocks of 1956, and the Maoist turn of 1968 to 1976.</desc>')
# bands
for a, b, label in [(1944.6, 1956.85, "fellow-travelling years"), (1968.4, 1976.8, "Maoist turn")]:
    out.append(f'<rect x="{x(a):.1f}" y="{AX-11}" width="{x(b)-x(a):.1f}" height="22" rx="4" class="pencil" opacity="0.13"/>')
    out.append(f'<text x="{x(a)+8:.1f}" y="{AX-17}" font-size="10" class="pencil" font-style="italic">{label}</text>')
# axis
out.append(f'<line x1="{X0-10}" y1="{AX}" x2="{X1+10}" y2="{AX}" class="stroke-ink" stroke-width="1.2"/>')
for yr in range(1945, 1980, 5):
    out.append(f'<line x1="{x(yr):.1f}" y1="{AX-4}" x2="{x(yr):.1f}" y2="{AX+4}" class="stroke-ink" stroke-width="1"/>')
    out.append(f'<text x="{x(yr):.1f}" y="{AX+21}" font-size="9" text-anchor="middle" class="graphite">{yr}</text>')
# events: (year, side, level, anchor, lines, here)
E = [
 (1944.65, "up", 1, "start", ["Aug 1944", "Liberation of Paris"], True),
 (1952.6, "up", 2, "middle", ["1952", "Sartre’s “Les Communistes", "et la paix”; break with Camus"], True),
 (1956.15, "up", 1, "middle", ["25 Feb 1956", "Khrushchev’s Secret Speech"], True),
 (1968.4, "up", 1, "middle", ["May 1968"], True),
 (1974.3, "up", 2, "middle", ["Apr–May 1974", "Tel Quel in China;", "Gulag published in French"], True),
 (1977.2, "up", 1, "end", ["1977", "the “new philosophers”", "(see §V)"], False),
 (1949.2, "down", 1, "middle", ["Mar 1949", "Socialisme ou Barbarie", "begins publishing"], True),
 (1955.5, "down", 2, "end", ["1955", "Aron, L’Opium", "des intellectuels"], True),
 (1956.84, "down", 1, "start", ["4 Nov 1956", "Soviet tanks crush", "the Budapest uprising"], True),
 (1971.5, "down", 1, "end", ["1971", "Tel Quel breaks with", "the PCF, turns Maoist"], True),
 (1976.8, "down", 2, "end", ["Autumn 1976", "Tel Quel drops Maoism"], True),
]
for yr, side, lvl, anchor, lines, here in E:
    cx = x(yr)
    cls = "pencil" if here else "graphite"
    scls = "stroke-pencil" if here else "stroke-ink"
    if side == "up":
        first = 112 if lvl == 1 else 46
        first = first - 16 * (len(lines) - 2) if lvl == 1 and len(lines) > 2 else first
        top_of_line = first + 16 * (len(lines) - 1) + 8
        out.append(f'<line x1="{cx:.1f}" y1="{AX-6}" x2="{cx:.1f}" y2="{top_of_line}" class="{scls}" stroke-width="1" stroke-dasharray="2 2"/>')
    else:
        first = 210 if lvl == 1 else 266
        out.append(f'<line x1="{cx:.1f}" y1="{AX+6}" x2="{cx:.1f}" y2="{first-12}" class="{scls}" stroke-width="1" stroke-dasharray="2 2"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{AX}" r="4.2" class="{cls}"/>')
    for i, t in enumerate(lines):
        w = ' font-weight="600"' if i == 0 else ''
        c = cls if i == 0 else "ink"
        out.append(f'<text x="{cx:.1f}" y="{first + 16*i}" font-size="11" text-anchor="{anchor}" class="{c}"{w}>{html.escape(t, quote=False)}</text>')
out.append('</svg>')
print("\n".join(out))
