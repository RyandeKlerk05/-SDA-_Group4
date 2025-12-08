'''
This file implements the Mann-Whitney U test for sub-question 4.
'''

from numpy import sqrt


class MannWhitney:
    def __init__(self, batch_fast, batch_slow):
        '''
        Initialization of Mann-Whitney U test.

        Args:
        - self: The current instance of the class.
        - batch_fast: The list with fast uptake countries, consists of 3-tuples
            like:
            ('fast uptake', social_media_users_change, mental_health_change)
        - batch_slow: The list with slow uptake countries, consists of 3-tuples
            like:
            ('slow uptake', social_media_users_change, mental_health_change)
        '''
        self.fast_batch = batch_fast
        self.slow_batch = batch_slow

    def SortMentalHealthScores(self):
        batches_combined = self.fast_batch + self.slow_batch

        # sorts by mental health score
        batches_combined.sort(key=lambda x: x[2])
        return batches_combined

    def CalculateRanks(self):
        batches = self.SortMentalHealthScores()
        ranked = []

        for i in range(len(batches)):
            score = batches[i][2]

            j = i

            while j < len(batches) and batches[j][2] == score:
                j += 1
            avg_rank = (i + 1 + j) / 2

            # Assigning the same rank to all the tied entries
            for k in range(i, j):
                country_data = batches[k]
                tuple_data = (country_data[0], country_data[1], country_data[2], avg_rank)
            ranked.append((tuple_data))

        return ranked

    def SplitCombinedBatches(self):
        ''' Splits the combined batches again after calculating the ranks. '''
        ranked = self.CalculateRanks()
        batch_fast = [x for x in ranked if x[0] == 'fast uptake']
        batch_slow = [x for x in ranked if x[0] == 'slow uptake']
        return batch_fast, batch_slow

    def GetSumRanks(self):
        '''
        Calculates the sum of the ranks for both the fast uptake (R1) and slow
        uptake countries (R2).
        '''
        batch_fast, batch_slow = self.SplitCombinedBatches()
        R1 = sum(x[-1] for x in batch_fast)
        R2 = sum(x[-1] for x in batch_slow)

        return R1, R2

    def GetLengths(self):
        n1 = len(self.fast_batch)
        n2 = len(self.slow_batch)
        return n1, n2

    def CalculateU(self):
        ''' Calculates the U-statistics U1 and U2.'''
        n1, n2 = self.GetLengths()

        R1, R2 = self.GetSumRanks()
        U1 = (n1 * n2) + ((n1 * (n1 + 1)) / 2) - R1
        U2 = (n1 * n2) + ((n2 * (n2 + 1)) / 2) - R2

        return U1, U2

    def CalculateZScore(self, U1, U2):
        ''' Calculates the Z-score  '''
        min_U = min(U1, U2)
        mean = self.CalculateMean()
        std = self.CalculateSTD()
        z_score = (min_U - mean) / std
        return z_score

    def CalculateMean(self):
        n1, n2 = self.GetLengths()
        return (n1 * n2) / 2

    def CalculateSTD(self):
        n1, n2 = self.GetLengths()
        std = sqrt((n1 * n2 * (n1 + n2 + 1)) / 12)
        return std
