"""Tests for Diari del Consell General acquisition (PLAN M1.04-05).

The fixtures are cut from a real session — DCG 01/2023, fetched 2026-08-02 — including its
defects, because the defects are what this module exists to handle.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from maia.schemas import License, Registre, Source
from maia.scraping.consell import (
    ARCHIVE,
    DOWNLOAD_SUFFIX,
    FIRST_ARCHIVED_YEAR,
    LAST_ARCHIVED_YEAR,
    Acquired,
    Session,
    WhitelistEntry,
    extract_pdf_text,
    fetch_session_documents,
    find_sessions,
    load_whitelist,
    main,
    match_whitelist,
    names_for_year,
    repair_pdf_text,
    scrape_year,
    speaker_counts,
    summarise,
)

STAMP = datetime(2026, 8, 2, tzinfo=UTC)
BASE = "https://www.consellgeneral.ad/ca/arxiu/diari-oficial-del-consell-general-1"

# Verbatim from the real archive index: the same session is linked several times, and the
# numbering is inconsistent (`dcg-1-2022` next to `dcg-02-2022`).
INDEX_HTML = f"""
<html><body>
  <a href="{BASE}/any-2022/dcg-1-2022">DCG 1/2022</a>
  <a href="{BASE}/any-2022/dcg-02-2022">DCG 02/2022</a>
  <a href="{BASE}/any-2022/dcg-1-2022">DCG 1/2022</a>
  <a href="{BASE}/any-2022/dcg-10-2022">DCG 10/2022</a>
  <a href="{BASE}/any-2022/dcg-02-2022/sendto_form">send</a>
  <a href="https://www.consellgeneral.ad/ca/noticies/una-noticia">not a session</a>
</body></html>
"""

#: The running footer, exactly as it appears mid-sentence on every page. Assembled rather than
#: written inline only because it is longer than the line limit.
_FOOTER_LINE = (
    "Diari oficial del Consell General \u2013 núm. 1/2023 \u2013 "
    "Sessió ordinària celebrada el dia 12 de gener del 2023 7"
)

# The three defects, as the extractor really emits them.
RAW_PDF_TEXT = f"""El Sr. Xavier Espot:
Gràcies, senyora síndica. Estic d ’acord amb l ’article que se ’m planteja i amb el con-
{_FOOTER_LINE}
tingut de la resposta que s ’ha donat.

El Sr. Raul Ferré:
Gràcies. Voldria saber si el Govern té previst d ’actuar en aquest àmbit abans que s ’acabi
l ’any, perquè les dades que tenim indiquen que la situació no ha millorat gens.

