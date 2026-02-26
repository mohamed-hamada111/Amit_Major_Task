import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import seaborn as sns


# ==============================
# Core Data Processing Class
# ==============================

class Data_Preprocessing:
    def __init__(self, data):
        self.df = data

    def overview(self):
        return pd.DataFrame({
            "Column": self.df.columns,
            "Dtype": self.df.dtypes,
            "Unique": self.df.nunique(),
            "Missing": self.df.isnull().sum()
        })

    def numerical_cols(self):
        return self.df.select_dtypes(include='number').columns

    def categorical_cols(self):
        return self.df.select_dtypes(include='object').columns

    def drop_duplicate(self):
        self.df = self.df.drop_duplicates()

    def clean_missing_data(self, strategy='mean'):
        ratio = self.df.isnull().mean()

        # Drop columns with >= 30% missing
        drop_cols = ratio[ratio >= 0.3].index
        self.df = self.df.drop(columns=drop_cols)

        # Fill numeric
        for col in self.numerical_cols():
            if strategy == 'mean':
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            else:
                self.df[col] = self.df[col].fillna(self.df[col].median())

        # Fill categorical
        for col in self.categorical_cols():
            self.df[col] = self.df[col].fillna(self.df[col].mode()[0])


# ==============================
# Tkinter Application
# ==============================

class DataApp(tk.Tk):
    def __init__(self, df):
        super().__init__()

        self.title("Data Preprocessing App")
        self.geometry("1200x700")

        self.processor = Data_Preprocessing(df)

        # Layout
        self.create_sidebar()
        self.create_main_area()

    # ==============================
    # Sidebar
    # ==============================

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg="#2c3e50", width=200)
        sidebar.pack(side="left", fill="y")

        ttk.Button(sidebar, text="Overview", command=self.show_overview).pack(pady=10, fill="x")
        ttk.Button(sidebar, text="Cleaning", command=self.show_cleaning).pack(pady=10, fill="x")
        ttk.Button(sidebar, text="Visualization", command=self.show_visualization).pack(pady=10, fill="x")

    # ==============================
    # Main Area
    # ==============================

    def create_main_area(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.tree = ttk.Treeview(self.main_frame)
        self.tree.pack(fill="both", expand=True)

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ==============================
    # Overview Section
    # ==============================

    def show_overview(self):
        self.clear_main()
        df = self.processor.overview()
        self.display_dataframe(df)

    # ==============================
    # Cleaning Section
    # ==============================

    def show_cleaning(self):
        self.clear_main()

        frame = tk.Frame(self.main_frame)
        frame.pack(pady=20)

        ttk.Button(frame, text="Drop Duplicates", command=self.drop_duplicates).pack(pady=10)

        self.strategy = ttk.Combobox(frame, values=["mean", "median"])
        self.strategy.current(0)
        self.strategy.pack(pady=10)

        ttk.Button(frame, text="Handle Missing Values", command=self.handle_missing).pack(pady=10)

    def drop_duplicates(self):
        self.processor.drop_duplicate()
        messagebox.showinfo("Done", "Duplicates removed successfully.")
        self.display_dataframe(self.processor.df)

    def handle_missing(self):
        strategy = self.strategy.get()
        self.processor.clean_missing_data(strategy=strategy)
        messagebox.showinfo("Done", f"Missing values handled using {strategy}.")
        self.display_dataframe(self.processor.df)

    # ==============================
    # Visualization Section
    # ==============================

    def show_visualization(self):
        self.clear_main()

        frame = tk.Frame(self.main_frame)
        frame.pack(pady=20)

        self.column_select = ttk.Combobox(frame, values=list(self.processor.df.columns))
        self.column_select.pack(pady=10)

        ttk.Button(frame, text="Distribution", command=self.plot_distribution).pack(pady=10)
        ttk.Button(frame, text="Correlation", command=self.plot_correlation).pack(pady=10)

    def plot_distribution(self):
        column = self.column_select.get()
        if column == "":
            return

        top = tk.Toplevel(self)
        top.title("Distribution Plot")

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

        if column in self.processor.numerical_cols():
            upper = self.processor.df[column].quantile(0.99)
            filtered = self.processor.df[self.processor.df[column] <= upper]
        else:
            filtered = self.processor.df

        sns.histplot(filtered[column], ax=ax, bins=30)
        ax.set_title(f"Distribution of {column}")

        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def plot_correlation(self):
        top = tk.Toplevel(self)
        top.title("Correlation Heatmap")

        fig = Figure(figsize=(6, 5))
        ax = fig.add_subplot(111)

        corr = self.processor.df.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # ==============================
    # Data Display
    # ==============================

    def display_dataframe(self, df):
        self.clear_main()

        tree = ttk.Treeview(self.main_frame)
        tree.pack(fill="both", expand=True)

        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))


# ==============================
# Run Application
# ==============================

if __name__ == "__main__":
    df = pd.read_csv("fordgobike-tripdataFor201902.csv")
    app = DataApp(df)
    app.mainloop()