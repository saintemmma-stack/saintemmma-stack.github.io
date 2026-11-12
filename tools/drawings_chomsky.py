# Generates the drawings for sections II-VIII of the Chomsky edition, in English and French.
# Usage: python3 tools/drawings_chomsky.py
# Writes one include file per drawing and language:
#   works/chomsky-french-intellectuals/_figures/<name>.md
#   fr/works/chomsky-french-intellectuals/_figures/<name>.md
# Each file holds a <figure class="sr-drawing"> with an inline SVG that uses the
# site's colour classes (ink, graphite, pencil, chart-bar, stroke-*) so it follows
# light and dark mode. Edit the data below, then rerun.
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = {"en": os.path.join(ROOT, "works/chomsky-french-intellectuals/_figures"),
       "fr": os.path.join(ROOT, "fr/works/chomsky-french-intellectuals/_figures")}

def esc(s):
    return html.escape(s, quote=False)

def figure(name, lang, svg, caption):
    os.makedirs(OUT[lang], exist_ok=True)
    body = ('<figure class="sr-drawing">\n<div class="sr-scroll">\n' + svg +
            '\n</div>\n<figcaption>' + caption + '</figcaption>\n</figure>\n')
    with open(os.path.join(OUT[lang], name + ".md"), "w") as f:
        f.write(body)

def svg_open(w, h, uid, title, desc):
    return [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="{uid}-t {uid}-d" xmlns="http://www.w3.org/2000/svg">',
            f'<title id="{uid}-t">{esc(title)}</title>', f'<desc id="{uid}-d">{esc(desc)}</desc>']

# ---------------------------------------------------------------- timelines
def timeline(uid, title, desc, y0, y1, ticks, events, bands=(), w=760, h=300, ax=150,
             x0=40, x1=720, segments=None, notes=()):
    """events: (year, label_y, anchor, [lines], here). label_y is the baseline of the
    first line; labels above the axis have label_y < ax, below have label_y > ax.
    bands: (from, to, label, label_side) drawn on the axis.
    segments: optional list of (ya, yb, xa, xb) for a broken axis."""
    if segments is None:
        segments = [(y0, y1, x0, x1)]
    def x(y):
        for ya, yb, xa, xb in segments:
            if ya <= y <= yb:
                return xa + (y - ya) * (xb - xa) / (yb - ya)
        raise ValueError(y)
    o = svg_open(w, h, uid, title, desc)
    for a, b, label, side in bands:
        o.append(f'<rect x="{x(a):.1f}" y="{ax-11}" width="{max(x(b)-x(a), 6):.1f}" height="22" rx="4" class="pencil" opacity="0.13"/>')
        ly = ax - 17 if side == "up" else ax + 33
        o.append(f'<text x="{x(a)+4:.1f}" y="{ly}" font-size="10" class="pencil" font-style="italic">{esc(label)}</text>')
    for ya, yb, xa, xb in segments:
        o.append(f'<line x1="{xa-8}" y1="{ax}" x2="{xb+8}" y2="{ax}" class="stroke-ink" stroke-width="1.2"/>')
    if len(segments) > 1:
        for (_, _, _, xb), (_, _, xa2, _) in zip(segments, segments[1:]):
            mid = (xb + xa2) / 2
            for dx in (-4, 4):
                o.append(f'<line x1="{mid+dx-4:.1f}" y1="{ax+7}" x2="{mid+dx+4:.1f}" y2="{ax-7}" class="stroke-ink" stroke-width="1.2"/>')
    for t in ticks:
        o.append(f'<line x1="{x(t):.1f}" y1="{ax-4}" x2="{x(t):.1f}" y2="{ax+4}" class="stroke-ink" stroke-width="1"/>')
        o.append(f'<text x="{x(t):.1f}" y="{ax+21}" font-size="9" text-anchor="middle" class="graphite">{t}</text>')
    for nx, ny, text in notes:
        o.append(f'<text x="{nx}" y="{ny}" font-size="10" text-anchor="middle" class="pencil" font-style="italic">{esc(text)}</text>')
    for yr, ly, anchor, lines, here in events:
        cx = x(yr)
        fill = "pencil" if here else "graphite"
        stroke = "stroke-pencil" if here else "stroke-ink"
        if ly < ax:   # label above
            end = ly + 16 * (len(lines) - 1) + 8
            o.append(f'<line x1="{cx:.1f}" y1="{ax-6}" x2="{cx:.1f}" y2="{end}" class="{stroke}" stroke-width="1" stroke-dasharray="2 2"/>')
        else:
            o.append(f'<line x1="{cx:.1f}" y1="{ax+6}" x2="{cx:.1f}" y2="{ly-12}" class="{stroke}" stroke-width="1" stroke-dasharray="2 2"/>')
        o.append(f'<circle cx="{cx:.1f}" cy="{ax}" r="4.2" class="{fill}"/>')
        for i, line in enumerate(lines):
            cls = fill if i == 0 else "ink"
            wt = ' font-weight="600"' if i == 0 else ""
            o.append(f'<text x="{cx:.1f}" y="{ly + 16*i}" font-size="11" text-anchor="{anchor}" class="{cls}"{wt}>{esc(line)}</text>')
    o.append("</svg>")
    return "\n".join(o)

