import tkinter as tk
def runApp():
    
    # Set up the main window
    app = tk.Tk()
    app.title("Hydroponics")
    app.geometry("1080x1920")

    #title 
    label = tk.Label(app, text="Hydroponics Data", font=("Arial", 14))
    label.pack(side="top")

    #showcase data


    app.mainloop()
runApp()