La Sra. síndica general:
Gràcies.
"""


@pytest.mark.unit
def test_the_archive_extent_is_recorded_not_assumed() -> None:
    """Verified against the live site: 1990-2023 return 200 and 2024 onward 404. A scraper that
    silently returns nothing for recent years is worse than one that says it does not cover them."""
    assert (FIRST_ARCHIVED_YEAR, LAST_ARCHIVED_YEAR) == (1990, 2023)
    assert ARCHIVE.format(year=2023).endswith("/any-2023")


# ── discovery ────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_sessions_are_found_deduplicated_and_in_published_order() -> None:
    """Not sorted: `dcg-10` would come before `dcg-2` as a string, and the archive numbering is
    inconsistent enough (`dcg-1-2022` beside `dcg-02-2022`) that constructing URLs from a counter
    would skip real sessions."""
    sessions = find_sessions(INDEX_HTML, year=2022)
    assert [s.slug for s in sessions] == ["dcg-1-2022", "dcg-02-2022", "dcg-10-2022"]
    assert all(s.year == 2022 for s in sessions)


@pytest.mark.unit
def test_a_session_knows_where_its_pdf_is() -> None:
    session = Session(url=f"{BASE}/any-2023/dcg-01-2023", year=2023)
    assert session.pdf_url == f"{BASE}/any-2023/dcg-01-2023{DOWNLOAD_SUFFIX}"
    assert session.slug == "dcg-01-2023"


@pytest.mark.unit
def test_non_session_links_are_not_mistaken_for_sessions() -> None:
    assert (
        find_sessions('<a href="https://www.consellgeneral.ad/ca/noticies/x">n</a>', year=2022)
        == []
    )


# ── PDF repair: the reason this module exists ────────────────────────────────


@pytest.mark.unit
def test_the_space_before_every_apostrophe_is_closed_up() -> None:
    """371 of these in one 54-page session. Left in, the corpus teaches the model to write Catalan
    elisions with a space in them — and nothing downstream catches it, because `d ’acord` is
    well-formed UTF-8, is in Catalan, and passes the language detector."""
    repaired = repair_pdf_text(RAW_PDF_TEXT)
    for broken in ("d ’acord", "l ’article", "se ’m", "s ’ha"):
        assert broken not in repaired
    for fixed in ("d’acord", "l’article", "se’m", "s’ha"):
        assert fixed in repaired


@pytest.mark.unit
def test_the_running_footer_is_removed() -> None:
    """53 per session, each cutting a sentence in half where the page broke."""
    repaired = repair_pdf_text(RAW_PDF_TEXT)
    assert "Diari oficial del Consell General" not in repaired
    assert "núm. 1/2023" not in repaired


@pytest.mark.unit
def test_a_word_split_across_a_page_break_is_rejoined() -> None:
    """`con-\\ntingut` is one word, and the footer sat between its halves."""
    assert "contingut" in repair_pdf_text(RAW_PDF_TEXT)


@pytest.mark.unit
def test_repair_never_touches_the_words_themselves() -> None:
    """Same rule as `clean_oral`: a helpful normaliser is how genuine Andorran lexicon gets
    rewritten into standard Catalan."""
    andorran = "El poble andorrà plega a les set i la canalla fa cap a casa."
    assert repair_pdf_text(andorran) == andorran


@pytest.mark.unit
def test_an_apostrophe_that_is_already_correct_is_left_alone() -> None:
    assert repair_pdf_text("d’acord amb l’article") == "d’acord amb l’article"


# ── PDF extraction ───────────────────────────────────────────────────────────


@pytest.mark.unit
def test_unreadable_bytes_raise_rather_than_return_nothing() -> None:
    """An empty string would be indistinguishable from a session with no interventions."""
    with pytest.raises(ValueError, match="unreadable PDF"):
        extract_pdf_text(b"this is not a PDF")


@pytest.mark.unit
def test_a_scanned_pdf_says_it_needs_ocr(tmp_path: object) -> None:
    """A PDF of page images extracts to nothing. Saying "no text" sends someone looking for a
    parser bug; saying "this is a scan" sends them to OCR."""
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    from io import BytesIO

    buffer = BytesIO()
    writer.write(buffer)
    with pytest.raises(ValueError, match="OCR"):
        extract_pdf_text(buffer.getvalue())


# ── the whitelist mismatch that fails silently ───────────────────────────────


@pytest.mark.unit
def test_a_whitelist_copied_from_the_attendance_list_is_reported() -> None:
    """The failure this check exists for, and it happened during development. The Diari prints
    "M. I. Sr. Raul Ferré Bonet" when taking attendance and "El Sr. Raul Ferré:" above what he
    says. A whitelist copied from the attendance list matches nothing, and the run then *succeeds*
    having ingested none of that person."""
    match = match_whitelist(["Raul Ferré", "Xavier Espot"], ["Xavier Espot", "Raul Ferré Bonet"])
    assert not match.ok
    assert match.matched == ("Xavier Espot",)
    assert match.unmatched == ("Raul Ferré Bonet",)
    assert match.suggestions["Raul Ferré Bonet"] == ("Raul Ferré",)
    assert "did you mean 'Raul Ferré'" in match.report()


@pytest.mark.unit
def test_a_fully_matched_whitelist_reports_nothing() -> None:
    match = match_whitelist(["Xavier Espot", "Pere López"], ["xavier  ESPOT"])
    assert match.ok
    assert match.report() == ""


@pytest.mark.unit
def test_an_unmatched_name_with_no_lookalike_still_reports() -> None:
    match = match_whitelist(["Xavier Espot"], ["Algú Que No Hi És"])
    assert not match.ok
    assert "never spoke" in match.report()
    assert "did you mean" not in match.report()


@pytest.mark.unit
def test_a_single_word_speaker_is_not_suggested() -> None:
    """ "síndica general" shares no surname with anybody; suggesting it for every miss would train
    the reader to ignore the warning."""
    match = match_whitelist(["síndica general", "secretària"], ["Xavier Espot"])
    assert match.suggestions == {}


# ── fetching ─────────────────────────────────────────────────────────────────


class FakeFetcher:
    """Stands in for PoliteFetcher: serves pages and PDFs from a map."""

    def __init__(self, pages: dict[str, str], pdfs: dict[str, bytes] | None = None) -> None:
        self.pages = pages
        self.pdfs = pdfs or {}
        self.disallowed: list[str] = []
        self.requested: list[str] = []

    def fetch(self, url: str) -> str | None:
        self.requested.append(url)
        return self.pages.get(url)

    def fetch_bytes(self, url: str) -> bytes | None:
        self.requested.append(url)
        return self.pdfs.get(url)


def _pdf(text: str) -> bytes:
    """A minimal but genuinely valid PDF containing ``text``, so extraction is really exercised.

    Written by hand rather than with a library: the point is to feed `pypdf` something a real
    generator would produce, including the font resource without which text extracts as nothing —
    which is exactly the "scanned PDF" case, and would make these tests pass for the wrong reason.

    The page uses WinAnsi, so the fixture text uses the ASCII apostrophe. Both forms appear in the
    real archive and `repair_pdf_text` handles both; the typographic one is covered directly in
    the repair tests, where there is no encoding in the way.
    """
    escaped = "\n".join(
        "({}) Tj T*".format(line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)"))
        for line in text.split("\n")
    )
    content = f"BT /F1 11 Tf 13 TL 40 750 Td\n{escaped}\nET".encode("latin-1", "replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for index, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{index} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    ).encode()
    return bytes(out)


#: Same defects as RAW_PDF_TEXT, with the ASCII apostrophe the PDF encoding can carry.
PDF_TEXT = RAW_PDF_TEXT.replace("\u2019", "'")


@pytest.mark.unit
def test_a_session_yields_documents_and_the_full_speaker_list() -> None:
    """The speaker list is not decoration: without it the caller cannot tell "the whitelist
    matched nobody" from "nobody said anything"."""
    session = Session(url=f"{BASE}/any-2023/dcg-01-2023", year=2023)
    fetcher = FakeFetcher({}, {session.pdf_url: _pdf(PDF_TEXT)})

    acquired = fetch_session_documents(
        fetcher,  # type: ignore[arg-type]
        session,
        whitelist=[WhitelistEntry("Xavier Espot")],
        fetched_at=STAMP,
        topic=["institucions"],
    )
    assert {"Xavier Espot", "Raul Ferré", "síndica general"} <= set(acquired.speakers)
    assert len(acquired.documents) == 1

    document = acquired.documents[0]
    assert document.source is Source.CONSELL_DIARI_SESSIONS
    assert document.license is License.PUBLIC_OFFICIAL
    assert document.registre is Registre.ANDORRA_PARLAT
    assert str(document.url) == session.url
    assert document.fetched_at == STAMP
    assert "d’acord" in document.text


