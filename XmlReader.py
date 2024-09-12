import tkinter as tk
from tkinter import ttk
import xml.dom.minidom
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# Create a function to toggle dark mode
def toggle_dark_mode():
    dark_mode = dark_mode_var.get()
    if dark_mode:
        # Dark mode color scheme
        root.configure(bg="#1E1E1E")
        xml_display.config(bg="#1E1E1E", fg="#FFFFFF", insertbackground="white")
        open_button.config(bg="#333333", fg="#FFFFFF")
        style.configure("Dark.Vertical.TScrollbar", troughcolor="#333333", background="#1E1E1E")
    else:
        # Light mode color scheme (default)
        root.configure(bg="white")
        xml_display.config(bg="white", fg="black", insertbackground="black")
        open_button.config(bg="lightgray", fg="black")
        style.configure("Dark.Vertical.TScrollbar", troughcolor="lightgray", background="white")

# create the root window
root = tk.Tk()
root.title('xmlReader')
root.geometry("800x600")  # Initial fixed size

# Center all widgets in the root window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Initialize the dark mode variable
dark_mode_var = tk.BooleanVar()
dark_mode_var.set(False)  # Set initial mode to light

# Create a dark mode toggle button
dark_mode_button = tk.Checkbutton(root, text="Dark Mode", variable=dark_mode_var, command=toggle_dark_mode)
dark_mode_button.grid(row=0, column=0, sticky="ne", padx=10, pady=10)

# Create a text widget to display XML content
xml_display = tk.Text(root, wrap=tk.WORD, borderwidth=0, highlightthickness=0, state=tk.DISABLED)
xml_display.grid(row=1, column=0, sticky="nsew")  # Use grid to expand with window

# Create a vertical scroll bar
style = ttk.Style()
style.configure("Dark.Vertical.TScrollbar", troughcolor="lightgray", background="white")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=xml_display.yview, style="Dark.Vertical.TScrollbar")
scrollbar.grid(row=1, column=1, sticky="ns")  # Use grid to place it on the right side

# Configure the text widget to use the scroll bar
xml_display.config(yscrollcommand=scrollbar.set)

# Initialize the file_path variable
file_path = ""

# Function to open an XML file
def open_xml_file():
    global file_path  # Declare file_path as a global variable

    file_path = fd.askopenfilename(
        filetypes=[("XML Files", "*.xml")],
        initialdir="/",  # Set the initial directory (optional)
        title="Select XML File",  # Set the dialog title (optional)
    )
    if file_path:
        display_xml_content(file_path)

        # Parse the selected XML file and perform actions here
        print(f"Opened XML file: {file_path}")
        showinfo(
            title='Open XML File',
            message= 'success'
        )

        # Change the window size after opening the file
        root.geometry("800x600")  # Change to the desired size

    else:
        showinfo(
            title='Open XML File',
            message= 'fail'
        )

# Function to display XML content
def display_xml_content(file_path):
    xml_display.config(state=tk.NORMAL)  # Enable the widget
    xml_display.delete(1.0, tk.END)  # Clear previous content

    try:
        # Parse the XML file
        doc = xml.dom.minidom.parse(file_path)

        # Loop through all the categories
        for category in doc.getElementsByTagName("category"):
            category_caption = category.getAttribute("caption")
            xml_display.insert(tk.END, f"{category_caption}:\n")

            # Loop through all the structures within the category
            for structure in category.getElementsByTagName("structure"):
                structure_caption = structure.getAttribute("caption")
                xml_display.insert(tk.END, f"  {structure_caption}:\n")

                # Loop through all the properties within the structure
                for property_elem in structure.getElementsByTagName("property"):
                    caption = property_elem.getAttribute("caption")
                    value = property_elem.getAttribute("value")
                    xml_display.insert(tk.END, f"    {caption}: {value}\n")

                xml_display.insert(tk.END, "\n")

            xml_display.insert(tk.END, "\n")

    except Exception as e:
        xml_display.insert(tk.END, f"Error: {str(e)}")

# Function to exit the application
def exit_application():
    root.destroy()  # Close the root window and exit the application

# Create a frame for the "Open" button
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0)  # Use grid to place the frame

# Create an "Open XML File" button inside the frame
open_button = tk.Button(button_frame, text="Open XML File", command=open_xml_file)
open_button.grid(row=0, column=0, padx=10, pady=10)  # Use grid to place the button

# Create an "Exit" button inside the frame
exit_button = tk.Button(button_frame, text="Exit", command=exit_application)
exit_button.grid(row=0, column=1, padx=10)  # Use grid to place the button

# Initialize with the default light mode color scheme
toggle_dark_mode()

# run the application
root.mainloop()




