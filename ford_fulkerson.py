

class GFG:
    def __init__(self, adj, size):

        # residual graph
        graph = [[1 if j in adj[i] else 0 for j in range(size, 2*size)] for i in range(size)]
        self.size = size
        self.graph = graph
        self.ppl = len(graph)
        self.jobs = len(graph[0])

    # A DFS based recursive function
    # that returns true if a matching
    # for vertex u is possible
    def bpm(self, u, matchR, seen):

        # Try every job one by one
        for v in range(self.jobs):

            # If applicant u is interested
            # in job v and v is not seen
            if self.graph[u][v] and seen[v] == False:

                # Mark v as visited
                seen[v] = True

                '''If job 'v' is not assigned to
                   an applicant OR previously assigned 
                   applicant for job v (which is matchR[v]) 
                   has an alternate job available. 
                   Since v is marked as visited in the 
                   above line, matchR[v]  in the following
                   recursive call will not get job 'v' again'''
                if matchR[v] == -1 or self.bpm(matchR[v],
                                               matchR, seen):
                    matchR[v] = u
                    return True
        return False

    # Returns maximum number of matching
    def maxBPM(self):
        '''An array to keep track of the
           applicants assigned to jobs.
           The value of matchR[i] is the
           applicant number assigned to job i,
           the value -1 indicates nobody is assigned.'''
        matchR = [-1] * self.jobs

        # Count of jobs assigned to applicants
        result = 0
        for i in range(self.ppl):

            # Mark all jobs as not seen for next applicant.
            seen = [False] * self.jobs

            # Find if the applicant 'u' can get a job
            if self.bpm(i, matchR, seen):
                result += 1
        return matchR

    def maximum_matching(self):
        matchR = self.maxBPM()
        matching = {}
        for i, value in enumerate(matchR):
            if value != -1:
                matching[value] = i + self.size
        return matching
