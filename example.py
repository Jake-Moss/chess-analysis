import chess
import chess.pgn
import chessHeatmap

pgn = chessHeatmap.load_pgn("dad.pgn")

filename = chessHeatmap.lost_piece_plot(pgn, [chess.ROOK])
filename