# ---------------------------------------------------------------- §II bar chart
TRANSL = [(2009, 14.3), (2011, 15.9), (2012, 17.3), (2013, 17.5), (2014, 17.4),
          (2017, 19.1), (2018, 18.5), (2019, 18.1)]

def translations(lang):
    fr = lang == "fr"
    W, H = 760, 270
    left, right, top, base = 70, 730, 40, 220
    ymax = 20
    def X(year): return left + (year - 2008.5) * (right - left) / 11
    def Y(v): return base - v * (base - top) / ymax
    title = ("Part des traductions dans les nouveautés publiées en France, 2009-2019" if fr
             else "Translations as a share of new titles published in France, 2009 to 2019")
    desc = ("Diagramme en barres. La part des traductions passe de 14,3 % en 2009 à 19,1 % en 2017, puis 18,1 % en 2019, "
            "soit environ un livre nouveau sur six." if fr else
            "Bar chart. The share of translations rises from 14.3 percent in 2009 to 19.1 percent in 2017, then 18.1 percent in 2019, "
            "or roughly one new book in six.")
    o = svg_open(W, H, "tr", title, desc)
    for g in (5, 10, 15, 20):
        o.append(f'<line x1="{left}" y1="{Y(g):.1f}" x2="{right}" y2="{Y(g):.1f}" class="stroke-rule" stroke-width="1"/>')
        lab = f"{g} %" if fr else f"{g}%"
        o.append(f'<text x="{left-8}" y="{Y(g)+3:.1f}" font-size="10" text-anchor="end" class="graphite">{lab}</text>')
    o.append(f'<line x1="{left}" y1="{base}" x2="{right}" y2="{base}" class="stroke-ink" stroke-width="1.2"/>')
    bw = 34
    for year, v in TRANSL:
        cx = X(year)
        top_y = Y(v)
        hgt = base - top_y
        r = 4
        # bar with rounded top corners, square at the baseline
        d = (f"M{cx-bw/2:.1f},{base} V{top_y+r:.1f} Q{cx-bw/2:.1f},{top_y:.1f} {cx-bw/2+r:.1f},{top_y:.1f} "
             f"H{cx+bw/2-r:.1f} Q{cx+bw/2:.1f},{top_y:.1f} {cx+bw/2:.1f},{top_y+r:.1f} V{base} Z")
        val = (f"{v:.1f}".replace(".", ",") + " %") if fr else f"{v:.1f}%"
        o.append(f'<path d="{d}" class="chart-bar"><title>{year} : {val}</title></path>' if fr else
                 f'<path d="{d}" class="chart-bar"><title>{year}: {val}</title></path>')
        o.append(f'<text x="{cx:.1f}" y="{base+16}" font-size="10" text-anchor="middle" class="graphite">{year}</text>')
        if year in (2009, 2017, 2019):
            o.append(f'<text x="{cx:.1f}" y="{top_y-6:.1f}" font-size="11" text-anchor="middle" class="ink" font-weight="600">{val}</text>')
    o.append("</svg>")
    cap = ("Environ un livre nouveau sur six publié en France est une traduction. Source : enquêtes annuelles de "
           "<em>Livres Hebdo</em>/Electre (nouveautés et nouvelles éditions, tous genres). Les années sans barre sont celles "
           "dont nous n’avons pas consulté l’enquête. Survolez une barre pour lire sa valeur." if fr else
           "Roughly one new book in six published in France is a translation. Source: annual surveys by "
           "<em>Livres Hebdo</em>/Electre (new titles and new editions, all genres). Years without a bar are years whose "
           "survey we have not consulted. Hover over a bar to read its value.")
    figure("translations", lang, "\n".join(o), cap)

