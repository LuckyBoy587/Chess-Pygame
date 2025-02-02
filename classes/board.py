from typing import List, Set, Optional
from classes.bishop import Bishop, BlackBishop, WhiteBishop
from classes.king import BlackKing, WhiteKing, King
from classes.knight import BlackKnight, WhiteKnight, Knight
from classes.pawn import BlackPawn, WhitePawn, Pawn, is_at_base
from classes.queen import BlackQueen, WhiteQueen, Queen
from classes.rook import BlackRook, WhiteRook, Rook
from classes.utils import Position, CastlingMove


class Board:
    def __init__(self):
        self.board: List[List[Optional[Bishop | Knight | Rook | Queen | King | Pawn]]] = []
        self.initialize_board()

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

    def get_piece_at(self, pos: Position):
        return self.board[pos.i][pos.j]

    def set_piece_at(self, pos: Position, piece):
        self.board[pos.i][pos.j] = piece

    def is_king_in_check(self, color: str) -> bool:
        king_pos = self.find_king_position(color)
        opponent_color = "black" if color == "white" else "white"
        opponent_moves = self.get_possible_moves_of_player(opponent_color)
        return king_pos in opponent_moves

    def find_king_position(self, color: str) -> Position:
        for i in range(8):
            for j in range(8):
                pos = Position(i, j)
                piece = self.get_piece_at(pos)
                if piece is not None and piece.color == color and isinstance(piece, King):
                    return pos

    def get_bishop_moves(self, pos: Position) -> List[Position]:
        i, j = pos.i, pos.j
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
        for di, dj in directions:
            curr_i, curr_j = i + di, j + dj
            while 0 <= curr_i < 8 and 0 <= curr_j < 8:
                target_pos = Position(curr_i, curr_j)
                piece = self.get_piece_at(target_pos)
                if piece is None:
                    moves.append(target_pos)
                else:
                    if piece.color != self.get_piece_at(pos).color:
                        moves.append(target_pos)
                    break
                curr_i += di
                curr_j += dj
        return moves

    def get_pawn_moves(self, pos: Position) -> List[Position]:
        i, j = pos.i, pos.j
        pawn: Pawn = self.get_piece_at(pos)
        moves = []
        direction = pawn.direction

        forward_pos = Position(i + direction, j)
        if self.get_piece_at(forward_pos) is None:
            moves.append(forward_pos)
            if is_at_base(i, pawn.color):
                double_forward_pos = Position(i + 2 * direction, j)
                if self.get_piece_at(double_forward_pos) is None:
                    moves.append(double_forward_pos)

        for dj in [-1, 1]:
            capture_pos = Position(i + direction, j + dj)
            if 0 <= capture_pos.j < 8:
                piece = self.get_piece_at(capture_pos)
                if piece is not None and piece.color != pawn.color:
                    moves.append(capture_pos)

        return moves

    def get_rook_moves(self, pos: Position) -> List[Position]:
        i, j = pos.i, pos.j
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in directions:
            curr_i, curr_j = i + di, j + dj
            while 0 <= curr_i < 8 and 0 <= curr_j < 8:
                target_pos = Position(curr_i, curr_j)
                piece = self.get_piece_at(target_pos)
                if piece is None:
                    moves.append(target_pos)
                else:
                    if piece.color != self.get_piece_at(pos).color:
                        moves.append(target_pos)
                    break
                curr_i += di
                curr_j += dj
        return moves

    def get_knight_moves(self, pos: Position) -> List[Position]:
        i, j = pos.i, pos.j
        moves = []
        offsets = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
        for di, dj in offsets:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < 8 and 0 <= new_j < 8:
                target_pos = Position(new_i, new_j)
                piece = self.get_piece_at(target_pos)
                if piece is None or piece.color != self.get_piece_at(pos).color:
                    moves.append(target_pos)
        return moves

    def get_queen_moves(self, pos: Position) -> List[Position]:
        return self.get_rook_moves(pos) + self.get_bishop_moves(pos)

    def get_king_moves(self, pos: Position) -> List[Position]:
        i, j = pos.i, pos.j
        moves = []
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                new_i, new_j = i + di, j + dj
                if 0 <= new_i < 8 and 0 <= new_j < 8:
                    target_pos = Position(new_i, new_j)
                    piece = self.get_piece_at(target_pos)
                    if piece is None or piece.color != self.get_piece_at(pos).color:
                        moves.append(target_pos)
        return moves

    def get_possible_moves(self, pos: Position) -> List[Position]:
        piece = self.get_piece_at(pos)
        if isinstance(piece, Bishop):
            return self.get_bishop_moves(pos)
        if isinstance(piece, Pawn):
            return self.get_pawn_moves(pos)
        if isinstance(piece, Rook):
            return self.get_rook_moves(pos)
        if isinstance(piece, Knight):
            return self.get_knight_moves(pos)
        if isinstance(piece, Queen):
            return self.get_queen_moves(pos)
        if isinstance(piece, King):
            return self.get_king_moves(pos)
        return []

    def get_possible_moves_of_player(self, color: str) -> Set[Position]:
        res = set()
        for i in range(8):
            for j in range(8):
                pos = Position(i, j)
                piece = self.get_piece_at(pos)
                if piece is not None and piece.color == color:
                    res.update(self.get_possible_moves(pos))
        return res

    def get_castling_moves(self, color: str) -> List[CastlingMove]:
        king_pos = Position(0, 4) if color == "black" else Position(7, 4)
        king = self.get_piece_at(king_pos)
        castling_moves = []
        if not isinstance(king, King) or king.has_moved:
            return castling_moves

        rook_positions = [Position(king_pos.i, 0), Position(king_pos.i, 7)]
        opponent_color = "white" if color == "black" else "black"
        opponent_moves = self.get_possible_moves_of_player(opponent_color)

        for rook_pos in rook_positions:
            rook = self.get_piece_at(rook_pos)
            if not isinstance(rook, Rook) or rook.has_moved:
                continue

            direction = -1 if rook_pos.j < king_pos.j else 1
            start_j = king_pos.j + direction
            end_j = rook_pos.j

            is_path_clear = True
            while start_j != end_j:
                if self.get_piece_at(Position(king_pos.i, start_j)) is not None or Position(king_pos.i, start_j) in opponent_moves:
                    is_path_clear = False
                    break
                start_j += direction

            if is_path_clear:
                castling_moves.append(CastlingMove(king_pos, direction))

        return castling_moves

    def do_castling(self, move: CastlingMove):
        self.set_piece_at(move.king_to_pos, self.get_piece_at(move.king_from_pos))
        self.set_piece_at(move.rook_to_pos, self.get_piece_at(move.rook_from_pos))
        self.set_piece_at(move.king_from_pos, None)
        self.set_piece_at(move.rook_from_pos, None)
