import hashlib
import time

class Move:
    NONE = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __init__(self, commitment, move=0):
        self.commitment = commitment
        self.move = move

    @classmethod
    def move_to_stc(cls, move):
        return {
            cls.NONE: 'None',
            cls.ROCK: 'Rock',
            cls.PAPER: 'Paper',
            cls.SCISSORS: 'Scissors'
        }[move]
    
class Challenge:
    def __init__(self, creator_address, _id, commitment):
        self.creator_address = creator_address
        self.opponent_address = None
        
        self.commitments = {
            self.creator_address: Move(commitment),
        }
        
        self.id = _id
        
        self.winner_address = None
        self.created_at = time.time()

    def add_commitment(self, address, commitment):
        self.opponent_address = address
        self.commitments[address] = Move(commitment)
    
    def reveal(self, address, move, nonce):
        if self.has_opponent_commited(self):
            raise Exception('Opponent has not committed yet')

        reveal_hash = Challenge.generate_hash(nonce + move)
        commitd_move = self.commitments.get(address)
        if commitd_move.commitment != reveal_hash:
            raise Exception('Move does not match commitment')
        
        self.commitments[address].move = int(move)

    @staticmethod    
    def generate_hash(input):
        return hashlib.sha256(input.encode()).hexdigest()
    
    def both_revealed(self):
        opponent_move = self.commitments[self.opponent_address].move
        creator_move = self.commitments[self.creator_address].move
        return opponent_move != Move.NONE and creator_move != Move.NONE
    
    def has_opponent_commited(self):
        return self.commitments.get(self.opponent_address) != None
    
    def evaluate_winner(self):
        opponent_move = self.commitments[self.opponent_address].move
        creator_move = self.commitments[self.creator_address].move
    
        if creator_move == Move.ROCK and opponent_move == Move.SCISSORS:
            self.winner_address = self.creator_address
        elif creator_move == Move.PAPER and opponent_move == Move.ROCK:
            self.winner_address = self.creator_address
        elif creator_move == Move.SCISSORS and opponent_move == Move.PAPER:
            self.winner_address = self.creator_address
        elif creator_move == opponent_move:
            self.winner_address = None
        else:
            self.winner_address = self.opponent_address