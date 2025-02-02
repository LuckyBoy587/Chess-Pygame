from typing import List, Optional

from pygame import Surface

from classes.board import Board
from classes.king import King
from classes.move import Move
from classes.rook import Rook
from classes.utils import PieceDrawer, highlight_cell, Position, CastlingMove
from classes.constants import POSSIBLE_MOVE_COLOR, CAPTURE_MOVE_COLOR, SELECTED_PIECE_COLOR


class Game:
    def __init__(self):
        self.drawer = PieceDrawer()
        self.board = Board()
        self.selected_position: Optional[Position] = None
        self.possible_moves: List[Position] = []
        self.special_moves: list[CastlingMove] = []
        self.current_player = "white"

    def toggle_player(self):
        self.current_player = "white" if self.current_player == "black" else "black"

    def draw_board(self, window: Surface):
        for i in range(8):
            for j in range(8):
                piece = self.board.get_piece_at(Position(i, j))
                if piece is not None:
                    self.drawer.draw(window, Position(i, j), piece.image_index)

        for cell in self.possible_moves:
            if self.board.get_piece_at(cell) is None:
                highlight_cell(window, cell, POSSIBLE_MOVE_COLOR)
            else:
                highlight_cell(window, cell, CAPTURE_MOVE_COLOR)

        for move in self.special_moves:
            if isinstance(move, CastlingMove):
                highlight_cell(window, move.king_to_pos, POSSIBLE_MOVE_COLOR)
        if self.selected_position is not None:
            highlight_cell(window, self.selected_position, SELECTED_PIECE_COLOR)

    def handle_mouse_click(self, clicked_position: Position):
        clicked_piece = self.board.get_piece_at(clicked_position)
        if clicked_piece is not None and clicked_piece.color == self.current_player:
            self.possible_moves = []
            self.special_moves = []
            self.selected_position = clicked_position
            for move in self.board.get_possible_moves(clicked_position):
                move_position = Position(move.i, move.j)
                move = Move(self.selected_position, move_position, self.board.get_piece_at(self.selected_position), self.board.get_piece_at(move_position))
                self.board.set_piece_at(move_position, self.board.get_piece_at(self.selected_position))
                self.board.set_piece_at(self.selected_position, None)
                if not self.board.is_king_in_check(self.current_player):
                    self.possible_moves.append(move_position)
                self.board.set_piece_at(self.selected_position, self.board.get_piece_at(move_position))
                self.board.set_piece_at(move_position, move.captured_piece)
            if isinstance(clicked_piece, King):
                self.special_moves = self.board.get_castling_moves(self.current_player)
        else:
            if clicked_position in self.possible_moves:
                piece = self.board.get_piece_at(self.selected_position)
                if isinstance(piece, King) or isinstance(piece, Rook):
                    piece.has_moved = True
                self.board.set_piece_at(clicked_position, self.board.get_piece_at(self.selected_position))
                self.board.set_piece_at(self.selected_position, None)
                self.toggle_player()
            else:
                for move in self.special_moves:
                    if move == clicked_position:
                        if isinstance(move, CastlingMove):
                            self.board.do_castling(move)
                            self.toggle_player()
                            break
            self.selected_position = None
            self.possible_moves = []
            self.special_moves = []