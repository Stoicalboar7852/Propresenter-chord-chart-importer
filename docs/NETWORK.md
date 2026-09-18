# What PCCI connects to

Everything on this page is for the person who has to approve it: a network
administrator, a school IT department, a church tech lead. If you only need the list of
domains to paste into a ticket, it is in [One list to paste](#one-list-to-paste).

**Converting a file needs no network at all.** Drop a Word document, a PDF or a ChordPro
file on the window and the whole conversion happens on your machine. The connections
below exist for one feature: finding a song online by name or by link.

## The short version

| | |
|---|---|
| Protocol | HTTPS on port 443. Nothing else. |
| Direction | Outbound only. PCCI opens no ports and listens on nothing. |
| What is sent | The words you typed in the search box, or the link you pasted. |
| What is not sent | No account details, no telemetry, no analytics, no crash reports, nothing about your files. PCCI has no accounts and no server of its own. |
| Identifies itself as | `Mozilla/5.0 (compatible; pcci/<version>; +https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer)` |
| Private addresses | Refused. A link that resolves to a local, loopback or link-local address is rejected before any request is made, and every redirect is re-checked. |
| If a domain stays blocked | That source is skipped, the search still runs, and the result names which sites answered. Blocking all of them leaves the file-based conversion working. |

## The domains, and what each one is for

### Searching for a song

These are asked in parallel every time you search. None of them is individually
required: whichever ones answer are merged into the results.

| Domain | What it is | What PCCI asks it for |
|---|---|---|
| `itunes.apple.com` | Apple's iTunes Search API | The song's real title, artist, album, year and cover art. No key, no account. |
| `www.ultimate-guitar.com` | Ultimate Guitar | Chord charts — the only source here that reliably has chords over the words. |
| `tabs.ultimate-guitar.com` | Ultimate Guitar (chart pages) | The chart itself, once a result is chosen. |
| `genius.com` | Genius | Lyrics, and the section labels (Verse, Chorus) most other sources do not carry. |
| `lrclib.net` | LRCLIB | An open, keyless lyrics API. Fills the gap for songs no chord site carries. |

### Cover art

The search results show each song's artwork. The picture is fetched by the app from
whichever address the source above gave it, so these are the image servers those two
use. Blocking them costs you the artwork and nothing else.

| Domain | What it is |
|---|---|
| `*.mzstatic.com` | Apple's artwork servers (`is1-ssl.mzstatic.com` through `is5-ssl.mzstatic.com`). |
| `images.genius.com` | Genius artwork. |
| `t2.genius.com` | Genius image resizer. |

### Optional, and off unless you turn it on

| Domain | What it is | When it is used |
|---|---|---|
| `api.musixmatch.com` | Musixmatch API | Only when a Musixmatch API key is set in the `PCCI_MUSIXMATCH_KEY` environment variable. With no key, PCCI never contacts it. |
| `www.musixmatch.com` | Musixmatch website | The link shown beside a Musixmatch result. Only opened if somebody clicks it. |
| `music.apple.com` | Apple Music | The link shown beside an Apple result. Only opened if somebody clicks it. |

### Getting the program in the first place

Not needed to run PCCI, only to download or update it.

| Domain | What it is |
|---|---|
| `github.com` | Where the releases are published. |
| `objects.githubusercontent.com` | Where GitHub serves the actual download. |

### Anything you paste

The search box also accepts a pasted link, which is the point of it: a chord site, a
church's own song page, a Google Doc published to the web, a ChordPro file in a
repository. PCCI will fetch **whatever address you paste**, so that host is reached too.
If your policy is an allow-list, people will be able to search the sites above and paste
links only to hosts you have allowed.

## One list to paste

Everything, in the order above. Ports: 443/TCP outbound.

```
itunes.apple.com
www.ultimate-guitar.com
tabs.ultimate-guitar.com
genius.com
lrclib.net
is1-ssl.mzstatic.com
is2-ssl.mzstatic.com
is3-ssl.mzstatic.com
is4-ssl.mzstatic.com
is5-ssl.mzstatic.com
images.genius.com
t2.genius.com
api.musixmatch.com
www.musixmatch.com
music.apple.com
github.com
objects.githubusercontent.com
```

If your filter takes wildcards, this is the same list shorter:

```
itunes.apple.com
music.apple.com
*.mzstatic.com
*.ultimate-guitar.com
*.genius.com
lrclib.net
*.musixmatch.com
github.com
objects.githubusercontent.com
```

## What to say when you ask

Most of this is easier to approve if it is described accurately, so: PCCI is a desktop
program that turns a chord chart into a presentation file. The network feature is a
song search that queries five public music and lyrics sites, reads back song titles and
words, and downloads cover-art thumbnails. It sends only the search text, stores nothing
about the user, requires no sign-in, and works without any of it — the network is a
convenience, not a dependency.

Ultimate Guitar and Genius are the two most likely to be blocked, usually as
"entertainment" or "streaming". They are the two that carry the words and the chords,
so if only some can be allowed, those are the ones worth arguing for; `lrclib.net` and
`itunes.apple.com` are plain APIs with no site attached and tend to pass without
trouble.

## Checking it from the machine itself

Each of these should return quickly. A block usually shows up as a timeout, a refusal,
or an HTML login page where JSON was expected.

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://itunes.apple.com/search?term=test
curl -sS -o /dev/null -w '%{http_code}\n' https://lrclib.net/api/search?q=test
curl -sS -o /dev/null -w '%{http_code}\n' https://www.ultimate-guitar.com/search.php?search_type=title&value=test
curl -sS -o /dev/null -w '%{http_code}\n' https://genius.com/api/search/song?q=test
```

PCCI itself will tell you which ones answered: run a search and read the notes under the
results, or from a terminal

```bash
pcci search "amazing grace"
```

which names the source behind every row it found.
