import tkinter as tk

# Colors for neon effect
BOARD_COLOR = "#00f2ff"
X_COLOR = "#61f8ff"
O_COLOR = "#ff217c"
WIN_LINE_COLOR = "#ff416c"
BG_COLOR = "#1b143a"

CELL_SIZE = 140
GRID_SIZE = 3
GLOW = 7  # Glow thickness

class NeonTicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neon Tic Tac Toe")
        self.configure(bg=BG_COLOR)
        self.turn_label = tk.Label(self, text="", font=("Arial", 22, "bold"), bg=BG_COLOR, fg="white")
        self.turn_label.pack(pady=(18, 8))
        self.canvas = tk.Canvas(self, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        self.reset_button = tk.Button(self, text="Reset", command=self.reset_game, font=("Arial", 16, "bold"), bg=WIN_LINE_COLOR, fg="white", activebackground="#ff90af")
        self.reset_button.pack(pady=(10, 20))
        self.board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.turn = "X"
        self.game_over = False
        self.winning_cells = None
        self.update_turn_label()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

    def update_turn_label(self):
        if self.game_over:
            winner, _ = self.check_winner()
            if winner:
                self.turn_label.config(text=f"Player {winner} wins!", fg=WIN_LINE_COLOR)
            else:
                self.turn_label.config(text=f"It's a tie!", fg=WIN_LINE_COLOR)
        else:
            self.turn_label.config(text=f"Player {self.turn}'s turn", fg="#fff")

    def reset_game(self):
        self.board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.turn = "X"
        self.game_over = False
        self.winning_cells = None
        self.canvas.delete("all")
        self.update_turn_label()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        # Draw neon grid
        for i in range(1, GRID_SIZE):
            for g in range(GLOW, 0, -1):
                self.canvas.create_line(
                    i*CELL_SIZE, 0, i*CELL_SIZE, CELL_SIZE*GRID_SIZE,
                    fill=BOARD_COLOR, width=10+g*2, stipple='gray25'
                )
                self.canvas.create_line(
                    0, i*CELL_SIZE, CELL_SIZE*GRID_SIZE, i*CELL_SIZE,
                    fill=BOARD_COLOR, width=10+g*2, stipple='gray25'
                )
        # Draw marks
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cx = c*CELL_SIZE + CELL_SIZE//2
                cy = r*CELL_SIZE + CELL_SIZE//2
                if self.board[r][c] == "X":
                    self.draw_x(cx, cy)
                elif self.board[r][c] == "O":
                    self.draw_o(cx, cy)
        # Draw win line if game over and there's a winner
        if self.game_over and self.winning_cells:
            self.draw_win_line(self.winning_cells)

    def draw_x(self, x, y):
        size = 40
        for g in range(GLOW, -1, -1):
            self.canvas.create_line(
                x-size-g, y-size-g, x+size+g, y+size+g,
                fill=X_COLOR, width=9+g*2, capstyle=tk.ROUND
            )
            self.canvas.create_line(
                x-size-g, y+size+g, x+size+g, y-size-g,
                fill=X_COLOR, width=9+g*2, capstyle=tk.ROUND
            )

    def draw_o(self, x, y):
        r = 47
        for g in range(GLOW, -1, -1):
            self.canvas.create_oval(
                x-r-g, y-r-g, x+r+g, y+r+g,
                outline=O_COLOR, width=9+g*2
            )

    def draw_win_line(self, cells):
        (r1, c1), (r2, c2) = cells
        x1 = c1*CELL_SIZE + CELL_SIZE//2
        y1 = r1*CELL_SIZE + CELL_SIZE//2
        x2 = c2*CELL_SIZE + CELL_SIZE//2
        y2 = r2*CELL_SIZE + CELL_SIZE//2
        for g in range(GLOW+3, 0, -1):
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=WIN_LINE_COLOR, width=22+g*2, capstyle=tk.ROUND, stipple='gray25'
            )
        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=WIN_LINE_COLOR, width=18, capstyle=tk.ROUND
        )

    def handle_click(self, event):
        if self.game_over:
            return
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == "":
            self.board[r][c] = self.turn
            winner, cells = self.check_winner()
            if winner:
                self.game_over = True
                self.winning_cells = cells
            elif all(all(cell != "" for cell in row) for row in self.board):
                self.game_over = True
                self.winning_cells = None
            else:
                self.turn = "O" if self.turn == "X" else "X"
            self.update_turn_label()
            self.draw_board()

    def check_winner(self):
        b = self.board
        N = GRID_SIZE
        for i in range(N):
            if b[i][0] and all(b[i][j] == b[i][0] for j in range(N)):
                return b[i][0], ((i, 0), (i, N-1))
            if b[0][i] and all(b[j][i] == b[0][i] for j in range(N)):
                return b[0][i], ((0, i), (N-1, i))
        if b[0][0] and all(b[j][j] == b[0][0] for j in range(N)):
            return b[0][0], ((0, 0), (N-1, N-1))
        if b[0][N-1] and all(b[j][N-1-j] == b[0][N-1] for j in range(N)):
            return b[0][N-1], ((0, N-1), (N-1, 0))
        return None, None

if __name__ == "__main__":
    app = NeonTicTacToe()
    app.mainloop()