@pytest.mark.unit
def test_the_speaker_is_recorded_so_the_d7_protection_is_downstream_not_structural() -> None:
    """§3.1 has a `speaker` field, it is deliberate (a quotation must be attributable), and this
    pipeline fills it in — so the corpus **can** be filtered down to one person.

    This test exists to stop anyone concluding otherwise from reading the module. The protection
    against reproducing an identifiable voice is D7 plus the M6.01 publication gate, and both have
    to keep being enforced; the ingest does not make the misuse impossible.
    """
    session = Session(url=f"{BASE}/any-2023/dcg-01-2023", year=2023)
    fetcher = FakeFetcher({}, {session.pdf_url: _pdf(PDF_TEXT)})
    acquired = fetch_session_documents(
        fetcher,  # type: ignore[arg-type]
        session,
        whitelist=[WhitelistEntry("Xavier Espot"), WhitelistEntry("Raul Ferré")],
    )
    speakers = {document.speaker for document in acquired.documents}
    assert speakers == {"Xavier Espot", "Raul Ferré"}
    # And the schema only tolerates it for this one source.
    assert all(d.source is Source.CONSELL_DIARI_SESSIONS for d in acquired.documents)


@pytest.mark.unit
def test_an_unreachable_or_unreadable_session_does_not_stop_the_run() -> None:
    """A year contains scanned procedural sittings; one of them must not end the acquisition."""
    session = Session(url=f"{BASE}/any-2023/dcg-99-2023", year=2023)
    missing = fetch_session_documents(
        FakeFetcher({}, {}),  # type: ignore[arg-type]
        session,
        whitelist=[WhitelistEntry("X")],
    )
    assert missing == Acquired()

    broken = FakeFetcher({}, {session.pdf_url: b"not a pdf"})
    assert fetch_session_documents(broken, session, whitelist=[WhitelistEntry("X")]) == Acquired()  # type: ignore[arg-type]


