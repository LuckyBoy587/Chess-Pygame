from pygame import Surface

from classes.bishop import Bishop, BlackBishop, WhiteBishop
from classes.constants import POSSIBLE_MOVE_COLOR, CAPTURE_MOVE_COLOR, SELECTED_PIECE_COLOR, PIECE_SIZE
from classes.king import BlackKing, WhiteKing, King
from classes.knight import BlackKnight, WhiteKnight, Knight
from classes.move import Move
from classes.pawn import BlackPawn, WhitePawn, Pawn, is_at_base
from classes.queen import BlackQueen, WhiteQueen, Queen
from classes.rook import BlackRook, WhiteRook, Rook
from classes.utils import PieceDrawer, highlight_cell


class Game:
    def __init__(self):
        self.drawer = PieceDrawer()
        self.board: list[list[Bishop | Knight | Rook | Queen | King | Pawn | None]] = []
        self.initialize_board()
        self.selected_position: tuple[int, int] | None = None
        self.possible_moves = []
        self.current_player = "white"

    def toggle_player(self):
        self.current_player = "white" if self.current_player == "black" else "black"

    def initialize_board(self):
        self.board.append(
            [BlackRook(), BlackKnight(), BlackBishop(), BlackQueen(), BlackKing(),
             BlackBishop(), BlackKnight(), BlackRook()])
        self.board.append([BlackPawn() for _ in range(8)])
        self.board.append([None for _ in range(8)])
        self.board.append([None for _ in range(8)])
        self.board.append([None for _ in range(8)])
        self.board.append([None for _ in range(8)])
        self.board.append([WhitePawn() for _ in range(8)])
        self.board.append(
            [WhiteRook(), WhiteKnight(), WhiteBishop(), WhiteQueen(), WhiteKing(),
             WhiteBishop(), WhiteKnight(), WhiteRook()])

    def draw_board(self, window: Surface):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None:
                    self.drawer.draw(window, (col * PIECE_SIZE, row * PIECE_SIZE), piece.image_index)

        for cell in self.possible_moves:
            if self.board[cell[0]][cell[1]] is None:
                highlight_cell(window, cell, POSSIBLE_MOVE_COLOR)
            else:
                highlight_cell(window, cell, CAPTURE_MOVE_COLOR)
        if self.selected_position is not None:
            highlight_cell(window, self.selected_position, SELECTED_PIECE_COLOR)

    def get_selected_piece(self):
        return self.get_piece_at(self.selected_position)

    def get_piece_at(self, pos: tuple[int, int]):
        return self.board[pos[0]][pos[1]]

    def handle_mouse_click(self, i: int, j: int):
        if self.board[i][j] is not None and self.board[i][j].color == self.current_player:
            self.possible_moves = []
            self.selected_position = (i, j)
            for (i, j) in self.get_possible_moves(i, j):
                move = Move(self.selected_position, (i, j), self.get_selected_piece(), self.get_piece_at((i, j)))
                self.make_move(move)
                if not self.is_king_in_check(self.current_player):
                    self.possible_moves.append((i, j))
                self.unmake_move(move)
        else:
            if (i, j) in self.possible_moves:
                move = Move(self.selected_position, (i, j), self.get_selected_piece(), self.get_piece_at((i, j)))
                self.make_move(move)
                self.toggle_player()
            self.selected_position = None
            self.possible_moves = []

    def make_move(self, move: Move):
        from_i, from_j = move.from_pos
        to_i, to_j = move.to_pos
        self.board[to_i][to_j] = self.board[from_i][from_j]
        self.board[from_i][from_j] = None

    def unmake_move(self, move: Move):
        from_i, from_j = move.from_pos
        to_i, to_j = move.to_pos
        self.board[from_i][from_j] = self.board[to_i][to_j]
        self.board[to_i][to_j] = move.captured_piece

    def is_king_in_check(self, color: str) -> bool:
        king_pos = self.find_king_position(color)
        opponent_color = "black" if color == "white" else "white"
        opponent_moves = self.get_possible_moves_of_player(opponent_color)
        return king_pos in opponent_moves

    def get_possible_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        if isinstance(self.board[i][j], Bishop):
            return self.get_bishop_moves(i, j)
        if isinstance(self.board[i][j], Pawn):
            return self.get_pawn_moves(i, j)
        if isinstance(self.board[i][j], Rook):
            return self.get_rook_moves(i, j)
        if isinstance(self.board[i][j], Knight):
            return self.get_knight_moves(i, j)
        if isinstance(self.board[i][j], Queen):
            return self.get_queen_moves(i, j)
        if isinstance(self.board[i][j], King):
            return self.get_king_moves(i, j)
        return []

    def get_bishop_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        pos = []
        curr_i = i - 1
        curr_j = j - 1
        while curr_i >= 0 and curr_j >= 0 and self.board[curr_i][curr_j] is None:
            pos.append((curr_i, curr_j))
            curr_i -= 1
            curr_j -= 1
        else:
            if curr_i >= 0 and curr_j >= 0 and self.board[curr_i][curr_j].color != self.board[i][j].color:
                pos.append((curr_i, curr_j))

        curr_i = i - 1
        curr_j = j + 1
        while curr_i >= 0 and curr_j < 8 and self.board[curr_i][curr_j] is None:
            pos.append((curr_i, curr_j))
            curr_i -= 1
            curr_j += 1
        else:
            if curr_i >= 0 and curr_j < 8 and self.board[curr_i][curr_j].color != self.board[i][j].color:
                pos.append((curr_i, curr_j))

        curr_i = i + 1
        curr_j = j - 1
        while curr_i < 8 and curr_j >= 0 and self.board[curr_i][curr_j] is None:
            pos.append((curr_i, curr_j))
            curr_i += 1
            curr_j -= 1
        else:
            if curr_i < 8 and curr_j >= 0 and self.board[curr_i][curr_j].color != self.board[i][j].color:
                pos.append((curr_i, curr_j))

        curr_i = i + 1
        curr_j = j + 1
        while curr_i < 8 and curr_j < 8 and self.board[curr_i][curr_j] is None:
            pos.append((curr_i, curr_j))
            curr_i += 1
            curr_j += 1
        else:
            if curr_i < 8 and curr_j < 8 and self.board[curr_i][curr_j].color != self.board[i][j].color:
                pos.append((curr_i, curr_j))

        return pos

    def get_pawn_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        pos = []
        pawn: Pawn = self.board[i][j]
        if self.board[i + pawn.direction][j] is None:
            pos.append((i + pawn.direction, j))

        if j > 0 and self.board[i + pawn.direction][j - 1] is not None and self.board[i + pawn.direction][
            j - 1].color != self.board[i][j].color:
            pos.append((i + pawn.direction, j - 1))

        if j < 7 and self.board[i + pawn.direction][j + 1] is not None and self.board[i + pawn.direction][
            j + 1].color != self.board[i][j].color:
            pos.append((i + pawn.direction, j + 1))

        if is_at_base(i, self.current_player) and self.board[i + pawn.direction * 2][j] is None:
            pos.append((i + pawn.direction * 2, j))

        return pos

    def get_rook_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        pos = []
        curr_i, curr_j = i - 1, j
        while curr_i >= 0 and self.board[curr_i][curr_j] is None:
            pos.append((curr_i, curr_j))
            curr_i -= 1
        else:
            if curr_i >= 0 and self.board[curr_i][curr_j].color != self.board[i][j].color:
                pos.append((curr_i, curr_j))

        curr_i, curr_j = i + 1, j
        while curr_i < 8 and self.board[curr_i][curr_j] is None:
            pos.append((curr_i, curr_j))
            curr_i += 1
        else:
            if curr_i < 8 and self.board[curr_i][curr_j].color != self.board[i][j].color:
                pos.append((curr_i, curr_j))

        curr_i, curr_j = i, j - 1
        while curr_j >= 0 and self.board[curr_i][curr_j] is None:
            pos.append((curr_i, curr_j))
            curr_j -= 1
        else:
            if curr_j >= 0 and self.board[curr_i][curr_j].color != self.board[i][j].color:
                pos.append((curr_i, curr_j))

        curr_i, curr_j = i, j + 1
        while curr_j < 8 and self.board[curr_i][curr_j] is None:
            pos.append((curr_i, curr_j))
            curr_j += 1
        else:
            if curr_j < 8 and self.board[curr_i][curr_j].color != self.board[i][j].color:
                pos.append((curr_i, curr_j))

        return pos

    def get_knight_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        pos = []
        for i_offset, j_offset in [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]:
            new_i, new_j = i + i_offset, j + j_offset
            if 0 <= new_i < 8 and 0 <= new_j < 8 and (
                    self.board[new_i][new_j] is None or self.board[new_i][new_j].color != self.board[i][j].color):
                pos.append((new_i, new_j))
        return pos

    def get_queen_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        return self.get_rook_moves(i, j) + self.get_bishop_moves(i, j)

    def get_king_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        pos = []
        for i_offset in range(-1, 2):
            for j_offset in range(-1, 2):
                new_i, new_j = i + i_offset, j + j_offset
                if 0 <= new_i < 8 and 0 <= new_j < 8 and (
                        self.board[new_i][new_j] is None or self.board[new_i][new_j].color != self.board[i][j].color):
                    pos.append((new_i, new_j))
        return pos

    def get_possible_moves_of_player(self, color: str) -> set[tuple[int, int]]:
        res = set()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None and self.board[i][j].color == color:
                    res.update(self.get_possible_moves(i, j))
        return res

    def find_king_position(self, color: str) -> tuple[int, int]:
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None and self.board[i][j].color == color and isinstance(self.board[i][j], King):
                    return i, j

