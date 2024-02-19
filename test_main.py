import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
from create_investment_data import create_investment_table


def expenditure_type(expenditure, investment_type):
    expenditure = {f'capital_fish_farm': ['Land', 'Construction', 'Power', 'Fingerlings', 'Manpower', 'Miscellenous'],
                   'operational_fish_farm': ['Power', 'Fish Feed', 'Salary', 'Fish Treatment', 'Maintenance', 'Others']}


class InvestmentTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Investment Tracker")
        self.root.geometry("500x500")
        self.root.configure(bg='lightblue')

        self.heading_font = font.Font(family='Courier', size=12, weight='bold')
        self.welcome_label = font.Font(family='Helvetica', size=10)
        self.label_font = font.Font(family='Helvetica', size=14)

        self.investment_types = ["Real Estate", "Agriculture", "Stocks", "Cryptocurrency", "Loan"]

        self.main_frame = tk.Frame(self.root, bg='lightblue')
        self.secondary_frame = tk.Frame(self.root, bg='lightblue')
        self.secondary_frame.grid(row=1, column=0, columnspan=2)

        user = self.check_user_data()

        if user:
            self.proceed_to_main(user[0])
        else:
            self.welcome_screen()

    def store_investment_data(self, investment_type, investment_subtype, investment_name, expenditure_type):
        unique_name = f'{investment_type}_{investment_subtype}_{investment_name}_{expenditure_type}'
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS PreviousInvestments (Type TEXT, Subtype TEXT, Name TEXT, UniqueName TEXT)")
        c.execute("INSERT INTO PreviousInvestments VALUES (?, ?, ?, ?)",
                  (investment_type, investment_subtype, investment_name, unique_name))
        conn.commit()
        conn.close()

    def check_user_data(self):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS User (Name TEXT, Email TEXT)")
        c.execute("SELECT * FROM User")
        user = c.fetchone()
        conn.close()
        return user

    def store_user_data(self, name, email):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO User VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()

    def submit_welcome_info(self):
        name = self.name_var.get()
        email = self.email_var.get()
        self.store_user_data(name, email)
        self.proceed_to_main(name)

    def welcome_screen(self):
        self.welcome_frame = tk.Frame(self.root, bg='lightblue')
        self.welcome_frame.grid(row=0, column=0)

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        ttk.Label(self.welcome_frame, text="Welcome to your Personal Investment Tracker!", font=self.heading_font,
                  background='lightblue').grid(row=0, column=0, columnspan=2)
        ttk.Label(self.welcome_frame, text="Enter your name: ", font=self.label_font,
                  background='lightblue').grid(row=1, column=0)
        ttk.Entry(self.welcome_frame, textvariable=self.name_var, font=self.label_font,
                  background='lightblue').grid(row=1, column=1)
        ttk.Label(self.welcome_frame, text="Enter your email:", font=self.label_font,
                  background='lightblue').grid(row=2, column=0)
        ttk.Entry(self.welcome_frame, textvariable=self.email_var, background='lightblue').grid(row=2, column=1)
        tk.Button(self.welcome_frame, text="Submit", command=self.submit_welcome_info, font=self.label_font,
                  bg='green', fg='white').grid(row=3, column=0, columnspan=2)

    def proceed_to_main(self, name):
        self.welcome_frame.grid_forget() if 'welcome_frame' in self.__dict__ else None

        self.main_frame.grid(row=0, column=0)
        tk.Label(self.main_frame, text=f"Hey {name}! \n Welcome to your Personal Investment Tracker",
                 font=self.heading_font,
                 bg='lightblue').grid(row=0, column=0, columnspan=3)

        tk.Label(self.main_frame, text=f'What would you like to do today?', font=self.welcome_label,
                 bg='lightblue').grid(row=1, column=0)

        tk.Button(self.main_frame, text='Track Investment', command=self.track_investment, font=self.label_font,
                  bg='green', fg='white').grid(row=5, column=1, sticky='nsew', pady=5)
        tk.Button(self.main_frame, text='Log Investment', command=self.log_investment, font=self.label_font, bg='green',
                  fg='white').grid(row=4, column=1, sticky='nsew', pady=1)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    def track_investment(self):
        self.new_window("Track Investment", "What Investment would you like to track?")

    def log_investment(self):
        self.new_window("Log Investment", "What investment would you like to log?")

    def display_fields(self, investment_type, frame, is_previous_investment, new_inv_name_var):
        create_investment_table(investment_type)
        fields_to_display = []
        field_names = {
            "Real Estate": {
                'capital': ['Property_ID', 'Purchase_Date', 'Property_Location', 'Purchase_Price', 'Construction_Cost'],
                'operational': ['Maintenance', 'Utilities', 'Property_Tax', 'Rent_Income']
            },
            "Agriculture": {
                'Fish Farm': {
                    'capital': ['Land', 'Construction', 'Power', 'Fingerlings'],
                    'operational': ['Power', 'Fish_Feed', 'Salary', 'Fish_Treatment', 'Maintenance']
                },
                'Cereal Farm': {
                    'capital': ['Land', 'Machinery', 'Initial_Seeds'],
                    'operational': ['Fertilizers', 'Pesticides', 'Labour', 'Water']
                },
                'Fruit Farm': {
                    'capital': ['Land', 'Initial_Plants', 'Equipment'],
                    'operational': ['Fertilizers', 'Pesticides', 'Labour', 'Water']
                },
                'Dairy Farm': {
                    'capital': ['Land', 'Barn_Construction', 'Initial_Cattle_Purchase'],
                    'operational': ['Feed', 'Veterinary_Care', 'Labour', 'Machinery_Maintenance']
                },
                'Poultry Farm': {
                    'capital': ['Land', 'Coop_Construction', 'Initial_Chick_Purchase'],
                    'operational': ['Feed', 'Veterinary_Care', 'Labour', 'Heating']
                },
                'Livestock Farm': {
                    'capital': ['Land', 'Fencing', 'Initial_Livestock_Purchase'],
                    'operational': ['Feed', 'Veterinary_Care', 'Labour']
                },
                'Other': {
                    'capital': ['Land', 'Equipment'],
                    'operational': ['Maintenance', 'Labour', 'Other_Costs']
                }
            },
            "Stocks": {
                'capital': ['Stock_ID', 'Ticker', 'Purchase_Date', 'Purchase_Price', 'Number_of_Shares'],
                'operational': ['Brokerage_Fee', 'Dividends']
            },
            "Cryptocurrency": {
                'capital': ['Crypto_ID', 'Coin_Name', 'Purchase_Date', 'Purchase_Price', 'Quantity'],
                'operational': ['Transaction_Fees', 'Maintenance_Fee']
            },
            "Loan": {
                'capital': ['Loan_ID', 'Borrower_Name', 'Principal_Amount', 'Interest_Rate'],
                'operational': ['Start_Date', 'End_Date', 'Repayment_Schedule', 'Outstanding_Amount']
            }
        }
        if is_previous_investment:
            conn = sqlite3.connect('investments.db')
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS PreviousInvestments (Type TEXT, Name TEXT, UniqueName TEXT)")
            c.execute("SELECT DISTINCT Name FROM PreviousInvestments WHERE Type = ?", (investment_type,))
            previous_investments = [item[0] for item in c.fetchall()]
            conn.close()
            if previous_investments:
                ttk.Label(frame, text="Select Previous Investment:", background='lightblue').grid(row=0, column=0)
                previous_investment_combo = ttk.Combobox(frame, values=previous_investments)
                previous_investment_combo.grid(row=0, column=1)
            else:
                messagebox.showerror("Error", "No saved Investment for Investment Type")
                return
        else:
            ttk.Label(frame, text="New Investment Name:", background='lightblue').grid(row=0, column=0)
            ttk.Entry(frame, textvariable=new_inv_name_var, background='lightblue').grid(row=0, column=1)

        def populate_fields(fields):
            # Remove existing widgets in the frame
            for widget in frame.winfo_children():
                widget.destroy()

            # Populate the fields
            for i, field in enumerate(fields['capital']):
                ttk.Label(frame, text=field, background='lightblue').grid(row=i, column=0)
                ttk.Entry(frame, textvariable=tk.StringVar(), background='lightblue').grid(row=i, column=1)

            # Add a separator for operational fields
            ttk.Label(frame, text="-------", background='lightblue').grid(row=len(fields['capital']), column=0)

            # Continue populating for operational fields
            for i, field in enumerate(fields['operational']):
                ttk.Label(frame, text=field, background='lightblue').grid(row=i + len(fields['capital']) + 1, column=0)
                ttk.Entry(frame, textvariable=tk.StringVar(), background='lightblue').grid(
                    row=i + len(fields['capital']) + 1, column=1)

        if investment_type == "Agriculture":
            # Create a dropdown for subtypes if Agriculture is selected
            ttk.Label(frame, text="Type of Agriculture", background='lightblue').grid(row=0, column=0)
            agriculture_types = list(field_names["Agriculture"].keys())
            type_of_agriculture_combo = ttk.Combobox(frame, values=agriculture_types, font=self.label_font)
            type_of_agriculture_combo.grid(row=0, column=1)

            def update_agriculture_fields(event):
                nonlocal fields_to_display  # Declare as nonlocal to modify
                subtype = type_of_agriculture_combo.get()
                if subtype:
                    fields_to_display = field_names['Agriculture'][subtype]
                    populate_fields(fields_to_display)

            type_of_agriculture_combo.bind("<<ComboboxSelected>>", update_agriculture_fields)
        else:
            fields_to_display = field_names.get(investment_type, {})
            populate_fields(fields_to_display)

    def new_window(self, title, question):
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.configure(bg='lightblue')

        tk.Label(new_window, text=question, font=self.label_font, bg='lightblue').pack()
        investment_type_combo = ttk.Combobox(new_window, values=self.investment_types, font=self.label_font)
        investment_type_combo.pack()
        fields_frame = tk.Frame(new_window, bg='lightblue')
        fields_frame.pack()

        new_inv_name_entry = None  # Initialize as None

        def update_fields(event):
            selected_type = investment_type_combo.get()
            if selected_type:
                # nonlocal new_inv_name_entry
                for widget in fields_frame.winfo_children():
                    widget.destroy()
                # new_inv_name_entry = self.display_fields(investment_type_combo.get(), fields_frame, True, new_inv_name_var)

            ask_previous = messagebox.askyesno("Question", 'Would you like to log previous investment?')
            new_inv_name_var = tk.StringVar()
            if ask_previous:
                self.display_fields(investment_type_combo.get(), fields_frame, True, new_inv_name_var)
            else:
                self.display_fields(investment_type_combo.get(), fields_frame, False, new_inv_name_var)

        investment_type_combo.bind("<<ComboboxSelected>>", update_fields)

        tk.Button(new_window, text="Back", command=new_window.destroy, font=self.label_font, bg='red',
                  fg='white').pack()

        def save_investment():
            if new_inv_name_entry:  # Only proceed if new_inv_name_entry is not None
                investment_name = new_inv_name_entry.get()
                self.store_investment_data(investment_type_combo.get(), investment_name)

        save_button = tk.Button(new_window, text="Save Investment", command=save_investment, font=self.label_font,
                                bg='green', fg='white')
        save_button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentTrackerApp(root)
    root.mainloop()
