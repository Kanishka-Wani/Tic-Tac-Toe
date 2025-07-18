import tkinter as tk
from itertools import cycle
from tkinter import messagebox

def play_beep():
    print('\a')  # Cross-platform beep (may not be audible on all OS)

class NeonTicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.configure(bg="#0f0f0f")
        self.resizable(False, False)
        self.board_size = 3
        self.scores = {"X": 0, "O": 0}
        self.players = cycle([("X", "#00f2ff"), ("O", "#ff00ff")])  # Neon cyan & pink
        self.current_player, self.current_color = next(self.players)
        self.buttons = {}
        self._create_widgets()
        self._reset_board()
        self._center_window()

    def _create_widgets(self):
        self.title_label = tk.Label(
            self,
            text="Neon Tic Tac Toe",
            font=("Consolas", 18, "bold"),
            bg="#0f0f0f",
            fg="#feca57"
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(10, 0))

        self.score_label = tk.Label(
            self,
            text=self._get_score_text(),
            font=("Consolas", 12, "bold"),
            bg="#0f0f0f",
            fg="#39ff14"
        )
        self.score_label.grid(row=1, column=0, columnspan=3)

        self.status_label = tk.Label(
            self,
            text=f"Player {self.current_player}'s Turn",
            font=("Consolas", 14, "bold"),
            bg="#0f0f0f",
            fg="#00ffff",
            pady=6
        )
        self.status_label.grid(row=2, column=0, columnspan=3)

        for row in range(self.board_size):
            for col in range(self.board_size):
                btn = tk.Button(
                    self,
                    text="",
                    font=("Consolas", 28, "bold"),
                    width=4,
                    height=1,
                    bg="#1c1c1c",
                    fg="white",
                    activebackground="#333",
                    relief="flat",
                    bd=2,
                    highlightthickness=0,
                    cursor="hand2",
                    command=lambda row=row, col=col: self._on_click(row, col)
                )
                btn.grid(row=row + 3, column=col, padx=4, pady=4)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2a2a2a"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1c1c1c") if b["state"] == tk.NORMAL else b["bg"])
                self.buttons[(row, col)] = btn

        restart_btn = tk.Button(
            self,
            text="🔁 Restart",
            font=("Consolas", 12, "bold"),
            command=self._reset_board,
            bg="#ff00ff",
            fg="black",
            activebackground="#cc00cc",
            relief="flat",
            width=14,
            cursor="hand2",
            pady=4
        )
        restart_btn.grid(row=6, column=0, columnspan=3, pady=10)

    def _get_score_text(self):
        return f"🏆 X: {self.scores['X']} | O: {self.scores['O']}"

    def _reset_board(self):
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        for btn in self.buttons.values():
            btn.config(text="", state=tk.NORMAL, bg="#1c1c1c", fg="white")
        self.players = cycle([("X", "#00f2ff"), ("O", "#ff00ff")])
        self.current_player, self.current_color = next(self.players)
        self.status_label.config(text=f"Player {self.current_player}'s Turn")

    def _on_click(self, row, col):
        btn = self.buttons[(row, col)]
        if btn["text"] == "" and not self._check_winner():
            play_beep()
            btn.config(text=self.current_player, fg=self.current_color)
            self.board[row][col] = self.current_player
            if self._check_winner():
                self.scores[self.current_player] += 1
                self.status_label.config(text=f"🎉 Player {self.current_player} Wins!")
                self._highlight_winner()
                self.score_label.config(text=self._get_score_text())
                messagebox.showinfo("Game Over", f"Player {self.current_player} Wins!")
            elif self._is_tie():
                self.status_label.config(text="🤝 It's a Tie!")
                messagebox.showinfo("Game Over", "It's a Tie!")
            else:
                self.current_player, self.current_color = next(self.players)
                self.status_label.config(text=f"Player {self.current_player}'s Turn")

    def _check_winner(self):
        b = self.board
        for i in range(self.board_size):
            if b[i][0] == b[i][1] == b[i][2] != "":
                self.winning_combo = [(i, 0), (i, 1), (i, 2)]
                return True
            if b[0][i] == b[1][i] == b[2][i] != "":
                self.winning_combo = [(0, i), (1, i), (2, i)]
                return True
        if b[0][0] == b[1][1] == b[2][2] != "":
            self.winning_combo = [(0, 0), (1, 1), (2, 2)]
            return True
        if b[0][2] == b[1][1] == b[2][0] != "":
            self.winning_combo = [(0, 2), (1, 1), (2, 0)]
            return True
        return False

    def _highlight_winner(self):
        for row, col in self.winning_combo:
            self.buttons[(row, col)].config(bg="#39ff14", fg="#000")
        self._disable_all_buttons()

    def _is_tie(self):
        return all(cell != "" for row in self.board for cell in row) and not self._check_winner()

    def _disable_all_buttons(self):
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

if __name__ == "__main__":
    app = NeonTicTacToe()
    app.mainloop()
