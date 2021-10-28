import tkinter as tk
import webbrowser
import modules
import PVOUT_multi
import concurrent.futures
from tkinter import ttk
from tkinter.constants import HORIZONTAL
from tkinter.messagebox import showerror
from PIL import Image, ImageTk

class Visual(tk.Tk):
    def __init__(self):
        super().__init__()
        
        class MainFrame(tk.Frame):
            def __init__(self, container):
                super().__init__(container)

            def mppt_results(self, df):
                # Positioning
                self.place(x=25, y=200)

                # Create a Treeview with dual Scrollbars
                tree = tk.ttk.Treeview(self, column=("c1", "c2", "c3", "c4"), show='headings', height=8)
                tree.column("# 1",anchor=tk.CENTER, stretch=tk.NO)
                tree.column("# 2", anchor=tk.CENTER, stretch=tk.NO)
                tree.column("# 3",anchor=tk.CENTER, stretch=tk.NO)
                tree.column("# 4", anchor=tk.CENTER, stretch=tk.NO)

                # Setting a limit of data to show per window
                if df.shape[0] > 8:
                    vsb = tk.Scrollbar(self, orient="vertical", command=tree.yview)
                    tree.configure(yscrollcommand=vsb.set)
                    vsb.grid(column=1, row=0, sticky=tk.NS)

                tree.grid(column=0, row=0, sticky=tk.NSEW)
                self.grid_columnconfigure(0, weight=1)
                self.grid_rowconfigure(0, weight=1)

                for index, header in enumerate(df.columns):
                    tree.column(index, width=82)
                    tree.heading(index, text=header)
                for row in range(df.shape[0]):
                    tree.insert('', 'end', values=list(df.iloc[row]))

        # Configure the root window
        self.color = 'white smoke'
        self.width = 380
        self.height = 250
        self.title('PVsolar')
        self.geometry(f'{self.width}x{self.height}')
        self.configure(background=self.color)

        # Calling innerclass
        self.data_frame = MainFrame(self)

        # Button indicatior
        self.indicator = 2
        self.df_indicator = 0
        self.checkbutton_state = tk.IntVar()

        #Months
        self.month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Buttons
        self.mppt_distribuitor = tk.Button(self, text="MPPT Distribuitor",
                     bd=1, width=26, command=lambda: self.save(1))

        self.pv_modules_estimator = tk.Button(self, text="PV Modules Estimator",
                    bd=1, width=26, command=lambda: self.save(2))
        self.save(1,1)
        self.mppt_distribuitor.place(x=0, y=0)
        self.pv_modules_estimator.place(x=int(self.width/2), y=0)
        self.mppt_distribuitor.bind("<Enter>", self.on_enter_button_1)
        self.mppt_distribuitor.bind("<Leave>", self.on_leave_button_1)
        self.pv_modules_estimator.bind("<Enter>", self.on_enter_button_2)
        self.pv_modules_estimator.bind("<Leave>", self.on_leave_button_2)
        self.window()
        

    class EntryWithPlaceholder(tk.Entry):
        def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
            super().__init__(master)

            self.placeholder = placeholder
            self.placeholder_color = color
            self.default_fg_color = self['fg']
            self.configure(width=10)

            self.bind("<FocusIn>", self.foc_in)
            self.bind("<FocusOut>", self.foc_out)

            self.put_placeholder()

        def put_placeholder(self):
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

        def foc_in(self, *args):
            if self['fg'] == self.placeholder_color:
                self.delete('0', 'end')
                self['fg'] = self.default_fg_color

        def foc_out(self, *args):
            if not self.get():
                self.put_placeholder()

    def window(self):
        #Creating
        # 1st Window
        self.modules_number_entry = tk.Entry(self, text="", width=10)
        self.min_modules_per_string_entry = tk.Entry(self, text="", width=10)
        self.max_modules_per_string_entry = tk.Entry(self, text="", width=10)
        self.set_your_parameters_label = tk.Label(self,
                   text="Set your parameters:", font=('Helvetica', 9, 'bold'),
                   justify=tk.CENTER, background=self.color)
        self.modules_number = tk.Label(self,
                   text="Number of photovoltaic modules:", font=('Helvetica', 9, 'bold'),
                   background=self.color)
        self.min_modules_per_string = tk.Label(self,
                   text="Minimum modules per string (desired):", font=('Helvetica', 9, 'bold'),
                background=self.color)
        self.max_modules_per_string = tk.Label(self,
                   text="Maximum modules per string (allowed):", font=('Helvetica', 9, 'bold'),
                background=self.color)
        self.mppt_distribuitor_button = tk.Button(self, text="MPPT Distribuitor",
                    justify=tk.CENTER, bd=1, width=26, command=lambda: self.checker(1))
        self.line = tk.Frame(self, height=1, width=400, bg="grey80", relief='groove')
        # 2nd window
        self.location_entry = tk.Entry(self, width=35)
        self.location_label = tk.Label(self,
                   text="Location: ", font=('Helvetica', 9, 'bold'),
                   background=self.color)
        self.decimal_only = tk.Label(self,
                   text="""Only Decimal Degree format supported.
e.g.: 46.198633, 6.058435""", fg="red" ,font=('Helvetica', 8),
                   justify=tk.CENTER, background=self.color)
        self.module_power = tk.Label(self,
                   text="Module Power:", font=('Helvetica', 9, 'bold'),
                   background=self.color)
        self.module_power_entry = tk.Entry(self, text="", width=5)
        self.Wp_label = tk.Label(self,
                   text="Wp", font=('Helvetica', 9, 'bold'),
                   background=self.color)
        self.avg_energy = tk.Label(self,
                   text="Avg. Energy:", font=('Helvetica', 9, 'bold'),
                   background=self.color)
        self.energy_entry = tk.Entry(self, text="", width=10)
        self.kWh_label = tk.Label(self,
                   text="kWh", font=('Helvetica', 9, 'bold'),
                   background=self.color)
        self.ratio_label = tk.Label(self,
                   text="DC/AC ratio:", font=('Helvetica', 9, 'bold'),
                   background=self.color)
        self.ratio_entry = self.EntryWithPlaceholder(self, "(optional)")
        self.ratio_entry.configure(width=9)
        self.coverage_label = tk.Label(self,
                   text="Coverage:", font=('Helvetica', 9, 'bold'),
                   background=self.color)
        self.coverage_entry = self.EntryWithPlaceholder(self, "(optional)")
        self.coverage_entry.configure(width=9)
        self.percent_simbol = tk.Label(self,
                   text="%", font=('Helvetica', 10, 'bold'),
                   background=self.color)
        self.multiple_energy_values = tk.Checkbutton(self, text="Use Monthly energy values instead", 
        bg=self.color, anchor='w', variable=self.checkbutton_state, command=lambda: self.monthly_values(self.checkbutton_state.get()))
        self.get_results_button = tk.Button(self, text="Get Results",
                    justify=tk.CENTER, bd=1, width=9, command=lambda: self.checker(2))
        self.connecting_label = tk.Label(self,
                   text="Connecting to server...", font=('Helvetica', 9, 'bold'),
                   background=self.color, fg="green")   

        #Loading information window pictures

        self.image_size = {'Gmail': (35, 30), "Stackoverflow": (150, 30), "Github": (125, 30),
              "Paypal": (124, 30), "Info": (33, 33)}
        self.img_gmail = Image.open("images\gmail.png")
        self.img_stack = Image.open("images\stack.png")
        self.img_github = Image.open("images\github.png")
        self.img_paypal = Image.open("images\paypal.png")
        self.img_info = Image.open("images\info.png")
        self.img_gmail = self.img_gmail.resize(self.image_size["Gmail"], Image.ANTIALIAS)
        self.img_stack = self.img_stack.resize(self.image_size["Stackoverflow"], Image.ANTIALIAS)
        self.img_github = self.img_github.resize(self.image_size["Github"], Image.ANTIALIAS)
        self.img_paypal = self.img_paypal.resize(self.image_size["Paypal"], Image.ANTIALIAS)
        self.img_info = self.img_info.resize(self.image_size["Info"], Image.ANTIALIAS)
        self.photo_img_gmail = ImageTk.PhotoImage(self.img_gmail)
        self.photo_img_stack = ImageTk.PhotoImage(self.img_stack)
        self.photo_img_github = ImageTk.PhotoImage(self.img_github)
        self.photo_img_paypal = ImageTk.PhotoImage(self.img_paypal)
        self.photo_img_info = ImageTk.PhotoImage(self.img_info)
        
        self.info_button = tk.Button(self, image=self.photo_img_info, command=self.information)
        self.created_by = tk.Label(self,
                   text="Created by Henfry De Los Santos", font=('Helvetica', 9, 'bold'),
                   justify=tk.CENTER,
                   padx=0, background=self.color)
        self.created_by.place(x = 90, y=210)
        self.info_button.place(x=19, y=200)

        # Positioning
        self.set_your_parameters_label.pack(pady=30)
        self.modules_number.place(x=36, y=61)
        self.min_modules_per_string.place(x=22, y=91)
        self.max_modules_per_string.place(x=20, y=121)
        self.modules_number_entry.place(x=275, y=62)
        self.min_modules_per_string_entry.place(x=275, y=92)
        self.max_modules_per_string_entry.place(x=275, y=122)
        self.mppt_distribuitor_button.pack(pady=73)
        self.line.place(x=0, y=195)
        self.wm_iconphoto(True, tk.PhotoImage(file='images/icon.png'))
        self.wm_iconwindow(self)
     
    def checker(self, window):
        if window == 1:
            modules_number = self.modules_number_entry.get()
            max_modules_per_string_entry = self.max_modules_per_string_entry.get()
            min_modules_per_string_entry = self.min_modules_per_string_entry.get()
            if str(modules_number).strip() == "" or str(max_modules_per_string_entry).strip() == "" or str(min_modules_per_string_entry).strip() == "":
                showerror(title="Error_NO_FILL", message="Please fill in all the fields requested")
            elif not str(modules_number).isdigit() or not str(max_modules_per_string_entry).isdigit() or not str(min_modules_per_string_entry).isdigit():
                showerror(title="Error_NUMBERS", message="Only numbers are allowed")
            elif int(modules_number) < int(min_modules_per_string_entry):
                showerror(title="Error_LESS_MODULES", message="The amount of modules can't be less than the minimum number of modules per string")
            elif int(max_modules_per_string_entry) < int(min_modules_per_string_entry):
                showerror(title="Error: MAX_STRING", message="The maximun number of modules per string can't be less than the minimum number of modules per string")
            elif int(max_modules_per_string_entry) == 0 or int(min_modules_per_string_entry) == 0:
                showerror(title="Error: DIV_0", message="The minimum number of strings to use must be 1")
            else:
                modules_number = int(modules_number)
                max_modules_per_string_entry = int(max_modules_per_string_entry )
                min_modules_per_string_entry = int(min_modules_per_string_entry)
                self.progress_bar()
                self.M = modules.Mppt(min_modules_per_string_entry, max_modules_per_string_entry, modules_number)
                for i, (key, values) in enumerate(self.M.numbers.items()):
                    self.root.update_idletasks()
                    percent = round(((i+1)/len(self.M.numbers)), 4)*100
                    self.update_progress_bar(percent)
                    self.M.combinations(key, values)
                self.root.destroy()

                if len(self.M.Mo_1) == 0:
                    self.df_indicator = 0
                    showerror(title="Error: VALUES_NOT_FOUND", 
                    message="No possible combinations were found with the provided parameters, please consider varying the number of modules per string")
                    self.data_frame.place_forget()
                    self.width = 380
                    self.height = 250
                    self.geometry(f'{self.width}x{self.height}')
                    self.line.place(x=0, y=195)
                    self.created_by.place(x=90, y=210)
                    self.info_button.place(x=19, y=200)
                else:
                    self.df_indicator = 1
                    self.height = 460
                    self.geometry(f'{self.width}x{self.height}')
                    sort = self.M.sorting()
                    self.data_frame.mppt_results(sort)
                    self.line.place(x=0, y=400)
                    self.created_by.place(x=90, y=415)
                    self.info_button.place(x=19, y=405)

        elif window == 2:
            if self.location_entry.get().strip() == "":
                showerror(title="Error: LOCATION_ENTRY", message="Please set the location (in Decimal Degree format).")
            elif self.module_power_entry.get().strip() == "":
                showerror(title="Error: EMPTY_VALUE", message="Please set the module power (Wp).")
            elif self.energy_entry.get().strip() == "":
                showerror(title="Error: ENERGY_ZERO", message="Please enter an energy consumption (kWh).")
            elif self.ratio_entry.get().strip() != "(optional)" and self.ratio_entry.get().strip() != "":
                self.E = PVOUT_multi.MTI(self.location_entry.get(), float(self.module_power_entry.get().strip()), float(self.energy_entry.get().strip()),
                float(self.ratio_entry.get().strip()))
            elif self.coverage_entry.get().strip() != "(optional)" and self.coverage_entry.get().strip() != "":
                self.E = PVOUT_multi.MTI(self.location_entry.get(), float(self.module_power_entry.get().strip()), float(self.energy_entry.get().strip()),
            1.25, (float(self.coverage_entry.get().strip())))
            elif (self.ratio_entry.get().strip() != "(optional)" and self.ratio_entry.get().strip() != "") and self.coverage_entry.get().strip() != "(optional)" and self.coverage_entry.get().strip() != "":
                self.E = PVOUT_multi.MTI(self.location_entry.get(), float(self.module_power_entry.get().strip()), float(self.energy_entry.get().strip()),
                float(self.ratio_entry.get().strip()), (float(self.coverage_entry.get().strip())))
            else:
                self.E = PVOUT_multi.MTI(self.location_entry.get(), float(self.module_power_entry.get().strip()), float(self.energy_entry.get().strip()))
            self.update()
            if self.E:
                self.connecting_label = tk.Label(self,
                   text="                 Connecting to server...    ", font=('Helvetica', 9, 'bold'),
                   background=self.color, fg="green")
                self.connecting_label.place(x=85, y=210)
                self.update_idletasks()
                self.PV_data = self.E.PVOUT_values()
                if self.PV_data is None:
                    self.connecting_label.destroy()
                    showerror(title="DATA_INTERNET_ERROR", message="Internet failure or Not enough data for the provided location was found.")
                else:
                    self.location_data = self.E.location_name()
                    if self.location_data is None:
                        self.connecting_label.destroy()
                        showerror(title="DATA_INTERNET_ERROR", message="Internet failure or Not enough data for the provided location was found.")
                    else:
                        self.connecting_label.destroy()
                        self.result_window(self.location_data, self.PV_data)    

    def result_window(self, location_data, PV_data):
        self.window = tk.Tk()
        self.WINDOW_WIDTH = 310
        self.WINDOW_HEIGHT = 310
        self.window.configure(background=self.color)
        self.window.title("Result")
        tk.Label(self.window, text="Location:", font=('Helvetica', 10, 'bold'),
                   background=self.color).pack(pady=(5,5))
        for name, location in location_data.items():
            tk.Label(self.window, text=f"{name.title()}: {location.title()}", font=('Helvetica', 9, 'bold'),
                   background=self.color).pack(pady=(5,0))
            self.WINDOW_HEIGHT += 26
        self.window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        tk.Label(self.window, text="PV Data*:", font=('Helvetica', 10, 'bold'),
                   background=self.color).pack(pady=(5,5))
        tk.Label(self.window, text=f"Specific PV power output: {PV_data[0]['PVOUT_csi']} kWh/kWp", font=('Helvetica', 9, 'bold'),
                   background=self.color).pack(pady=(5,0))
        tk.Label(self.window, text=f"Direct normal irradiation: {PV_data[0]['DNI']} kWh/m^2", font=('Helvetica', 9, 'bold'),
                   background=self.color).pack(pady=(5,0))
        tk.Label(self.window, text=f"Global horizontal irradiation: {PV_data[0]['GHI']} kWh/m^2", font=('Helvetica', 9, 'bold'),
                   background=self.color).pack(pady=(5,0))
        tk.Label(self.window, text=f"Diffuse horizontal irradiation: {PV_data[0]['DIF']} kWh/m^2", font=('Helvetica', 9, 'bold'),
                   background=self.color).pack(pady=(5,0))
        tk.Label(self.window, text=f"Optimum tilt of PV modules: {PV_data[0]['OPTA']}º", font=('Helvetica', 9, 'bold'),
                   background=self.color).pack(pady=(5,0))
        tk.Label(self.window, text=f"Approx. photovoltaic modules: {PV_data[1]}", font=('Helvetica', 9, 'bold'), fg="blue",
                   background=self.color).pack(pady=(5,0))
        tk.Label(self.window, text=f"""*Despite the fact that all the data shown is real, 
        we recommend carrying out more detailed 
        studies in specialized software for the sizing 
        of photovoltaic plants, such as PVsyst.""", font=('Helvetica', 8, 'bold'), fg="red",
                   background=self.color).pack(pady=(10,0))
        

    def update_progress_bar(self, percent):
        self.root.update()
        self.my_progress['value'] = round(percent, 2)
        self.progress_text['text']= f"{str(percent)[:5]}%"
        self.root.title(f"Loading... {str(percent)[:5]}%")
    
    def terminate(self):
        self.root.destroy()

    def progress_bar(self):
        self.root = tk.Toplevel()
        #self.root.transient(self)
        self.root.grab_set()
        self.root.geometry("300x80")
        self.root.configure(background='white')
        self.root.title("Loading...")
        self.my_progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=200, 
        mode="determinate")
        self.my_progress.place(x=30, y=15)
        self.progress_text = tk.Label(self.root,
                   text="0%", font=('Helvetica', 10, 'bold'),
                background='white')
        self.progress_text.place(x=235, y=15)
        self.abort_button = tk.Button(self.root, text="Abort",
                    justify=tk.CENTER, bd=1, width=15, command=self.terminate).pack(pady=(45,0))

    def hide_window(self, window):
        # Hiding windows 2 elements
        if window == 1:
            self.show(1)
            self.location_label.place_forget()
            self.location_entry.place_forget()
            self.decimal_only.place_forget()
            self.module_power.place_forget()
            self.module_power_entry.place_forget()
            self.Wp_label.place_forget()
            self.avg_energy.place_forget()
            self.energy_entry.place_forget()
            self.kWh_label.place_forget()
            self.ratio_label.place_forget()
            self.ratio_entry.place_forget()
            self.coverage_label.place_forget()
            self.coverage_entry.place_forget()
            self.percent_simbol.place_forget()
            self.multiple_energy_values.place_forget()
            self.get_results_button.place_forget()

        # Hiding windows 1 elements
        if window == 2:
            self.set_your_parameters_label.pack_forget()
            self.modules_number.place_forget()
            self.min_modules_per_string.place_forget()
            self.max_modules_per_string.place_forget()
            self.modules_number_entry.place_forget()
            self.min_modules_per_string_entry.place_forget()
            self.max_modules_per_string_entry.place_forget()
            self.mppt_distribuitor_button.pack_forget()
            self.line.place_forget()
            self.data_frame.place_forget()
            self.width = 380
            self.height = 250
            self.geometry(f'{self.width}x{self.height}')
            self.line.place(x=0, y=195)
            self.show(2)

    def show(self, window):
        if window == 1:
            self.set_your_parameters_label.pack(pady=30)
            self.modules_number.place(x=36, y=61)
            self.min_modules_per_string.place(x=22, y=91)
            self.max_modules_per_string.place(x=20, y=121)
            self.modules_number_entry.place(x=275, y=62)
            self.min_modules_per_string_entry.place(x=275, y=92)
            self.max_modules_per_string_entry.place(x=275, y=122)
            self.mppt_distribuitor_button.pack(pady=73)
            if self.df_indicator == 0:
                self.data_frame.place_forget()
                self.width = 380
                self.height = 250
                self.geometry(f'{self.width}x{self.height}')
                self.line.place(x=0, y=195)
            else:
                self.height = 460
                self.geometry(f'{self.width}x{self.height}')
                self.data_frame.place(x=25, y=200)
                self.line.place(x=0, y=400)
                self.created_by.place(x=90, y=415)
                self.info_button.place(x=19, y=405)

        elif window == 2:
            self.location_label.place(x=35, y=40)
            self.location_entry.place(x=115, y=40)
            self.decimal_only.place(x=125, y=60)
            self.module_power.place(x=15, y= 100)
            self.module_power_entry.place(x=115, y=100)
            self.Wp_label.place(x=150, y=100)
            self.avg_energy.place(x=180, y= 100)
            self.energy_entry.place(x=266, y=100)
            self.kWh_label.place(x=335, y=100)
            self.ratio_label.place(x=20, y= 130)
            self.ratio_entry.place(x=115, y=130)
            self.coverage_label.place(x=187, y= 130)
            self.coverage_entry.place(x=271, y=130)
            self.percent_simbol.place(x=335, y=130)
            self.multiple_energy_values.place(x=100, y=160)
            self.get_results_button.place(x=296, y=209)
            self.created_by.place(x = 90, y=210)
            self.info_button.place(x=19, y=200)

    def monthly_values(self, state):
        columns_and_rows = [(0, 0), (0, 2), (0, 4), (1, 0), (1, 2), 
        (1, 4), (2, 0), (2, 2), (2, 4), (3, 0), (3, 2), (3, 4), ]
        entrys =[(0, 1), (0, 3), (0, 5), (1, 1), (1, 3), 
         (1, 5), (2, 1), (2, 3), (2, 5), (3, 1), (3, 3), (3, 5)]
        if state == 1:
            self.root = tk.Toplevel()
            self.root.resizable(False, False)
            self.root.entries = []
            self.root.grab_set()
            self.root.geometry("320x200")
            self.root.configure(background=self.color)
            self.root.title("Set your monthly values")
            for value in range(12):
                tk.Label(self.root, text=self.month[value], 
                    bg=self.color).grid(row=columns_and_rows[value][0], column=columns_and_rows[value][1], pady=(10,0), padx=(5,0))
                entry = tk.Entry(self.root, width=10)
                entry.grid(row=entrys[value][0], column=entrys[value][1], pady=(10,0), padx=(5,0))
                self.root.entries.append(entry)
                tk.Label(self.root,
                   text="All values most be in kWh", fg="red" ,font=('Helvetica', 8),
                   justify=tk.CENTER, background=self.color).place(x=100, y=125)
            tk.Button(self.root, justify = tk.CENTER, text="Cancel", command=self.terminate, width=15, font=('Helvetica', 9)).place(x=30, y=150)
            tk.Button(self.root, justify = tk.CENTER, text="Set", command=self.get_values, width=15, font=('Helvetica', 9)).place(x=180, y=150)

    def get_values(self):
        self.energy_entry.delete(0, tk.END)
        avg = [float(value.get()) for value in self.root.entries if value.get().strip() != ""]
        try:
            energy_avg = (sum(avg)/len(avg))
        except ZeroDivisionError:
            energy_avg = 0
        self.energy_entry.insert(0, round(energy_avg , 2))
        self.terminate()     

    def information(self):
        self.information_window = tk.Toplevel()
        self.information_window.title('Information')
        self.information_window.configure(background=self.color)
        self.information_window.geometry('380x275')

        tk.Label(self.information_window,
                    text="""Hope this program helped you.
        Please take a minute and read the documentation.
        If you have any questions or suggestion,
        Please feel free to contact me.
        All links are provided down below.""",
                    justify=tk.CENTER,
                    padx=0, background=self.color).pack(pady=(5, 5))

        tk.Label(self.information_window,
                    text='¡Break a leg!', font=('Helvetica', 10, 'bold'),
                    justify=tk.CENTER,
                    padx=0, background=self.color).pack(pady=(0, 2))

        tk.Label(self.information_window,
                    text="Created by Henfry De Los Santos", font=('Helvetica', 8, 'bold'),
                    justify=tk.CENTER,
                    padx=0, background=self.color).pack(pady=5)

        tk.Label(self.information_window,
                        text="Contact me:",
                        justify=tk.CENTER,
                        padx=0, background=self.color).place(x=90, y=145)

        tk.Label(self.information_window,
                        text="Project:",
                        justify=tk.CENTER,
                        padx=0, background=self.color).place(x=280, y=145)
        tk.Label(self.information_window,
                        text="Donate:",
                        justify=tk.CENTER,
                        padx=0, background=self.color).place(x=167, y=205)

        self.gmail_button = tk.Button(self.information_window, image=self.photo_img_gmail, command=self.open_gmail)
        self.stackoverflow_button = tk.Button(self.information_window, image=self.photo_img_stack, command=self.open_stack_page)
        self.github_button = tk.Button(self.information_window, image=self.photo_img_github, command=self.open_github_page)
        self.paypal_button = tk.Button(self.information_window, image=self.photo_img_paypal, command=self.open_paypal_page)

        self.gmail_button.place(x=15, y=165)
        self.stackoverflow_button.place(x=60, y=165)
        self.github_button.place(x=235, y=165)
        self.paypal_button.place(x=125, y=225)
        self.information_window.resizable(False, False)

    def on_enter_button_1(self, action):
        if self.indicator == 1:
            self.mppt_distribuitor['background'] = '#E5F1FB'

    def on_leave_button_1(self, action):
        self.mppt_distribuitor['background'] = 'SystemButtonFace'

    def on_enter_button_2(self, action):
        if self.indicator == 2:
            self.pv_modules_estimator['background'] = '#E5F1FB'

    def on_leave_button_2(self, action):
        self.pv_modules_estimator['background'] = 'SystemButtonFace'

    def save(self, number, index=0):
        self.indicator = number
        if number == 1:
            self.mppt_distribuitor.config(relief=tk.SUNKEN)
            self.stop(2)
            if index == 0:
                self.hide_window(1)
        else:
            self.pv_modules_estimator.config(relief=tk.SUNKEN)
            self.stop(1)
            self.hide_window(2)

    def stop(self, number):
        self.indicator = number
        if number == 1:
            self.mppt_distribuitor.config(relief=tk.RAISED)
        else:
            self.pv_modules_estimator.config(relief=tk.RAISED)
    
    def open_gmail(self):
        webbrowser.open("mailto:?to=henfry@protonmail.com", new=1)

    def open_github_page(self):
        webbrowser.open("https://github.com/henfrydls/PVcolab", new=1)

    def open_stack_page(self):
        webbrowser.open("https://stackoverflow.com/users/14391986/henfry-de-los-santos", new=1)

    def open_paypal_page(self):
        webbrowser.open("http://paypal.me/henfrydls", new=1)

if __name__ == '__main__':
    app = Visual()
    app.resizable(False, False)
    app.mainloop()

"""<div>Iconos diseñados por <a href="https://www.flaticon.es/autores/srip" title="srip">srip
</a> from <a href="https://www.flaticon.es/" title="Flaticon">www.flaticon.es</a></div>"""