@pytest.mark.unit
def test_scrape_year_walks_the_index() -> None:
    index_url = ARCHIVE.format(year=2022)
    first = f"{BASE}/any-2022/dcg-1-2022"
    fetcher = FakeFetcher(
        {index_url: INDEX_HTML},
        {f"{first}{DOWNLOAD_SUFFIX}": _pdf(PDF_TEXT)},
    )
    acquired = scrape_year(fetcher, 2022, whitelist=[WhitelistEntry("Xavier Espot")], limit=1)  # type: ignore[arg-type]
    assert len(acquired.documents) == 1
    assert fetcher.requested == [index_url, f"{first}{DOWNLOAD_SUFFIX}"]


@pytest.mark.unit
def test_a_missing_index_yields_nothing_rather_than_raising() -> None:
    assert scrape_year(FakeFetcher({}), 1970, whitelist=[WhitelistEntry("X")]) == Acquired()  # type: ignore[arg-type]


@pytest.mark.unit
def test_acquired_results_add_up() -> None:
    left = Acquired((), ("a",))
    right = Acquired((), ("b",))
    assert (left + right).speakers == ("a", "b")


@pytest.mark.unit
def test_speaker_counts_reports_who_actually_took_the_floor() -> None:
    """The attendance list names everybody present; most never speak. Choosing a whitelist needs
    the second list, not the first."""
    counts = speaker_counts(RAW_PDF_TEXT)
    assert counts == {"Xavier Espot": 1, "Raul Ferré": 1, "síndica general": 1}


@pytest.mark.unit
def test_summarise_counts_characters_not_just_documents() -> None:
    session = Session(url=f"{BASE}/any-2023/dcg-01-2023", year=2023)
    fetcher = FakeFetcher({}, {session.pdf_url: _pdf(PDF_TEXT)})
    acquired = fetch_session_documents(fetcher, session, whitelist=[WhitelistEntry("Xavier Espot")])  # type: ignore[arg-type]
    assert "1 intervention(s)" in summarise(acquired.documents)
    assert summarise(()) == "0 intervention(s), 0 characters"


# ── the shipped whitelist and the CLI ────────────────────────────────────────


