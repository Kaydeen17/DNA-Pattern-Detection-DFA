class GeneticAnalyzer:
    def __init__(self):
        self.state = "Q0"
        self.position = None   # current position in the sequence
        #booleans for whether a genetic marker is detected
        self.start_codon_detected = False
        self.cancer_detected = False
        self.huntingtons_detected = False

        # index positions of detected sequences
        self.start_codon_index = None
        self.cancer_index = None
        self.huntingtons_index = None
        self.sequence_cancer = None
        self.sequence_huntingtons = None

    # transitions for the dfa using a nested dictionary where outer keys represent states
    # inner keys represent letters and inner values specify the next state.
    TRANSITIONS = {
        #start codon detection from q0-q3
        "Q0": {"A": "Q1"},
        "Q1": {"T": "Q2", "C": "Q0", "G": "Q0"},
        "Q2": {"G": "Q3", "A": "Q1", "C": "Q0", "T": "Q0"},
        #start codon detected when q2 transitions to q3 on a G
        # start codon must be detectd for it to check for huntingtons or cancer hence why it goes back to q0
        #or q1 on anything besides a G
        "Q3": {"T": "Q3", "A": "Q3", "G": "Q4", "C": "Q10"},# accept state start codon
        "Q4": {"T": "Q3", "A": "Q3", "G": "Q5", "C": "Q10"},
        "Q5": {"T": "Q6", "G": "Q5", "A": "Q3", "C": "Q10"},
        "Q6": {"G": "Q7", "T": "Q3", "A": "Q3", "C": "Q10"},
        "Q7": {"A": "Q8", "T": "Q3", "G": "Q5", "C": "Q10"},
        "Q8": {"T": "Q9", "A": "Q3", "G": "Q4", "C": "Q10"},
        # cancer detected when q8 transitions to q9 on a T
        "Q9": {"A": "Q3", "G": "Q3", "T": "Q3", "C": "Q10"},# accept state cancer
        "Q10": {"A": "Q11", "C": "Q10", "T": "Q3", "G": "Q4"},
        "Q11": {"G": "Q12", "C": "Q10", "A": "Q3", "T": "Q3"},
        "Q12": {"C": "Q13", "T": "Q3", "A": "Q3", "G": "Q5"},
        "Q13": {"A": "Q14", "C": "Q10", "T": "Q3"},
        "Q14": {"G": "Q15", "C": "Q10", "T": "Q3", "A": "Q3"},
        "Q15": {"C": "Q16", "G": "Q5", "T": "Q3", "A": "Q3"},
        "Q16": {"G": "Q4", "A": "Q17", "T": "Q3", "C": "Q10"},
        "Q17": {"G": "Q18", "C": "Q10", "T": "Q3", "A": "Q3"},
        # huntingtons detected when q17 transitions to q18 on a G
        "Q18": {"G": "Q4", "C": "Q3", "A": "Q3", "T": "Q3"},#accept state huntingtons
    }
    # updates the current state based on the input character
    def transition(self, char):
        self.state = self.TRANSITIONS[self.state].get(char, "Q0")

    #deals with the state indexing
    def state_index(self):
        # checks if start codon has been detected before so it doesn't reassign the detection index
        if self.state == "Q3" and not self.start_codon_detected:
            self.start_codon_detected = True
            self.start_codon_index = self.position - 2
        #same logic as above
        elif self.state == "Q9" and not self.cancer_detected:
            self.cancer_detected = True
            self.cancer_index = self.position - 5
        #same logic as above
        elif self.state == "Q18" and not self.huntingtons_detected:
            self.huntingtons_detected = True
            self.huntingtons_index = self.position - 8

    def run(self, sequence):
        #itterates through the entire string
        for i in range(len(sequence)):
            #keeps track of the position
            self.position = i
            #passes the letter at the current index in the string to the transition
            self.transition(sequence[i])
            self.state_index()
            #  the entirety of the detected sequence from start codon to mutation/diseases
            if self.start_codon_detected:
                if self.cancer_detected:
                    self.sequence_cancer = sequence[self.start_codon_index:self.cancer_index + 6]

                if self.huntingtons_detected:
                    self.sequence_huntingtons = sequence[self.start_codon_index:self.huntingtons_index + 9]

        #returns a dictionary about what the genetic analyzer detected
        return {
            "start_codon": self.start_codon_detected,
            "start_codon_index": self.start_codon_index,
            "cancer": self.cancer_detected,
            "cancer_index": self.cancer_index,
            "huntingtons": self.huntingtons_detected,
            "huntingtons_index": self.huntingtons_index,
            "sequence_cancer": self.sequence_cancer,
            "sequence_huntingtons": self.sequence_huntingtons
        }