# ---------------------------------------------------------------- §III
def positivism(lang):
    fr = lang == "fr"
    segs = [(1925, 1940, 40, 400), (1975, 1990, 460, 720)]
    E = [
        (1929, 112, "middle", ["1929", "Manifeste du cercle de Vienne" if fr else "Vienna Circle manifesto"], True),
        (1933.5, 196, "middle", ["1933-1934", "Carnap traduit en français" if fr else "Carnap in French"], True),
        (1935.7, 40, "middle", ["sept. 1935" if fr else "Sept 1935", "Congrès pour l’unité de la" if fr else "Unity of Science congress", "science, Sorbonne" if fr else "at the Sorbonne"], True),
        (1937.6, 240, "end", ["1937", "Congrès Descartes, Paris"], True),
        (1938.2, 112, "start", ["1938", "Anschluss : le cercle" if fr else "Anschluss: the Circle", "se disperse" if fr else "disperses"], False),
        (1978, 40, "middle", ["1978", "doctorat de Pierre Jacob" if fr else "Pierre Jacob’s PhD", "à Harvard" if fr else "at Harvard"], True),
        (1980.3, 196, "middle", ["1980", "Jacob, L’Empirisme logique ;" if fr else "Jacob, L’Empirisme logique;", "De Vienne à Cambridge"], True),
        (1985, 112, "middle", ["1985", "le manifeste en français" if fr else "the manifesto in French", "(éd. Soulez)" if fr else "(ed. Soulez)"], True),
    ]
    svg = timeline("lp", "Le positivisme logique et la France, 1929-1985" if fr else "Logical positivism and France, 1929 to 1985",
                   ("Chronologie à axe interrompu : le manifeste de 1929, les traductions et congrès parisiens des années 1930, une interruption de 1940 à 1975, puis les livres de Pierre Jacob en 1980 et l’édition française du manifeste en 1985." if fr else
                    "Timeline with a broken axis: the 1929 manifesto, the Paris translations and congresses of the 1930s, a gap from 1940 to 1975, then Pierre Jacob’s books of 1980 and the French edition of the manifesto in 1985."),
                   1925, 1990, [1925, 1930, 1935, 1940, 1975, 1980, 1985, 1990], E, h=290, ax=150, segments=segs,
                   notes=[(430, 180, "1940-1975 :" if fr else "1940–1975:"), (430, 193, "presque rien" if fr else "almost nothing"), (430, 206, "en français" if fr else "in French")])
    cap = ("Le mouvement est passé par Paris dans les années 1930, puis a presque disparu de la scène française jusqu’en 1980. L’axe est interrompu entre 1940 et 1975. Bleu : événements discutés ici ; gris : contexte." if fr else
           "The movement passed through Paris in the 1930s, then all but vanished from the French scene until 1980. The axis is broken between 1940 and 1975. Blue marks the events discussed here; grey marks context.")
    figure("positivism", lang, svg, cap)