@pytest.mark.unit
def test_the_shipped_whitelist_is_wide_enough_that_nobody_is_reproducible() -> None:
    """The measurement that forced this file to grow. With two names, **94% of the corpus was one
    person** — which teaches an idiolect rather than a register, and is what D7 forbids. Widening
    to every named speaker with >=40 substantive interventions took the largest share to ~13% and
    the corpus from 2.1M to 15.9M characters, from PDFs already on disk.

    The assertion is on the *shape* of the list, not its exact contents: the PO may add or remove
    a name (D-0049), but dropping back to a handful would silently restore the failure.
    """
    from pathlib import Path

    entries = load_whitelist(Path(__file__).resolve().parents[1] / "configs" / "parlamentaris.txt")
    names = {e.name for e in entries}
    assert len(names) >= 25, "too few speakers: one voice will dominate the corpus again"

    # Offices of the chair are excluded on purpose: "síndica general" has more interventions than
    # anyone and almost all are procedural, so including them refills the corpus with formulae.
    assert not {n for n in names if n.lower().startswith(("síndic", "sindic"))}

    # The names the PO asked for by hand are present, in the printed form.
    assert {"Xavier Espot", "Raul Ferré"} <= names
    assert "Raul Ferré Bonet" not in names

    # 2021: the Diari printed the office, so it must be matched that year.
    assert "cap de Govern" in names_for_year(entries, 2021)
    # 2015: the office was Toni Martí's. Matching it would attribute his words to Espot.
    assert "cap de Govern" not in names_for_year(entries, 2015)


@pytest.mark.unit
def test_both_spellings_of_a_name_are_listed_rather_than_folded() -> None:
    """The Diari prints "Èric Jover" and "Eric Jover". Listed twice on purpose: folding accents in
    the matcher would risk merging genuinely different names, and this corpus has 37 speakers."""
    from pathlib import Path

    names = {
        e.name
        for e in load_whitelist(
            Path(__file__).resolve().parents[1] / "configs" / "parlamentaris.txt"
        )
    }
    assert {"Èric Jover", "Eric Jover"} <= names


@pytest.mark.unit
def test_the_cli_refuses_a_missing_or_empty_whitelist(
    tmp_path: object, capsys: pytest.CaptureFixture[str]
) -> None:
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    assert main(["--whitelist", str(tmp_path / "nope.txt")]) == 1
    assert "no whitelist" in capsys.readouterr().err

    empty = tmp_path / "empty.txt"
    empty.write_text("# only a comment\n", encoding="utf-8")
    assert main(["--whitelist", str(empty)]) == 1
    assert "lists no speakers" in capsys.readouterr().err


