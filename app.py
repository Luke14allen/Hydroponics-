import tkinter as tk
from PIL import Image, ImageTk
import os
import process

def on_mouse_wheel(event, canvas, scroll_direction="vertical"):
    if scroll_direction == "vertical":
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    else:
        canvas.xview_scroll(int(-1*(event.delta/120)), "units")

def runApp():
    imagefold = 'images'
    datafold = 'data'
    # Set up the main window
    app = tk.Tk()
    app.title("Hydroponics")
    app.geometry("1080x600")

    #title 
    label = tk.Label(app, text="Hydroponics Data", font=("Arial", 14))
    label.pack(side="top")

    #showcase data
    datacan = tk.Canvas(app)
    datacan.pack(side='bottom', fill='both', expand=True)
    scroll = tk.Scrollbar(app, orient="vertical", command=datacan.yview)
    scroll.pack(side='right', fill='y')

    datacan.configure(yscrollcommand=scroll.set)
    datacan.bind('<Enter>', lambda event: datacan.bind('<MouseWheel>', lambda event: on_mouse_wheel(event, datacan, "vertical")))
    datacan.bind('<Leave>', lambda event: datacan.unbind('<MouseWheel>'))
    label_frame = tk.Frame(datacan)
    datacan.create_window((0,0), window=label_frame, anchor='nw')
    for file in os.listdir(datafold):
        file_path = os.path.join(datafold, file)
        data = process.read_csv_by_date(file_path)
        avg = process.getAverages(data)
        for key, value in avg.items():
            label = tk.Label(label_frame, text=f'{key}:  {value}', font=('Arial', 12))
            label.pack(side='top', anchor='w')
        dates = list(data)
        date1 = dates[0]
        date2 = dates[-1]
        averages = tk.Label(label_frame, text=f"Data Average for {date1} through {date2}", font=("Arial", 12))
        averages.pack(side="top",anchor='w')
    label_frame.update_idletasks()
    datacan.config(scrollregion=datacan.bbox("all"))

    curcan = tk.Canvas(app)
    curcan.place(relx=1.0, rely=1.0, anchor='se', relwidth=0.5, relheight=0.5)
    current = tk.Label(curcan, text='Current Readings', font=('Arial', 12))
    current.place(relx=0.5, rely=0.5, anchor='center')
    files = os.listdir(datafold)
    file_paths = [os.path.join(datafold, file) for file in files]
    file_times = [(file, os.path.getmtime(file)) for file in file_paths]

    file_times.sort(key=lambda x: x[1], reverse=True)

    most_recent_file = file_times[0][0]
    currdata = process.read_csv_by_date(most_recent_file)
    print(currdata)

    photos = []
    frame = tk.Frame(app)
    frame.pack(fill='both', expand=True)
    canvas = tk.Canvas(frame, width=1000, height=250)
    h_scroll = tk.Scrollbar(frame, orient='horizontal', command=canvas.xview)
    canvas.configure(xscrollcommand=h_scroll.set)
    
    canvas.bind('<Enter>', lambda event: canvas.bind('<MouseWheel>', lambda event: on_mouse_wheel(event, canvas, "horizontal")))
    canvas.bind('<Leave>', lambda event: canvas.unbind('<MouseWheel>'))
    
    h_scroll.pack(side='bottom', fill='x')
    canvas.pack(side='left', fill='both', expand=True)

    image_frame = tk.Frame(canvas)
    canvas.create_window((0,0), window=image_frame, anchor='nw')
# Loop through all images in the folder
    for filename in reversed(os.listdir(imagefold)):
        file_path = os.path.join(imagefold, filename)
        
        # Open and resize the image
        image = Image.open(file_path)
        resized_image = image.resize((200, 200))
        
        # Convert to Tkinter-compatible image
        photo = ImageTk.PhotoImage(resized_image)
        
        # Keep a reference to avoid garbage collection
        photos.append(photo)
        date = process.extract_date_from_image(file_path)
        # Create and display label with image and filename
        label = tk.Label(image_frame, text=date, image=photo, compound='top')
        label.pack(side='left', padx=5)
    image_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))
    
    app.mainloop()
if __name__ == "__main__":
    runApp()
