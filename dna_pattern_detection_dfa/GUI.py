import tkinter as tk
from tkinter import filedialog, messagebox
from dfa1 import GeneticAnalyzer
from PIL import Image, ImageTk
#install the pillow lib so pip install pillow

class GUIApp:
    def __init__(self, root):
        # initialize the main window
        self.root = root
        self.root.title("Genetic Analyzer")
        self.root.geometry("600x600")

        # background Canvas
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)

        #display image
        self.bg_image = Image.open("dna_background.jpg")
        self.bg_image = self.bg_image.resize((600, 600))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        #creates the prompt asking the user to enter the sequence
        self.label = tk.Label(root, text="Select a file or enter sequence:", font=("Arial", 14), bg="white")
        self.label.place(x=150, y=30)

        # creates the button that allows a user to select a file
        self.load_button = tk.Button(root, text="Load File", command=self.load_file, font=("Arial", 12))
        self.load_button.place(x=180, y=70)

        # creates the widget for the user to type the sequence
        self.sequence_entry = tk.Entry(root, width=50, font=("Arial", 12))
        self.sequence_entry.place(x=50, y=110)

        # creates the button to analyze the sequence entered
        self.analyze_button = tk.Button(root, text="Analyze Text", command=self.analyze_text, font=("Arial", 12))
        self.analyze_button.place(x=450, y=105)

        self.result_label = tk.Label(root, text="Results:", font=("Arial", 12, "bold"), bg="white")
        self.result_label.place(x=50, y=160)

        self.result_text = tk.Text(root, height=10, width=70, font=("Arial", 10))
        self.result_text.place(x=50, y=190)

    def load_file(self): #loads the file and extracts the text
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    sequence = file.read().strip()
                    self.run_analyzer(sequence)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read the file: {e}")

    def analyze_text(self): # handles text inputs
        sequence = self.sequence_entry.get().strip()
        if not sequence:
            messagebox.showwarning("Warning", "Please enter a genetic sequence.")
            return
        self.run_analyzer(sequence)


    def run_analyzer(self, sequence):
        analyzer = GeneticAnalyzer()

        result = analyzer.run(sequence)

        # clear previous results from the result text box
        self.result_text.delete("1.0", tk.END)

        result_text = "\n--- New Analysis ---\n"
        result_text += f"Start Codon: {'Detected at index ' + str(result['start_codon_index']) if result['start_codon'] else 'Start codon not found'}\n"

        findings = []
        if result["cancer"] is not False:
            findings.append(
                f"Cancer: Detected at index {result['cancer_index']}\nStart Codon to Cancer Sequence: {result['sequence_cancer']}")
        if result["huntingtons"] is not False:
            findings.append(
                f"Huntington's Disease: Detected at index {result['huntingtons_index']}\nStart Codon to Huntington’s Sequence: {result['sequence_huntingtons']}")

        # if no significant patterns are found, show an appropriate message
        if result["start_codon"]:
            result_text += "\n".join(findings) if findings else "No significant patterns found.\n"

        #display the results
        self.result_text.insert(tk.END, result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