# ---------------------------------------------------------------- §IV
def attic(lang):
    fr = lang == "fr"
    W, H = 760, 320
    def x(y): return 40 + (y - 1935) * 680 / 50
    o = svg_open(W, H, "at", "Deux lieux de la biologie française, 1938-1980" if fr else "Two places in French biology, 1938 to 1980",
                 ("Deux lignes de temps parallèles : en haut, le « grenier » d’André Lwoff à l’Institut Pasteur, de sa création en 1938 au prix Nobel de 1965 ; en bas, la tradition néo-lamarckienne de la Sorbonne, avec L’Évolution du vivant de Grassé en 1973 et l’article de Boesiger." if fr else
                  "Two parallel timelines: above, André Lwoff’s ‘attic’ at the Pasteur Institute, from its founding in 1938 to the 1965 Nobel Prize; below, the neo-Lamarckian tradition at the Sorbonne, with Grassé’s L’Évolution du vivant in 1973 and Boesiger’s paper."))
    L1, L2 = 110, 245
    o.append(f'<text x="30" y="22" font-size="11" class="pencil" font-weight="600">{esc("Institut Pasteur : le « grenier » de Lwoff" if fr else "Pasteur Institute: Lwoff’s ‘attic’")}</text>')
    o.append(f'<text x="30" y="200" font-size="11" class="graphite" font-weight="600">{esc("Sorbonne : la chaire d’évolution, néo-lamarckienne" if fr else "Sorbonne: the neo-Lamarckian chair of evolution")}</text>')
    for t in range(1940, 1990, 10):
        o.append(f'<line x1="{x(t):.1f}" y1="40" x2="{x(t):.1f}" y2="{H-24}" class="stroke-rule" stroke-width="1" stroke-dasharray="1 3"/>')
        o.append(f'<text x="{x(t):.1f}" y="{H-8}" font-size="9" text-anchor="middle" class="graphite">{t}</text>')
    for ly in (L1, L2):
        o.append(f'<line x1="30" y1="{ly}" x2="730" y2="{ly}" class="stroke-ink" stroke-width="1.2"/>')
    def mark(yr, lane, above, anchor, lines, here):
        cx = x(yr)
        fill = "pencil" if here else "graphite"
        o.append(f'<circle cx="{cx:.1f}" cy="{lane}" r="4.2" class="{fill}"/>')
        y0 = lane - 48 if above else lane + 22
        if above:
            o.append(f'<line x1="{cx:.1f}" y1="{lane-6}" x2="{cx:.1f}" y2="{lane-26}" class="{"stroke-pencil" if here else "stroke-ink"}" stroke-width="1" stroke-dasharray="2 2"/>')
        dx = -6 if anchor == "end" else (6 if anchor == "start" else 0)
        for i, line in enumerate(lines):
            cls = fill if i == 0 else "ink"
            wt = ' font-weight="600"' if i == 0 else ""
            o.append(f'<text x="{cx+dx:.1f}" y="{y0+15*i}" font-size="11" text-anchor="{anchor}" class="{cls}"{wt}>{esc(line)}</text>')
    mark(1938, L1, False, "start", ["1938", "service créé" if fr else "department founded"], True)
    mark(1945.9, L1, True, "middle", ["fin 1945" if fr else "late 1945", "Monod arrive" if fr else "Monod joins"], True)
    mark(1950.8, L1, False, "middle", ["1950", "Jacob arrive" if fr else "Jacob joins"], True)
    mark(1961, L1, True, "middle", ["1960-1961", "ARN messager, opéron" if fr else "messenger RNA, operon"], True)
    mark(1965.8, L1, False, "middle", ["1965", "prix Nobel" if fr else "Nobel Prize"], True)
    mark(1970.8, L1, True, "start", ["1970", "Le Hasard et la Nécessité"], True)
    mark(1973, L2, False, "end", ["1973", "Grassé, L’Évolution du vivant"], False)
    mark(1974, L2, False, "start", ["1974", "Boesiger : la France," if fr else "Boesiger: France as a", "« fossile vivant »" if fr else "“living fossil”"], False)
    o.append("</svg>")
    cap = ("Deux mondes contemporains. En haut, l’atelier de Lwoff sous les combles de l’Institut Pasteur ; en bas, la chaire d’évolution de la Sorbonne, tenue par des néo-lamarckiens jusque dans les années 1960." if fr else
           "Two worlds at the same time. Above, Lwoff’s workshop under the roof of the Pasteur Institute; below, the Sorbonne’s chair of evolution, held by neo-Lamarckians into the 1960s.")
    figure("attic", lang, "\n".join(o), cap)

