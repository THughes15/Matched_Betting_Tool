import os
from tkinter import Toplevel
from frames import *


class App(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # Configure the root window
        self.title('Matched Betting Tool')
        self.geometry('427x180')

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Quali):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # Display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Home Page Frame
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        normal_inputs = Inputs(self)
        normal_inputs.grid(column=0, row=0, padx=20)

        # Menu Buttons
        menu = Menu(self, controller)
        menu.grid(column=1, row=0)


class Menu(Frame):
    def __init__(self, ws, controller):
        Frame.__init__(self, ws)
        self.ws = ws

        home_button = ttk.Button(self, text="Home Page",
                                 command=lambda: controller.show_frame(StartPage))
        home_button.grid(row=0, column=0, padx=10, pady=10)

        quali_button = ttk.Button(self, text="Qualification",
                                  command=lambda: controller.show_frame(Quali))
        quali_button.grid(row=1, column=0, padx=10, pady=10)

        button1 = ttk.Button(self, text="Open Log",
                             command=lambda: os.startfile('Betting Tool Log.xlsx'))
        button1.grid(row=2, column=0, padx=10, pady=10)

        button2 = ttk.Button(self, text="Calculator",
                             command=lambda: self.open_window())
        button2.grid(row=3, column=0, padx=10, pady=10)

    def open_window(self):
        window = Window(self)
        window.grab_set()


# Qualification Bet Page Frame
class Quali(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        options = QualiInputs(self)
        options.grid(column=0, row=0, padx=20)

        menu = Menu(self, controller)
        menu.grid(column=1, row=0, sticky='N')


# Calculator Window
class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('295x335')
        self.title('Calculator')

        self.optimal = ''
        self.back_profit = ''
        self.lay_profit = ''

        # Bet Type Selection
        type_frame = Frame(self)
        label = ttk.Label(type_frame, text='Bet Type:')
        label.grid(column=0, row=0)
        self.bet_type = ttk.Combobox(type_frame, width=17)
        self.bet_type['values'] = ('Qualification',
                                   'Free Bet (SNR)',
                                   'Free Bet (SR)')
        self.bet_type.current(0)
        self.bet_type.grid(column=0, row=1)

        # Back Stake Info
        frame1 = Frame(self)
        label = ttk.Label(frame1, text='Back Stake:')
        label.grid(column=0, row=0)
        self.stake = ttk.Entry(frame1)
        self.stake.grid(column=0, row=1)

        # Back Odds Info
        frame2 = Frame(self)
        label = ttk.Label(frame2, text='Back Odds:')
        label.grid(column=0, row=0)
        self.back_odds = ttk.Entry(frame2)
        self.back_odds.grid(column=0, row=1)

        # Lay Odds Info
        frame3 = Frame(self)
        label = ttk.Label(frame3, text='Lay Odds:')
        label.grid(column=0, row=0)
        self.lay_odds = ttk.Entry(frame3)
        self.lay_odds.grid(column=0, row=1)

        # Lay Commission Info
        frame4 = Frame(self)
        label = ttk.Label(frame4, text='Commission (%):')
        label.grid(column=0, row=0)
        self.commission = ttk.Entry(frame4)
        self.commission.insert('end', '0')
        self.commission.grid(column=0, row=1)

        type_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=10)
        frame1.grid(column=0, row=1, padx=10, pady=10)
        frame2.grid(column=1, row=1, padx=10, pady=10)
        frame3.grid(column=0, row=2, padx=10, pady=10)
        frame4.grid(column=1, row=2, padx=10, pady=10)

        button = ttk.Button(self, text='Calculate',
                            command=self.calc,  default='active')
        button.grid(column=0, row=4, columnspan=2, pady=20, ipady=5, ipadx=5)

        # Frame to display calculations
        calc_frame = Frame(self)
        label = tk.Label(calc_frame, text='Optimal Lay Bet: ')
        label.grid(column=0, row=0)
        self.optimal_label = tk.Label(calc_frame, text='')
        self.optimal_label.grid(column=1, row=0)

        label = tk.Label(calc_frame, text='Bookmaker Win Profit/Loss: ')
        label.grid(column=0, row=1)
        self.back_label = tk.Label(calc_frame, text='')
        self.back_label.grid(column=1, row=1)

        label = tk.Label(calc_frame, text='Exchange Win Profit/Loss: ')
        label.grid(column=0, row=2)
        self.lay_label = tk.Label(calc_frame, text='')
        self.lay_label.grid(column=1, row=2)

        calc_frame.grid(column=0, row=6, columnspan=2)

    def calc(self):
        bet_type = self.bet_type.get()
        stake = float(self.stake.get())
        back_odds = float(self.back_odds.get())
        lay_odds = float(self.lay_odds.get())
        comm = float(self.commission.get()) / 100

        if bet_type == 'Qualification':
            optimal = round(back_odds / (lay_odds - comm) * stake, 2)
            back_profit = ((back_odds - 1) * stake) - ((lay_odds - 1) * optimal)
            lay_profit = (optimal * (1 - comm)) - stake
        elif bet_type == 'Free Bet (SNR)':
            optimal = (back_odds - 1) / (lay_odds - comm) * stake
            back_profit = ((back_odds - 1) * stake) - ((lay_odds - 1) * optimal)
            lay_profit = optimal * (1 - comm)
        else:
            optimal = back_odds / (lay_odds - comm) * stake
            back_profit = (back_odds * stake) - ((lay_odds - 1) * optimal)
            lay_profit = optimal * (1 - comm)

        self.optimal_label['text'] = f'£{optimal}'
        self.back_label['text'] = f'£{back_profit:.2f}'
        self.lay_label['text'] = f'£{lay_profit:.2f}'


if __name__ == "__main__":
    app = App()
    app.mainloop()
