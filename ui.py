import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Dict

from persona import BuddyAI


class ChatUI:
    """Tkinter user interface for Buddy AI chat."""

    def __init__(self, bot: BuddyAI):
        self.bot = bot
        self.root = tk.Tk()
        self.root.title("Buddy AI Chat")
        self.root.geometry("980x620")
        self.root.minsize(900, 560)

        self.style = ttk.Style(self.root)
        self.theme = "dark"
        self.history_items: List[Dict[str, str]] = []
        self._configure_style()
        self._build_interface()
        self._initialize_greeting()

    def _configure_style(self) -> None:
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self.color_palettes = {
            "dark": {
                "bg": "#1f242c",
                "panel_bg": "#252a33",
                "card_bg": "#2e3441",
                "text": "#eef2f7",
                "secondary_text": "#a8b0be",
                "accent": "#7c9cff",
                "button_bg": "#4c6ef5",
                "button_fg": "#ffffff",
                "entry_bg": "#2f3440",
                "entry_fg": "#f3f6fb",
                "listbox_bg": "#252a33",
                "listbox_fg": "#eef2f7",
                "highlight": "#7c9cff"
            },
            "light": {
                "bg": "#f4f7fb",
                "panel_bg": "#ffffff",
                "card_bg": "#eef1f6",
                "text": "#222831",
                "secondary_text": "#5d6d7a",
                "accent": "#3b82f6",
                "button_bg": "#3b82f6",
                "button_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "entry_fg": "#1f2937",
                "listbox_bg": "#ffffff",
                "listbox_fg": "#1f2937",
                "highlight": "#3b82f6"
            }
        }

        self._apply_theme()

    def _apply_theme(self) -> None:
        palette = self.color_palettes[self.theme]
        self.root.configure(bg=palette["bg"])

        self.style.configure("TFrame", background=palette["bg"] )
        self.style.configure("Card.TFrame", background=palette["panel_bg"], borderwidth=0)
        self.style.configure("Header.TLabel", background=palette["bg"], foreground=palette["text"] )
        self.style.configure("Subtitle.TLabel", background=palette["bg"], foreground=palette["secondary_text"] )
        self.style.configure("Accent.TButton", background=palette["button_bg"], foreground=palette["button_fg"], borderwidth=0)
        self.style.map("Accent.TButton", background=[("active", palette["highlight"] )])
        self.style.configure("TButton", background=palette["button_bg"], foreground=palette["button_fg"], borderwidth=0)
        self.style.configure("TLabel", background=palette["bg"], foreground=palette["text"] )
        self.style.configure("TEntry", fieldbackground=palette["entry_bg"], foreground=palette["entry_fg"], background=palette["entry_bg"], bordercolor=palette["highlight"])
        self.style.configure("TScrollbar", background=palette["panel_bg"], troughcolor=palette["bg"], arrowcolor=palette["accent"])

        self.entry_bg = palette["entry_bg"]
        self.entry_fg = palette["entry_fg"]
        self.chat_bg = palette["card_bg"]
        self.chat_fg = palette["text"]
        self.history_bg = palette["listbox_bg"]
        self.history_fg = palette["listbox_fg"]
        self.details_bg = palette["card_bg"]
        self.details_fg = palette["text"]
        self.button_bg = palette["button_bg"]
        self.button_fg = palette["button_fg"]
        self.highlight = palette["highlight"]

    def _build_interface(self) -> None:
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        sidebar_frame = ttk.Frame(self.root, style="Card.TFrame", padding=(14, 14, 12, 14))
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(14, 0), pady=14)
        sidebar_frame.columnconfigure(0, weight=1)
        sidebar_frame.rowconfigure(1, weight=1)

        header_frame = ttk.Frame(sidebar_frame, style="Card.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)

        ttk.Label(header_frame, text="Chat History", style="Header.TLabel", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        self.theme_button = ttk.Button(
            header_frame,
            text="Light Mode",
            command=self.toggle_theme,
            style="Accent.TButton"
        )
        self.theme_button.grid(row=0, column=1, sticky="e")

        self.history_list = tk.Listbox(
            sidebar_frame,
            width=32,
            height=28,
            font=("Segoe UI", 10),
            activestyle="none",
            exportselection=False,
            bg=self.history_bg,
            fg=self.history_fg,
            selectbackground=self.highlight,
            selectforeground=self.history_bg,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.highlight,
            relief="flat"
        )
        self.history_list.grid(row=1, column=0, sticky="nsew")
        self.history_list.bind("<<ListboxSelect>>", self._on_history_select)

        history_scroll = ttk.Scrollbar(sidebar_frame, orient="vertical", command=self.history_list.yview)
        history_scroll.grid(row=1, column=1, sticky="ns")
        self.history_list.configure(yscrollcommand=history_scroll.set)

        self.history_details = scrolledtext.ScrolledText(
            sidebar_frame,
            width=34,
            height=12,
            font=("Segoe UI", 10),
            state="disabled",
            wrap="word",
            bg=self.details_bg,
            fg=self.details_fg,
            insertbackground=self.entry_fg,
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.highlight,
            highlightcolor=self.highlight
        )
        self.history_details.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(14, 0))

        self.clear_history_button = ttk.Button(
            sidebar_frame,
            text="Clear History",
            command=self._clear_history,
            style="Accent.TButton"
        )
        self.clear_history_button.grid(row=3, column=0, columnspan=2, pady=(12, 0), sticky="ew")

        chat_frame = ttk.Frame(self.root, style="Card.TFrame", padding=(12, 14, 16, 14))
        chat_frame.grid(row=0, column=1, sticky="nsew", padx=(12, 14), pady=14)
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(1, weight=1)

        ttk.Label(chat_frame, text="Buddy AI Conversation", style="Header.TLabel", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap="word",
            state="disabled",
            font=("Segoe UI", 11),
            bg=self.chat_bg,
            fg=self.chat_fg,
            insertbackground=self.entry_fg,
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.highlight,
            highlightcolor=self.highlight
        )
        self.chat_display.grid(row=1, column=0, sticky="nsew")
        self.chat_display.tag_configure("user", foreground="#7fc3ff")
        self.chat_display.tag_configure("bot", foreground="#9fefb9")
        self.chat_display.tag_configure("meta", foreground=self.color_palettes[self.theme]["secondary_text"], font=("Segoe UI", 9, "italic"))

        input_frame = ttk.Frame(chat_frame, style="Card.TFrame")
        input_frame.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        input_frame.columnconfigure(0, weight=1)

        self.user_input = ttk.Entry(input_frame, font=("Segoe UI", 11), foreground=self.entry_fg)
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=(0, 4))
        self.user_input.bind("<Return>", self._handle_send_event)
        self.user_input.focus()

        send_button = ttk.Button(input_frame, text="Send", command=self.send_message, style="Accent.TButton")
        send_button.grid(row=0, column=1, sticky="e")

        self.status_label = ttk.Label(
            chat_frame,
            text="Type a message and press Send or Enter.",
            style="Subtitle.TLabel",
            font=("Segoe UI", 9)
        )
        self.status_label.grid(row=3, column=0, sticky="w", pady=(8, 0))

    def toggle_theme(self) -> None:
        self.theme = "light" if self.theme == "dark" else "dark"
        self._apply_theme()
        self._refresh_widgets()
        self.theme_button.configure(text="Dark Mode" if self.theme == "light" else "Light Mode")

    def _refresh_widgets(self) -> None:
        palette = self.color_palettes[self.theme]
        self.root.configure(bg=palette["bg"])
        self.history_list.configure(bg=self.history_bg, fg=self.history_fg, selectbackground=self.highlight, selectforeground=self.history_bg, highlightbackground=self.highlight)
        self.history_details.configure(bg=self.details_bg, fg=self.details_fg, insertbackground=self.entry_fg)
        self.chat_display.configure(bg=self.chat_bg, fg=self.chat_fg, insertbackground=self.entry_fg)
        self.user_input.configure(background=self.entry_bg, foreground=self.entry_fg)
        self.status_label.configure(style="Subtitle.TLabel")
        self.theme_button.configure(style="Accent.TButton")
        self.clear_history_button.configure(style="Accent.TButton")

    def _initialize_greeting(self) -> None:
        greeting = self.bot.default_greeting
        self._append_chat("Buddy", greeting)
        self._add_history_entry("<Start conversation>", greeting)

    def _append_chat(self, speaker: str, text: str) -> None:
        self.chat_display.configure(state="normal")
        if speaker == "You":
            self.chat_display.insert(tk.END, f"{speaker}: {text}\n", "user")
        else:
            self.chat_display.insert(tk.END, f"{speaker}: {text}\n", "bot")
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see(tk.END)

    def _add_history_entry(self, user_text: str, bot_response: str) -> None:
        entry_label = user_text if len(user_text) <= 60 else user_text[:57] + "..."
        self.history_list.insert(tk.END, entry_label)
        self.history_items.append({"user": user_text, "bot": bot_response})
        self.history_list.see(tk.END)

    def _clear_history(self) -> None:
        self.history_list.delete(0, tk.END)
        self.history_items.clear()
        self.history_details.configure(state="normal")
        self.history_details.delete("1.0", tk.END)
        self.history_details.insert(tk.END, "No history selected.")
        self.history_details.configure(state="disabled")
        self.status_label.configure(text="History cleared.")

    def _show_history_details(self, index: int) -> None:
        if index < 0 or index >= len(self.history_items):
            return
        item = self.history_items[index]
        self.history_details.configure(state="normal")
        self.history_details.delete("1.0", tk.END)
        self.history_details.insert(tk.END, f"You:\n{item['user']}\n\nBuddy:\n{item['bot']}")
        self.history_details.configure(state="disabled")

    def _on_history_select(self, event: tk.Event) -> None:
        selection = event.widget.curselection()
        if not selection:
            return
        self._show_history_details(selection[0])

    def _handle_send_event(self, event: tk.Event) -> None:
        self.send_message()
        return "break"

    def send_message(self) -> None:
        user_text = self.user_input.get().strip()
        if not user_text:
            self.status_label.configure(text="Please enter a message before sending.")
            return

        self._append_chat("You", user_text)
        response = self.bot.get_response(user_text)
        self._append_chat("Buddy", response)
        self._add_history_entry(user_text, response)

        self.user_input.delete(0, tk.END)
        self.status_label.configure(text="Message sent. Select a history entry to view details.")

    def run(self) -> None:
        self.root.mainloop()