# ---------------------------------------------------------------- §V
def gulag(lang):
    fr = lang == "fr"
    E = [
        (1939.1, 50, "start", ["févr. 1939" if fr else "Feb 1939", "Chomsky, 10 ans, écrit" if fr else "Chomsky, aged 10, writes", "sur la chute de Barcelone" if fr else "on the fall of Barcelona"], False),
        (1949.2, 150, "middle", ["janv.-avr. 1949" if fr else "Jan–Apr 1949", "procès Kravchenko, Paris" if fr else "Kravchenko trial, Paris"], True),
        (1949.9, 236, "middle", ["nov. 1949" if fr else "Nov 1949", "appel de David Rousset" if fr else "David Rousset’s appeal", "sur les camps soviétiques" if fr else "on the Soviet camps"], True),
        (1962.9, 100, "middle", ["1962", "Une journée d’Ivan Denissovitch" if fr else "One Day in the Life of Ivan Denisovich"], True),
        (1973.99, 50, "end", ["28 déc. 1973" if fr else "28 Dec 1973", "L’Archipel du Goulag en russe," if fr else "The Gulag Archipelago in Russian,", "YMCA-Press, Paris"], True),
        (1974.4, 236, "end", ["1974", "traduction française ;" if fr else "French translation;", "Soljenitsyne expulsé d’URSS" if fr else "Solzhenitsyn expelled from the USSR"], True),
        (1975.5, 100, "start", ["1975", "Glucksmann, La Cuisinière…"], True),
        (1977.4, 236, "start", ["27 mai 1977" if fr else "27 May 1977", "nouveaux philosophes" if fr else "new philosophers", "à Apostrophes" if fr else "on Apostrophes"], True),
        (1980, 150, "start", ["1979-1980", "affaire Faurisson" if fr else "Faurisson affair"], False),
    ]
    svg = timeline("gu", "Ce que l’on pouvait savoir, et quand, 1936-1980" if fr else "What could be known, and when, 1936 to 1980",
                   ("Chronologie : les procès de Moscou, l’enfance de Chomsky, le procès Kravchenko et l’appel de Rousset en 1949, Soljenitsyne en 1962 et 1973-1974, puis les nouveaux philosophes et l’affaire Faurisson." if fr else
                    "Timeline: the Moscow trials, Chomsky’s childhood, the Kravchenko trial and Rousset’s appeal in 1949, Solzhenitsyn in 1962 and 1973 to 1974, then the new philosophers and the Faurisson affair."),
                   1934, 1984, [1935, 1940, 1945, 1950, 1955, 1960, 1965, 1970, 1975, 1980], E,
                   bands=[(1936.6, 1938.2, "procès de Moscou" if fr else "Moscow trials", "down")], h=300, ax=190, x0=40, x1=680)
    cap = ("Les camps soviétiques n’étaient pas un secret en 1974 : ils avaient été plaidés devant un tribunal parisien dès 1949. Bleu : événements français ou parisiens ; gris : repères liés à Chomsky." if fr else
           "The Soviet camps were no secret in 1974: they had been argued over in a Paris courtroom as early as 1949. Blue marks French or Parisian events; grey marks points of reference in Chomsky’s own story.")
    figure("gulag", lang, svg, cap)

