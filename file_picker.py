import tkinter
import tkinter.filedialog

class FilePicker:
    def __init__(self):
        self.top = tkinter.Tk()
        self.top.withdraw()
        self.file_name = None
        self.is_folder = False

    def prompt_file(self, title="Select a file", filetypes=[("All files", "*.*")], initialdir="/"):
        if filetypes == []:
            filetypes = [("All files", "*.*")]
        elif filetypes == None:
            filetypes = [("All files", "*.*")]
        elif filetypes == "Folder":
            self.file_name = tkinter.filedialog.askdirectory(title=title, initialdir=initialdir)
            self.is_folder = True
            return self.file_name
        self.file_name = tkinter.filedialog.askopenfilename(title=title, filetypes=filetypes, initialdir=initialdir)
        self.is_folder = False
        return self.file_name


if __name__ == "__main__":
    file_picker = FilePicker()
    print(file_picker.prompt_file())
    print(file_picker.file_name)
    print(file_picker.is_folder)
    print(file_picker.prompt_file(title="Select a folder", filetypes="Folder", initialdir="/"))
    print(file_picker.is_folder)