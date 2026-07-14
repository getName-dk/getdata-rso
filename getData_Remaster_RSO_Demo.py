#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
getData Remaster RSO Demo

This is a review/demo version for Riot Production/RSO application.
It uses sample data only and does not connect to Riot services.
No API keys, RSO client secrets, access tokens, or private match records are included.
"""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


APP_TITLE = "getData Remaster RSO Demo"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "sample_data"


def load_json(name: str):
    path = DATA_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


class GetDataRSODemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1120x720")
        self.minsize(980, 620)

        self.matches = load_json("matches.json")
        self.participants = load_json("participants.json")
        self.scores = load_json("performance_scores.json")
        self.rso_mock = load_json("rso_mock.json")
        self.migration_candidates = load_json("migration_candidates.json")

        self.configure(bg="#0b1020")
        self._setup_style()
        self._build_layout()

    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#0b1020")
        style.configure("Panel.TFrame", background="#121a33", relief="flat")
        style.configure("TLabel", background="#0b1020", foreground="#eef3ff", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#0b1020", foreground="#eef3ff", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background="#0b1020", foreground="#aab6d3", font=("Segoe UI", 10))
        style.configure("PanelTitle.TLabel", background="#121a33", foreground="#eef3ff", font=("Segoe UI", 13, "bold"))
        style.configure("PanelText.TLabel", background="#121a33", foreground="#aab6d3", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", background="#10172c", foreground="#eef3ff", fieldbackground="#10172c", rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background="#17203c", foreground="#eef3ff", font=("Segoe UI", 10, "bold"))

    def _build_layout(self):
        root = ttk.Frame(self)
        root.pack(fill="both", expand=True, padx=20, pady=20)

        header = ttk.Frame(root)
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text=APP_TITLE, style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Private local admin tool demo. Sample data only. RSO flow is mocked until Riot approval.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        self._tab_dashboard()
        self._tab_records()
        self._tab_rankings()
        self._tab_rso()
        self._tab_migration()
        self._tab_policy()

    def _make_tab(self, title: str):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text=title)
        return frame

    def _panel(self, parent, title: str, text: str):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=18)
        ttk.Label(panel, text=title, style="PanelTitle.TLabel").pack(anchor="w")
        ttk.Label(panel, text=text, style="PanelText.TLabel", wraplength=300).pack(anchor="w", pady=(8, 0))
        return panel

    def _tab_dashboard(self):
        tab = self._make_tab("Dashboard")
        top = ttk.Frame(tab)
        top.pack(fill="x", padx=18, pady=18)

        cards = [
            ("Legacy Records", f"{len(self.matches)} sample games", "Existing getData records remain preserved as legacy data."),
            ("Migration Candidates", f"{len(self.migration_candidates)} sample candidate", "RSO/Riot match data is linked only after review."),
            ("Player Scores", f"{len(self.scores)} sample ranks", "MVP/ACE and performance score engine preview."),
        ]
        for i, (title, metric, desc) in enumerate(cards):
            p = ttk.Frame(top, style="Panel.TFrame", padding=18)
            p.grid(row=0, column=i, sticky="nsew", padx=8)
            top.columnconfigure(i, weight=1)
            ttk.Label(p, text=title, style="PanelTitle.TLabel").pack(anchor="w")
            ttk.Label(p, text=metric, style="PanelTitle.TLabel").pack(anchor="w", pady=(10, 4))
            ttk.Label(p, text=desc, style="PanelText.TLabel", wraplength=260).pack(anchor="w")

        info = ttk.Frame(tab, style="Panel.TFrame", padding=18)
        info.pack(fill="both", expand=True, padx=26, pady=(4, 18))
        ttk.Label(info, text="Review Purpose", style="PanelTitle.TLabel").pack(anchor="w")
        body = (
            "This demo shows the intended local administrator getData Remaster flow for Riot Production/RSO review.\n\n"
            "Current state: manually entered private custom game records.\n"
            "Planned RSO state: users voluntarily connect Riot accounts, then getData creates migration candidates "
            "between existing private records and Riot match records.\n\n"
            "Safety rule: existing records are not overwritten. Data is stored as legacy + api + resolved fields."
        )
        ttk.Label(info, text=body, style="PanelText.TLabel", wraplength=980, justify="left").pack(anchor="w", pady=(10, 0))

    def _tab_records(self):
        tab = self._make_tab("Manual Records")
        columns = ("legacy_game_id", "player", "line", "champion", "kda", "level", "gold", "damage", "team", "win")
        tree = ttk.Treeview(tab, columns=columns, show="headings")
        headings = {
            "legacy_game_id": "Legacy Game",
            "player": "Player",
            "line": "Line",
            "champion": "Champion",
            "kda": "KDA",
            "level": "Level",
            "gold": "Gold",
            "damage": "Damage",
            "team": "Legacy Team",
            "win": "Win",
        }
        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=110, anchor="center")
        tree.column("legacy_game_id", width=180)
        tree.column("player", width=120)

        for p in self.participants:
            tree.insert("", "end", values=(
                p["legacy_game_id"], p["player"], p["line"], p["champion"],
                f'{p["kills"]}/{p["deaths"]}/{p["assists"]}',
                p["level"], p["gold"], p["damage"], p["team"], "Y" if p["win"] else "N"
            ))
        tree.pack(fill="both", expand=True, padx=18, pady=18)

    def _tab_rankings(self):
        tab = self._make_tab("MVP / Rankings")
        columns = ("rank", "player", "score", "tags")
        tree = ttk.Treeview(tab, columns=columns, show="headings")
        for col, label in zip(columns, ["Rank", "Player", "Performance Score", "Tags"]):
            tree.heading(col, text=label)
            tree.column(col, anchor="center", width=160)
        tree.column("tags", width=360)
        for s in sorted(self.scores, key=lambda x: x["rank"]):
            tree.insert("", "end", values=(s["rank"], s["player"], s["score"], ", ".join(s["tags"])))
        tree.pack(fill="both", expand=True, padx=18, pady=18)

    def _tab_rso(self):
        tab = self._make_tab("Riot Account Link")
        panel = ttk.Frame(tab, style="Panel.TFrame", padding=24)
        panel.pack(fill="both", expand=True, padx=18, pady=18)
        ttk.Label(panel, text="Planned Riot Sign On Flow", style="PanelTitle.TLabel").pack(anchor="w")
        txt = (
            "This demo does not connect to Riot services.\n\n"
            "After Production/RSO approval, this screen will open the Riot Sign On authorization page for participant opt-in. "
            "The user will log in, grant consent, and return to the configured callback URL.\n\n"
            f"Planned redirect URI for local prototype: {self.rso_mock.get('planned_redirect_uri')}\n\n"
            "Collected after opt-in: PUUID, gameName, tagLine."
        )
        ttk.Label(panel, text=txt, style="PanelText.TLabel", wraplength=900, justify="left").pack(anchor="w", pady=(12, 18))
        ttk.Button(panel, text="Connect Riot Account (Mock)", style="Accent.TButton", command=self._mock_connect).pack(anchor="w")

    def _mock_connect(self):
        messagebox.showinfo(
            "Mock RSO Flow",
            "This is a non-network demo.\n\nAfter Riot approval, this button will redirect users to Riot Sign On."
        )

    def _tab_migration(self):
        tab = self._make_tab("Migration Candidates")
        columns = ("legacy_game_id", "match_id", "confidence", "team_mapping", "status", "evidence")
        tree = ttk.Treeview(tab, columns=columns, show="headings")
        labels = ["Legacy Game", "Match ID", "Confidence", "Team Mapping", "Status", "Evidence"]
        for col, label in zip(columns, labels):
            tree.heading(col, text=label)
            tree.column(col, anchor="center", width=150)
        tree.column("evidence", width=360)

        for c in self.migration_candidates:
            ev = c.get("evidence", {})
            evidence_text = f'champs:{ev.get("champion_matches")} kda:{ev.get("kda_matches")} participants:{ev.get("participant_matches")}'
            tree.insert("", "end", values=(c["legacy_game_id"], c["match_id"], c["confidence"], c["team_mapping"], c["status"], evidence_text))
        tree.pack(fill="both", expand=True, padx=18, pady=18)

    def _tab_policy(self):
        tab = self._make_tab("Data Policy")
        panel = ttk.Frame(tab, style="Panel.TFrame", padding=24)
        panel.pack(fill="both", expand=True, padx=18, pady=18)
        ttk.Label(panel, text="Safety and Privacy Rules", style="PanelTitle.TLabel").pack(anchor="w")
        text = (
            "1. This demo contains sample data only.\n"
            "2. No real API keys, RSO client secrets, access tokens, or private records are included.\n"
            "3. Existing getData records are treated as legacy data and are never overwritten automatically.\n"
            "4. RSO/Riot match data creates migration candidates for review.\n"
            "5. Users can disconnect Riot accounts and request deletion of stored mappings or tokens.\n"
            "6. The app is private, non-commercial, and not used for gambling or betting."
        )
        ttk.Label(panel, text=text, style="PanelText.TLabel", wraplength=920, justify="left").pack(anchor="w", pady=(12, 0))


if __name__ == "__main__":
    app = GetDataRSODemo()
    app.mainloop()