# ---------------------------------------------------------------- §VI
def cycles(lang):
    fr = lang == "fr"
    W, H = 760, 280
    def x(y): return 40 + (y - 1870) * 680 / 130
    o = svg_open(W, H, "cy", "Les trois cycles du pouvoir intellectuel selon Régis Debray" if fr else "Régis Debray’s three cycles of intellectual power",
                 ("Trois bandes qui se chevauchent : le cycle universitaire de 1880 à 1930, le cycle éditorial de 1920 à 1960, le cycle médiatique à partir de 1968, avec quelques repères de J’accuse en 1898 à Sur la télévision en 1996." if fr else
                  "Three overlapping bands: the university cycle from 1880 to 1930, the publishing cycle from 1920 to 1960, the media cycle from 1968, with markers from J’accuse in 1898 to On Television in 1996."))
    rows = [(1880, 1930, 40, "cycle universitaire (1880-1930)" if fr else "university cycle (1880–1930)"),
            (1920, 1960, 78, "cycle éditorial (1920-1960)" if fr else "publishing cycle (1920–1960)"),
            (1968, 2000, 116, "cycle médiatique (depuis 1968)" if fr else "media cycle (from 1968)")]
    for a, b, y, label in rows:
        o.append(f'<rect x="{x(a):.1f}" y="{y}" width="{x(b)-x(a):.1f}" height="24" rx="4" class="pencil" opacity="0.16"/>')
        o.append(f'<text x="{x(a)+8:.1f}" y="{y+16}" font-size="11" class="ink">{esc(label)}</text>')
    o.append(f'<rect x="{x(1975.03):.1f}" y="150" width="{x(1990.47)-x(1975.03):.1f}" height="10" rx="3" class="pencil" opacity="0.6"><title>{"Apostrophes, 1975-1990" if fr else "Apostrophes, 1975–1990"}</title></rect>')
    o.append(f'<text x="{x(1975.03)-6:.1f}" y="159" font-size="10" text-anchor="end" class="pencil" font-style="italic">Apostrophes</text>')
    ax = 196
    o.append(f'<line x1="30" y1="{ax}" x2="730" y2="{ax}" class="stroke-ink" stroke-width="1.2"/>')
    for t in range(1880, 2010, 20):
        o.append(f'<line x1="{x(t):.1f}" y1="{ax-4}" x2="{x(t):.1f}" y2="{ax+4}" class="stroke-ink" stroke-width="1"/>')
        o.append(f'<text x="{x(t):.1f}" y="{ax+18}" font-size="9" text-anchor="middle" class="graphite">{t}</text>')
    marks = [(1898.04, "middle", "1898 : J’accuse" if fr else "1898: J’accuse", 230),
             (1980.3, "end", "1980 : obsèques de Sartre" if fr else "1980: Sartre’s funeral", 230),
             (1996.4, "end", "1996 : Sur la télévision" if fr else "1996: On Television", 256)]
    for yr, anchor, label, ly in marks:
        cx = x(yr)
        o.append(f'<circle cx="{cx:.1f}" cy="{ax}" r="4" class="pencil"/>')
        if ly < ax:
            o.append(f'<line x1="{cx:.1f}" y1="{ly+6}" x2="{cx:.1f}" y2="{ax-6}" class="stroke-pencil" stroke-width="1" stroke-dasharray="2 2"/>')
            o.append(f'<text x="{cx:.1f}" y="{ly}" font-size="11" text-anchor="{anchor}" class="pencil" font-weight="600">{esc(label)}</text>')
        else:
            o.append(f'<line x1="{cx:.1f}" y1="{ax+6}" x2="{cx:.1f}" y2="{ly-12}" class="stroke-pencil" stroke-width="1" stroke-dasharray="2 2"/>')
            o.append(f'<text x="{cx + (-4 if anchor == "end" else 4):.1f}" y="{ly}" font-size="11" text-anchor="{anchor}" class="pencil" font-weight="600">{esc(label)}</text>')
    o.append("</svg>")
    cap = ("D’après Régis Debray, <em>Le Pouvoir intellectuel en France</em> (1979) : le centre de gravité passe du professeur à l’éditeur, puis aux médias. La bande foncée marque les quinze années d’<em>Apostrophes</em>." if fr else
           "After Régis Debray, <em>Le Pouvoir intellectuel en France</em> (1979): the centre of gravity moves from the professor to the publisher, then to the media. The dark strip marks the fifteen years of <em>Apostrophes</em>.")
    figure("cycles", lang, "\n".join(o), cap)

# ---------------------------------------------------------------- §VII
def foundations(lang):
    fr = lang == "fr"
    segs = [(1600, 1760, 40, 360), (1920, 2000, 420, 720)]
    E = [
        (1625, 60, "middle", ["1625", "Mersenne, La Vérité", "des sciences"], True),
        (1641, 196, "middle", ["1641", "Descartes, Méditations" if fr else "Descartes, Meditations"], False),
        (1658, 60, "start", ["1658", "Gassendi, Syntagma", "philosophicum"], True),
        (1748, 196, "end", ["1748", "Hume, Enquête" if fr else "Hume, Enquiry"], True),
        (1932, 60, "middle", ["1932", "Neurath : le bateau" if fr else "Neurath’s boat"], True),
        (1951, 196, "middle", ["1951", "Quine, « Deux dogmes »" if fr else "Quine, “Two Dogmas”"], True),
        (1979, 60, "end", ["1979", "Lyotard, La Condition", "postmoderne"], False),
        (1996, 196, "end", ["1996", "affaire Sokal" if fr else "Sokal affair"], False),
    ]
    svg = timeline("fd", "Renoncer aux fondements : deux époques" if fr else "Giving up foundations: two periods",
                   ("Chronologie à axe interrompu : au XVIIe et au XVIIIe siècle, Mersenne, Gassendi et Hume répondent au doute de Descartes sans fondement absolu ; au XXe siècle, Neurath et Quine, puis Lyotard et l’affaire Sokal." if fr else
                    "Timeline with a broken axis: in the seventeenth and eighteenth centuries Mersenne, Gassendi and Hume answer Descartes’s doubt without absolute foundations; in the twentieth, Neurath and Quine, then Lyotard and the Sokal affair."),
                   1600, 2000, [1600, 1650, 1700, 1750, 1920, 1950, 1980, 2000], E, h=250, ax=150, segments=segs)
    cap = ("Le renoncement aux fondements certains n’est pas né à Paris en 1968 : Mersenne et Gassendi le pratiquaient déjà, et les positivistes logiques en avaient fait leur image du bateau. L’axe est interrompu entre 1760 et 1920. Bleu : positions qui renoncent aux fondements sans renoncer à la connaissance." if fr else
           "Giving up certain foundations did not begin in Paris in 1968: Mersenne and Gassendi already practised it, and the logical positivists made it into the image of the boat. The axis is broken between 1760 and 1920. Blue marks positions that give up foundations without giving up knowledge.")
    figure("foundations", lang, svg, cap)