@pytest.mark.unit
def test_the_cli_writes_jsonl_and_warns_about_an_unmatched_whitelist(
    tmp_path: object, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """End to end over a fake network: index, PDF, whitelist, output, warning."""
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    index_url = ARCHIVE.format(year=2022)
    session_pdf = f"{BASE}/any-2022/dcg-1-2022{DOWNLOAD_SUFFIX}"
    fetcher = FakeFetcher({index_url: INDEX_HTML}, {session_pdf: _pdf(PDF_TEXT)})
    monkeypatch.setattr("maia.scraping.http.polite_fetcher", lambda **kwargs: fetcher)

    whitelist = tmp_path / "w.txt"
    whitelist.write_text("Xavier Espot\nAlgú Absent\n", encoding="utf-8")
    out = tmp_path / "corpus.jsonl"

    code = main(
        [
            "--from-year",
            "2022",
            "--to-year",
            "2022",
            "--limit",
            "1",
            "--whitelist",
            str(whitelist),
            "--out",
            str(out),
        ]
    )
    assert code == 0
    lines = out.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert "consell_diari_sessions" in lines[0]

    captured = capsys.readouterr()
    assert "1 intervention(s)" in captured.out
    assert "wrote 1 document(s)" in captured.out
    assert "Algú Absent" in captured.err  # the silent-failure warning


@pytest.mark.unit
def test_the_cli_dry_run_fetches_no_pdfs(
    tmp_path: object, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The right first command when the site's layout may have changed under us."""
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    index_url = ARCHIVE.format(year=2022)
    fetcher = FakeFetcher({index_url: INDEX_HTML})
    monkeypatch.setattr("maia.scraping.http.polite_fetcher", lambda **kwargs: fetcher)

    whitelist = tmp_path / "w.txt"
    whitelist.write_text("Xavier Espot\n", encoding="utf-8")

    assert (
        main(
            ["--from-year", "2022", "--to-year", "2022", "--dry-run", "--whitelist", str(whitelist)]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "2022: 3 session(s)" in out
    assert DOWNLOAD_SUFFIX in out
    assert fetcher.requested == [index_url]  # no PDF was fetched


@pytest.mark.unit
def test_a_run_that_collected_nothing_exits_non_zero(
    tmp_path: object, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Zero documents means the layout changed, the whitelist names nobody who spoke, or robots
    blocked everything — never "the sessions were empty". A zero exit would hide all three."""
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    fetcher = FakeFetcher({})
    fetcher.disallowed.append("https://www.consellgeneral.ad/blocked")
    monkeypatch.setattr("maia.scraping.http.polite_fetcher", lambda **kwargs: fetcher)

    whitelist = tmp_path / "w.txt"
    whitelist.write_text("Xavier Espot\n", encoding="utf-8")
    assert main(["--from-year", "2022", "--to-year", "2022", "--whitelist", str(whitelist)]) == 1
    assert "robots.txt disallowed 1 URL(s)" in capsys.readouterr().err


@pytest.mark.unit
def test_no_limit_walks_every_session_in_the_year() -> None:
    """`--limit` is a development convenience; the default must be the whole year."""
    index_url = ARCHIVE.format(year=2022)
    pdfs = {
        f"{BASE}/any-2022/{slug}{DOWNLOAD_SUFFIX}": _pdf(PDF_TEXT)
        for slug in ("dcg-1-2022", "dcg-02-2022", "dcg-10-2022")
    }
    fetcher = FakeFetcher({index_url: INDEX_HTML}, pdfs)
    acquired = scrape_year(fetcher, 2022, whitelist=[WhitelistEntry("Xavier Espot")])  # type: ignore[arg-type]
    assert len(acquired.documents) == 3


@pytest.mark.unit
def test_the_cli_without_out_still_reports_and_exits_zero(
    tmp_path: object, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Counting what a year holds before committing to a full download is a real use."""
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    index_url = ARCHIVE.format(year=2022)
    fetcher = FakeFetcher(
        {index_url: INDEX_HTML},
        {f"{BASE}/any-2022/dcg-1-2022{DOWNLOAD_SUFFIX}": _pdf(PDF_TEXT)},
    )
    monkeypatch.setattr("maia.scraping.http.polite_fetcher", lambda **kwargs: fetcher)
    whitelist = tmp_path / "w.txt"
    whitelist.write_text("Xavier Espot\n", encoding="utf-8")

    assert (
        main(
            [
                "--from-year",
                "2022",
                "--to-year",
                "2022",
                "--limit",
                "1",
                "--whitelist",
                str(whitelist),
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert "1 intervention(s)" in captured.out
    assert "wrote" not in captured.out


# ── office aliases, and the year range that makes them safe ──────────────────


@pytest.mark.unit
def test_an_office_alias_only_matches_while_its_holder_held_it() -> None:
    """The correctness control this feature exists for. `cap de Govern` is Espot from 2019; before
    that it is Toni Martí. An unscoped alias would attribute one politician's words to another —
    a worse bug than the missing interventions it was added to fix."""
    entries = [WhitelistEntry("Xavier Espot"), WhitelistEntry("cap de Govern", 2019, 2023)]
    assert names_for_year(entries, 2015) == {"Xavier Espot"}
    assert names_for_year(entries, 2021) == {"Xavier Espot", "cap de Govern"}
    assert names_for_year(entries, 2026) == {"Xavier Espot"}


@pytest.mark.unit
def test_an_open_ended_range_is_allowed_at_either_end() -> None:
    assert WhitelistEntry("x", first_year=2019).applies_to(2030)
    assert not WhitelistEntry("x", first_year=2019).applies_to(2018)
    assert WhitelistEntry("x", last_year=2019).applies_to(1999)
    assert not WhitelistEntry("x", last_year=2019).applies_to(2020)
    assert WhitelistEntry("x").applies_to(1066)
    assert WhitelistEntry("x", 2019, 2023).is_office
    assert not WhitelistEntry("x").is_office


@pytest.mark.unit
def test_the_whitelist_file_parses_names_ranges_and_comments(tmp_path: object) -> None:
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    path = tmp_path / "w.txt"
    path.write_text(
        "# a comment\n\nXavier Espot\ncap de Govern [2019-2023]\nRaul Ferré  # trailing comment\n",
        encoding="utf-8",
    )
    entries = load_whitelist(path)
    assert [(e.name, e.first_year, e.last_year) for e in entries] == [
        ("Xavier Espot", None, None),
        ("cap de Govern", 2019, 2023),
        ("Raul Ferré", None, None),
    ]


@pytest.mark.unit
def test_a_malformed_whitelist_line_is_an_error_not_a_skip(tmp_path: object) -> None:
    """A line silently ignored is a speaker silently missing, which is the failure mode this whole
    area keeps producing."""
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    path = tmp_path / "w.txt"
    path.write_text("cap de Govern [2019]\n", encoding="utf-8")
    with pytest.raises(ValueError, match="cannot read whitelist entry"):
        load_whitelist(path)

    path.write_text("cap de Govern [2023-2019]\n", encoding="utf-8")
    with pytest.raises(ValueError, match="ends before it starts"):
        load_whitelist(path)


@pytest.mark.unit
def test_a_session_matches_the_alias_valid_for_its_year() -> None:
    """The 2021 sessions print the office; the 2022 ones print the name. One whitelist, both."""
    transcript = "El Sr. cap de Govern:\n" + "Gràcies, senyora síndica. " * 12
    whitelist = [WhitelistEntry("Xavier Espot"), WhitelistEntry("cap de Govern", 2019, 2023)]

    for year, expected in ((2021, 1), (2015, 0)):
        session = Session(url=f"{BASE}/any-{year}/dcg-1-{year}", year=year)
        fetcher = FakeFetcher({}, {session.pdf_url: _pdf(transcript)})
        acquired = fetch_session_documents(fetcher, session, whitelist=whitelist)  # type: ignore[arg-type]
        assert len(acquired.documents) == expected


@pytest.mark.unit
def test_the_cli_rejects_a_malformed_whitelist(
    tmp_path: object, capsys: pytest.CaptureFixture[str]
) -> None:
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    path = tmp_path / "w.txt"
    path.write_text("cap de Govern [nonsense]\n", encoding="utf-8")
    assert main(["--whitelist", str(path)]) == 1
    assert "cannot read whitelist entry" in capsys.readouterr().err


@pytest.mark.unit
def test_the_footer_of_a_two_day_sitting_is_removed_too() -> None:
    """The first version of this regex spelled out "celebrada el dia" and silently missed every
    two-day sitting, which prints "celebrada els dies 02 i 03". Seven footers survived into a
    2.1M-character corpus before a count caught them, so the match is now on the footer's *shape* —
    starts with the publication's name, ends in a page number — not on its wording."""
    two_day = (
        "abans\n"
        "Diari oficial del Consell General \u2013 núm.25/2021 \u2013 Sessió ordinària "
        "celebrada els dies 02 i 03 de desembre del 2021 95\n"
        "després"
    )
    assert "Diari oficial" not in repair_pdf_text(two_day)
    assert "abans" in repair_pdf_text(two_day)
    assert "després" in repair_pdf_text(two_day)


@pytest.mark.unit
def test_a_sentence_that_mentions_the_publication_is_not_a_footer() -> None:
    """Anchored to a whole line ending in a page number, so a member talking *about* the Diari
    keeps their words."""
    sentence = "El Diari oficial del Consell General publica les lleis aprovades."
    assert repair_pdf_text(sentence) == sentence
