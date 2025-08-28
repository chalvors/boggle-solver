import sys
sys.path.insert(1, '../')
from solve import Solve
import unittest


class TestSolve(unittest.TestCase):

    def test_found_words(self):

        test_board = [
            ['T', 'U', 'R', 'N'], 
            ['A', 'A', 'S', 'I'], 
            ['E', 'P', 'I', 'U'], 
            ['B', 'E', 'A', 'R']
        ]
        test_board_size = len(test_board)
        expected_words = ['RAISIN', 'TARSIA', 'ARIAS', 'ATAPS', 'AURAE', 'AURAS', 'AURIS', 'BEARS', 'BEAUS', 'BEAUT', 'BEEPS', 'EARNS', 'PAISA', 'PARIS', 'PEARS', 'RAIAS', 'RIATA', 'RUINS', 'SARIN', 'SPEAR', 'SPEIR', 'TAPAS', 'TAPIR', 'TAPIS', 'TARNS', 'TARSI', 'TURNS', 'URAEI', 'URSAE', 'ARIA', 'ATAP', 'AURA', 'BEAR', 'BEAT', 'BEAU', 'BEEP', 'EARN', 'EARS', 'NISI', 'PAIR', 'PARS', 'PEAR', 'PEAS', 'PEAT', 'PIAS', 'RAIA', 'RAPE', 'RAPS', 'RASP', 'RIAS', 'RINS', 'RIPE', 'RIPS', 'RUIN', 'SARI', 'SIPE', 'SPAE', 'SPAR', 'SPAT', 'SURA', 'TAPA', 'TAPE', 'TAPS', 'TARN', 'TARS', 'TAUS', 'TURN', 'URNS', 'URSA', 'UTAS', 'AAS', 'AIR', 'AIS', 'APE', 'ARS', 'ASP', 'BEE', 'EAR', 'EAT', 'EAU', 'INS', 'PAR', 'PAS', 'PAT', 'PEA', 'PEE', 'PIA', 'PIE', 'PIS', 'PIU', 'PSI', 'RAP', 'RAS', 'RAT', 'RIA', 'RIN', 'RIP', 'RUT', 'SAE', 'SAP', 'SAT', 'SAU', 'SIN', 'SIP', 'SIR', 'SPA', 'SRI', 'TAE', 'TAP', 'TAR', 'TAS', 'TAU', 'URN', 'UTA']

        solve = Solve('../valid_words.json')
        found_words = solve.find_words(test_board, test_board_size)

        self.assertEqual(found_words, expected_words)


if __name__ == '__main__':
    unittest.main()