# ---------------------------------------------------------------- §VIII
def travels(lang):
    fr = lang == "fr"
    W, H = 760, 280
    o = svg_open(W, H, "tv", "Comment la théorie française a voyagé" if fr else "How French theory travelled",
                 ("Schéma en cinq étapes : Paris dans les années 1960, le colloque de Johns Hopkins en 1966, les départements de lettres américains, la théorie postcoloniale (Said, Subaltern Studies, Spivak), puis ses critiques de gauche (Ahmad, Chibber)." if fr else
                  "Diagram in five steps: Paris in the 1960s, the Johns Hopkins symposium in 1966, American literature departments, postcolonial theory (Said, Subaltern Studies, Spivak), then its critics on the left (Ahmad, Chibber)."))
    o.append('<defs><marker id="tv-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="pencil"/></marker></defs>')
    boxes = [
        (10, 40, 170, ["Paris, années 1960" if fr else "Paris, 1960s", "le structuralisme et après :" if fr else "structuralism and after:", "Barthes, Derrida, Foucault"], True),
        (200, 40, 165, ["Baltimore, oct. 1966" if fr else "Baltimore, Oct 1966", "colloque de Johns Hopkins" if fr else "Johns Hopkins symposium"], True),
        (385, 40, 170, ["États-Unis, 1970-1980" if fr else "United States, 1970s–80s", "la « French Theory »" if fr else "“French Theory” in", "dans les départements" if fr else "literature departments", "de lettres" if fr else ""], True),
        (575, 40, 175, ["Théorie postcoloniale" if fr else "Postcolonial theory", "Said, L’Orientalisme (1978)" if fr else "Said, Orientalism (1978)", "Subaltern Studies (1982-)", "Spivak (1988)"], True),
        (500, 180, 250, ["Critiques de gauche" if fr else "Critics on the left", "Ahmad, In Theory (1992)", "Chibber, Postcolonial Theory and", "the Specter of Capital (2013)"], False),
    ]
    for bx, by, bw, lines, here in boxes:
        lines = [l for l in lines if l]
        bh = 22 + 16 * len(lines)
        o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="none" class="{"stroke-pencil" if here else "stroke-ink"}" stroke-width="1.2"/>')
        for i, line in enumerate(lines):
            cls = ("pencil" if here else "graphite") if i == 0 else "ink"
            wt = ' font-weight="600"' if i == 0 else ""
            o.append(f'<text x="{bx+12}" y="{by+22+16*i}" font-size="11" class="{cls}"{wt}>{esc(line)}</text>')
    for x1, x2 in ((180, 198), (365, 383), (555, 573)):
        o.append(f'<line x1="{x1}" y1="70" x2="{x2}" y2="70" class="stroke-pencil" stroke-width="1.4" marker-end="url(#tv-arrow)"/>')
    o.append('<path d="M640,178 C640,160 660,150 660,130" fill="none" class="stroke-ink" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#tv-arrow)"/>')
    o.append(f'<text x="668" y="160" font-size="10" class="graphite" font-style="italic">{"répond" if fr else "replies"}</text>')
    o.append("</svg>")
    cap = ("Un trajet schématique, d’après François Cusset, <em>French Theory</em> (2003). Les flèches pleines suivent la diffusion ; la flèche pointillée, la critique venue de la gauche, dont celle de Chomsky est proche." if fr else
           "A schematic route, after François Cusset, <em>French Theory</em> (2003). Solid arrows follow the spread; the dotted arrow marks the critique from the left, to which Chomsky’s is close.")
    figure("travels", lang, "\n".join(o), cap)

if __name__ == "__main__":
    for lang in ("en", "fr"):
        translations(lang); positivism(lang); attic(lang); gulag(lang)
        cycles(lang); foundations(lang); travels(lang)
    print("written:", sorted(os.listdir(OUT["en"])))
