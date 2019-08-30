"""Clockity

This program creates a graphical user interface containing a working
stopwatch, countdown, and a time-date display.
"""

# Author: Roberto Guerra <robertoguerra@mail.com>

import tkinter as tk
import time
import datetime
import winsound
import threading


class Clockity_Window(tk.Tk):
    """This class creates the programs window and window properties.

    This class inherits from the 'Tk' class inside the 'tkinter' module and is
    responsible for creating the window and window properties for the program.
    Also, here is where sound is created and added to the program through the
    use of the 'winsound' module.

    Attributes
    ----------
    frames : dict
        Dictonary storing the different frames with their corresponding names.

    Methods
    -------
    r_frame(self, cont)
        Displays a specific frame above the rest.
    sounds(self, sound)
        Creates and plays three different sounds.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)   # Initializes 'Tk'

        # Used 'Tk' to create the window and window properties
        tk.Tk.wm_title(self, 'Clockity')
        tk.Tk.geometry(self, '360x344')
        tk.Tk.resizable(self, 0, 0)
        tk.Tk.wm_attributes(self, '-topmost', 1)

        # Created to contain other frames
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Names and stores different frames, along with
        # with 'container', into a dictionary
        for F in (Home, Stopwatch, CountDown):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # Called so the first frame to be displayed is 'Home'
        self.r_frame(Home)

    def r_frame(self, cont):
        """Displays a specific frame above the rest.

        Argument 'cont' must be passed as a specific
        frames name for that frame to be displayed.

        Parameters
        ----------
        cont
            The frame being called to be displayed
            using 'tkraise()'.
        """

        frame = self.frames[cont]
        frame.tkraise()

    def sounds(self, sound):
        """Creates and plays three different sounds.

        Argument 'sound' must be passed as an integer
        from one through three for one of the three
        sound effects to be played.

        Parameters
        ----------
        sound : int
            Chooses one of the three sounds to play.
        """

        if sound == 1:
            winsound.Beep(800, 100)
        elif sound == 2:
            winsound.Beep(500, 100)
        elif sound == 3:
            winsound.Beep(2000, 500)


class Home(tk.Frame):
    """Creates the 'Home' frame.

    This class inherits from the 'Frame' class inside the 'tkinter' module
    and is responsible for creating the 'Home' frame, which is to function
    as the programs homepage. Here is where the buttons leading to the other
    frames are created as well as a display showing the current time and date.

    Attributes
    ----------
    updated_home_timedate : str
        The present time and date.

    Methods
    -------
    home_timedate_update()
        Finds and displays the present time and date.
    """

    def __init__(self, parent, controller):
        """
        Parameters
        ----------
        parent : tkinter.Frame
            Required to represent the widgets in this class.
        controller : __main__.Clockity_Window
            Allows 'r_frame()' and 'sounds()', defined in the 'Clockity_Window'
            class, to be called from within this class.
        """

        tk.Frame.__init__(self, parent)     # Initializes 'Frame'

        self.updated_home_timedate = ''

        go_to_stopwatch_frame = tk.Button(
            self,
            text='Stopwatch', font=('Arial', 20, 'bold'),
            fg='black', bg='green',
            height=8, width=10,
            command=lambda: [
                controller.r_frame(Stopwatch),
                controller.sounds(1)
                ]
        )
        go_to_stopwatch_frame.grid(row=0, column=0)

        go_to_countdown_frame = tk.Button(
            self,
            text='Countdown', font=('Arial', 20, 'bold'),
            fg='black', bg='red',
            height=8, width=10,
            command=lambda: [
                controller.r_frame(CountDown),
                controller.sounds(1)
                ]
        )
        go_to_countdown_frame.grid(row=0, column=1)

        present_timedate_label = tk.Label(
            self,
            text=self.updated_home_timedate, font=('Arial', 15, 'bold'),
            fg='black', bg='white',
            height=2,
        )
        present_timedate_label.grid(row=1, columnspan=2, sticky='we')

        def home_timedate_update():
            """Finds and displays the present time and date.

            Must be called using the 'threading' module in order to have it run
            in the background. Otherwise the program will not execute properly.
            """

            # Used to update, and format, the time and date every second
            while True:

                home_dt = datetime.datetime.now()

                home_dt_hours = home_dt.strftime('%I')
                if home_dt_hours[0] == '0':
                    home_dt_hours = home_dt_hours.replace('0', '')
                home_dt_months = home_dt.strftime('%m')
                home_dt_days = home_dt.strftime('%d')
                if home_dt_months[0] == '0':
                    home_dt_months = home_dt_months.replace('0', '')
                if home_dt_days[0] == '0':
                    home_dt_days = home_dt_days.replace('0', '')

                self.updated_home_timedate = (
                    home_dt_hours +
                    home_dt.strftime(':%M %p') +
                    '\n' +
                    home_dt_months +
                    '/' +
                    home_dt_days +
                    home_dt.strftime('/%Y')
                )

                present_timedate_label.configure(
                    text=self.updated_home_timedate
                )

                time.sleep(1)

        # Used to run 'home_time_date_update()' in the background in order
        # to avoid problems executing the rest of the program.
        background_function = threading.Thread(target=home_timedate_update)
        background_function.start()


class Stopwatch(tk.Frame):
    """Creates the Stopwatch frame and a working stopwatch.

    This class inherits from the 'Frame' class inside the 'tkinter' module
    and is responsible for creating the 'Stopwatch' frame, which is to
    functon as the programs stopwatch page. Here is where a usable stopwatch
    is created.

    Instance Attributes
    -------------------
    stopwatch_key : bool
        Used to allow or prevent the stopwatch from running.
    HMS_key : bool
        Lets the stopwatch know from what time to begin running from.
    record_laps : int
        Used to keep track of the number of laps being displayed.
    new_time : str
        Is continuously assigned the present hour, minute, and second.
    new_deci : str
        Is continuously assigned the present decisecond.
    old_time : str
        Stores the present hour, minute, and second for later use.
    old_deci : str
        Stores the present decisecond for later use.

    Methods
    -------
    clear_stopwatch()
        Stops and resets the stopwatch and laps for reuse.
    pause_stopwatch()
        Stops the the stopwatch from running.
    start_stopwatch()
        Begins running the stopwatch.
    record_lap()
        Displays present lap and the difference relative to the previous.
    """

    def __init__(self, parent, controller):
        """
        Parameters
        ----------
        parent : tkinter.Frame
            Required to represent the widgets in this class.
        controller : __main__.Clockity_Window
            Allows 'r_frame()' and 'sounds()', defined in the 'Clockity_Window'
            class, to be called from within this class.
        """

        tk.Frame.__init__(self, parent)     # Initializes 'Frame'

        self.stopwatch_key = True
        self.HMS_key = True
        self.recorded_laps = 0
        self.new_time = ''
        self.new_deci = ''
        self.old_time = ''
        self.old_deci = ''

        def clear_stopwatch():
            """Stops and resets the stopwatch and laps for reuse."""

            controller.sounds(2)

            self.stopwatch_key = False
            self.HMS_key = True
            self.recorded_laps = 0

            lap_button.configure(text=' ', bg=self.cget('bg'), command=None)
            lap_display.configure(state='normal')
            lap_display.delete('1.0', 'end')
            lap_display.configure(state='disabled')

            stopwatch_time_label.configure(text='00:00:00')
            stopwatch_mini_time_label.configure(text='.0')
            start_stopwatch_button.configure(
                text='Start',
                bg='green',
                command=start_stopwatch
            )

        def pause_stopwatch():
            """Stops the stopwatch from running.

            Can only be called if the stopwatch is currently running.
            """

            controller.sounds(2)

            self.stopwatch_key = False
            self.HMS_key = False

            lap_button.configure(text=' ', bg=self.cget('bg'), command=None)
            start_stopwatch_button.configure(
                text='Cont.',
                bg='blue',
                command=start_stopwatch
            )

        def start_stopwatch():
            """Begins running the stopwatch.

            Can only be called if the stopwatch isn't currently running.
            """

            controller.sounds(2)
            self.stopwatch_key = True

            lap_button.configure(text='Lap', bg='green', command=record_lap)
            start_stopwatch_button.configure(
                text='Pause',
                command=pause_stopwatch
                )

            # Used to let the stopwatch know what time
            # to begin running from
            if self.HMS_key is True:
                hours = 0
                minutes = 0
                seconds = 0
                deci_sec = 0
            else:
                hours = int(self.new_time[0:2])
                minutes = int(self.new_time[3:5])
                seconds = int(self.new_time[6:8])
                deci_sec = int(self.new_deci)

            # Runs and updates the stopwatch every decisecond.
            while self.stopwatch_key is True:

                self.new_time = (
                    str(hours).zfill(2) +
                    ':' +
                    str(minutes).zfill(2) +
                    ':' +
                    str(seconds).zfill(2)
                )
                self.new_deci = str(deci_sec)

                # Stops the stopwatch so the numbers wont
                # run off the screen
                if self.new_time == '99:59:59':
                    stopwatch_time_label.configure(text='Overflow')
                    stopwatch_mini_time_label.configure(text='')
                    lap_button.configure(
                        text='',
                        bg=self.cget('bg'),
                        command=None
                    )
                    break

                else:
                    stopwatch_time_label.configure(text=self.new_time)
                    stopwatch_mini_time_label.configure(
                        text='.' +
                        self.new_deci
                    )
                    self.update()

                # Pauses the while loop for 0.087 seconds. Used
                # so the while loop takes about one decisecond
                # per run.
                time.sleep(0.087)
                deci_sec += 1
                if deci_sec == 10:
                    deci_sec = 0
                    seconds += 1
                    if seconds == 60:
                        seconds = 0
                        minutes += 1
                        if minutes == 60:
                            minutes = 0
                            hours += 1

        def record_lap():
            """Displays present lap and difference relative to the previous.

            Can only be called if the stopwatch is currently running.
            """

            if self.stopwatch_key is True:

                controller.sounds(2)
                self.recorded_laps += 1
                lap_display.configure(state='normal')

                # Used displays the first lap and difference.
                if self.recorded_laps == 1:

                    difference = self.new_time + '.' + self.new_deci

                    lap_display.insert(
                        'end',
                        str(self.recorded_laps) +
                        '|     ' +
                        str(difference) +
                        '     |     ' +
                        str(difference) +
                        '\n'
                    )
                    lap_display.see('end')

                    self.old_time = self.new_time
                    self.old_deci = self.new_deci

                # Used to display the lap and difference when there is at least
                # one lap on display.
                else:

                    # Finds the difference between the new lap and the previous
                    diff_d = int(self.new_deci) - int(self.old_deci)
                    diff_s = int(self.new_time[6:8]) - int(self.old_time[6:8])
                    diff_m = int(self.new_time[3:5]) - int(self.old_time[3:5])
                    diff_h = int(self.new_time[0:2]) - int(self.old_time[0:2])
                    if diff_d < 0:
                        diff_d = 10 - -diff_d
                        diff_s -= 1
                    if diff_s < 0:
                        diff_s = 60 - -diff_s
                        diff_m -= 1
                    if diff_m < 0:
                        diff_m = 60 - -diff_m
                        diff_h -= 1

                    difference = (
                        str(diff_h).zfill(2) +
                        ':' +
                        str(diff_m).zfill(2) +
                        ':' +
                        str(diff_s).zfill(2) +
                        '.' +
                        str(diff_d)
                    )

                    lap_display.insert(
                        'end',
                        str(self.recorded_laps) +
                        '|     ' +
                        self.new_time +
                        '.' +
                        self.new_deci +
                        '     |     ' +
                        str(difference) +
                        '\n'
                    )
                    lap_display.see('end')

                    self.old_time = self.new_time
                    self.old_deci = self.new_deci

                lap_display.configure(state='disabled')

        # Displays the hours, minutes, and seconds on the stopwatch
        stopwatch_time_label = tk.Label(
            self,
            text='00:00:00', font=('Arial', 58, 'bold')
        )
        stopwatch_time_label.grid(row=0, columnspan=2, stick='w')

        # Displays the deciseconds on the stopwatch
        stopwatch_mini_time_label = tk.Label(
            self,
            text='.0', font=('Arial', 20, 'bold')
        )
        stopwatch_mini_time_label.grid(row=0, columnspan=1, sticky='se')

        start_stopwatch_button = tk.Button(
            self,
            text='Start', font=('Arial', 20, 'bold'),
            fg='black', bg='green',
            height=0, width=7,
            command=start_stopwatch
        )
        start_stopwatch_button.grid(row=1, columnspan=2, sticky='w')

        lap_button = tk.Button(
            self,
            text='', font=('Arial', 20, 'bold'),
            fg='black', bg=self.cget('bg'),
            height=0, width=7
        )
        lap_button.grid(row=1, columnspan=2)

        clear_stopwatch_button = tk.Button(
            self,
            text='Clear', font=('Arial', 20, 'bold'),
            fg='black', bg='red',
            height=0, width=7,
            command=clear_stopwatch
        )
        clear_stopwatch_button.grid(row=1, columnspan=2, sticky='e')

        lap_display = tk.Text(
            self,
            font=('Arial', 10, 'bold'),
            height=8, width=21,
            state='disabled'
        )
        lap_display.grid(row=2, column=0, sticky='we')

        lap_display_scrollbar = tk.Scrollbar(
            self,
            orient='vertical',
            command=lap_display.yview
        )
        lap_display.configure(yscrollcommand=lap_display_scrollbar.set)
        lap_display_scrollbar.grid(row=2, column=0, sticky='nse')

        back_button_1 = tk.Button(
            self,
            text='<-- Back', font=('Arial', 10, 'bold'),
            fg='black', bg='blue',
            height=3, width=44,
            command=lambda: [
                controller.r_frame(Home),
                clear_stopwatch()
                ]
        )
        back_button_1.grid(row=3, column=0, sticky='w')


class CountDown(tk.Frame):
    """Creates the CountDown frame and a working countdown.

    This class inherits from the 'Frame' class inside the 'tkinter' module
    and is responsible for creating the 'Countdown' frame, which is to
    function as the programs countdown page. Here is where a usable countdown
    is created.

    Attributes
    ----------
    number_key : bool
        Used to allow or prevent the number buttons from being used.
    countdown_key : bool
        Used to allow or prevent the countdown from running.
    time_update : str
        Assigned up to six numbers entered by the user.
    updated_time : str
        The numbers entered; converted and formatted as an actual time.
    updated_deci : int
        The deciseconds on the countdown.
    alarm_key : int
        An integer letting the alarm know for how long to sound for.

    Methods
    -------
    format_number_inputs()
        Formats the numbers entered as 'hours:minutes:seconds'.
    number_buttons(num)
        Stores numbers entered using the number buttons.
    clear_countdown()
        Stops and resets the countdown for reuse.
    pause_countdown()
        Stops the countdown from running.
    start_countdown()
        Begins running the countdown.
    set_countdown()
        Converts the numbers entered as an actual time.
    """

    def __init__(self, parent, controller):
        """
        Parameters
        ----------
        parent : tkinter.Frame
            Required to represent the widgets in this class.
        controller : __main__.Clockity_Window
            Allows 'r_frame()' and 'sounds()', defined in the 'Clockity_Window'
            class, to be called from within this class.
        """

        tk.Frame.__init__(self, parent)     # Initializes 'Frame'

        self.number_key = True
        self.countdown_key = False
        self.time_update = ''
        self.updated_time = ''
        self.updated_deci = 0
        self.alarm_key = 0

        def format_number_inputs():
            """Formats the numbers entered as 'hours:minutes:seconds'.

            Can only be called through 'number_buttons()' as numbers
            are being entered.
            """

            if len(self.time_update) == 1:
                self.updated_time = '00:00:0' + self.time_update
            elif len(self.time_update) == 2:
                self.updated_time = '00:00:' + self.time_update
            elif len(self.time_update) == 3:
                self.updated_time = (
                    '00:0' +
                    self.time_update[0] +
                    ':' +
                    self.time_update[1:3]
                )
            elif len(self.time_update) == 4:
                self.updated_time = (
                    '00:' +
                    self.time_update[0:2] +
                    ':' +
                    self.time_update[2:4]
                )
            elif len(self.time_update) == 5:
                self.updated_time = (
                    '0' +
                    self.time_update[0] +
                    ':' +
                    self.time_update[1:3] +
                    ':' +
                    self.time_update[3:5]
                )
            elif len(self.time_update) == 6:
                self.updated_time = (
                    self.time_update[0:2] +
                    ':' +
                    self.time_update[2:4] +
                    ':' +
                    self.time_update[4:6]
                )

            # Displays the newly formatted time on the countdown
            countdown_time_label.configure(text=self.updated_time)

        def number_buttons(num):
            """Stores the numbers entered using the number buttons.

            Function will do nothing if 'number_key is False'.
            Therefore the number buttons do nothing while the
            countdown is in use.

            Parameters
            ----------
            num : int
                The number entered by the user through the number buttons.
            """

            # Wont allow this function to do anything if the countdown
            # is currently in use.
            if self.number_key is True:

                # Allows '0' to be entered only if at least one other
                # number has been entered.
                if num == 0:
                    if len(self.time_update) == 0:
                        pass
                    elif len(self.time_update) < 6:
                        controller.sounds(2)
                        self.time_update = self.time_update + str(num)
                        format_number_inputs()

                elif num != 0:
                    if len(self.time_update) < 6:
                        controller.sounds(2)
                        self.time_update = self.time_update + str(num)
                        format_number_inputs()

        def clear_countdown():
            """Stops and resets the countdown for reuse."""

            controller.sounds(2)

            self.countdown_key = False
            self.time_update = ''
            self.updated_deci = 0
            self.number_key = True

            # Used to stop the alarm if it is currently ringing.
            self.alarm_key = 14

            set_countdown_button.configure(
                text='Set',
                bg='green',
                command=set_countdown
            )
            countdown_time_label.configure(
                text='00:00:00',
                font=('Arial', 58, 'bold')
            )
            countdown_mini_time_label.configure(text='.0')

        def pause_countdown():
            """Pauses the countdown.

            Can only be called after starting or continuing
            the countdown.
            """

            controller.sounds(2)
            self.countdown_key = False

            set_countdown_button.configure(
                text='Cont.',
                bg='blue',
                command=start_countdown
            )

        def start_countdown():
            """Begins the countdown.

            This function can only be called after pressing the
            set button or after pausing the countdown.
            """

            controller.sounds(2)
            self.countdown_key = True
            set_countdown_button.configure(
                text='Pause',
                bg='blue',
                command=pause_countdown
            )

            # Stores the individual time units for use
            # in the while loop.
            if len(self.updated_time) < 9:
                hours = int(self.updated_time[0:2])
                minutes = int(self.updated_time[3:5])
                seconds = int(self.updated_time[6:8])
                deci_sec_2 = self.updated_deci
            else:
                hours = int(self.updated_time[0:3])
                minutes = int(self.updated_time[4:6])
                seconds = int(self.updated_time[7:9])
                deci_sec_2 = self.updated_deci

            # Runs and updates the countdown every decisecond
            while self.countdown_key is True:

                self.updated_time = (
                    str(hours).zfill(2) +
                    ':' +
                    str(minutes).zfill(2) +
                    ':' +
                    str(seconds).zfill(2)
                )
                self.updated_deci = deci_sec_2

                countdown_mini_time_label.configure(
                    text='.' +
                    str(self.updated_deci)
                )
                countdown_time_label.configure(text=self.updated_time)

                # Makes sure the time displayed doesn't run off the screen
                if len(self.updated_time) != 9:
                    countdown_time_label.configure(font=('Arial', 58, 'bold'))
                self.update()

                # Pauses the while loop for 0.087 seconds. Used
                # so the while loop takes about one decisecond
                # per run.
                time.sleep(0.087)
                deci_sec_2 -= 1
                if deci_sec_2 == -1:
                    deci_sec_2 = 9
                    seconds -= 1

                    # Stops the countdown and sets off an alarm
                    # once the time reaches zero.
                    if self.updated_time == '00:00:00':

                        self.alarm_key = 0
                        def_bg = self.cget('bg')
                        set_countdown_button.configure(
                            bg=def_bg,
                            text='',
                            command=lambda: None
                        )

                        while self.alarm_key < 14:
                            controller.sounds(3)

                            # Flashes the countdown display red
                            countdown_time_label.configure(bg='red')
                            countdown_mini_time_label.configure(bg='red')
                            random_label.configure(bg='red')
                            time.sleep(0.1)
                            self.update()
                            countdown_time_label.configure(bg=def_bg)
                            countdown_mini_time_label.configure(bg=def_bg)
                            random_label.configure(bg=def_bg)
                            time.sleep(0.1)
                            self.alarm_key += 1
                            self.update()

                        self.number_key = True
                        set_countdown_button.configure(
                            text='Set',
                            bg='green',
                            command=set_countdown
                        )
                        break

                    # Continues updating the countdown
                    # time once it is confirmed it hasn't
                    # run out of time.
                    if seconds == -1:
                        seconds = 59
                        minutes -= 1
                        if minutes == -1:
                            minutes = 59
                            hours -= 1

        def set_countdown():
            """Converts the numers entered as an actual time.

            Cannot be called when the countdown is running or is paused.
            If no numbers have been entered, this function will do nothing.
            """

            # Wont allow this function do anything
            # unless a number has been entered.
            if self.time_update == '':
                pass

            else:
                controller.sounds(2)
                self.time_update = ''
                self.number_key = False

                # Converts the entered numbers into an actual time
                hours = int(self.updated_time[0:2])
                minutes = int(self.updated_time[3:5])
                seconds = int(self.updated_time[6:8])
                if seconds > 59 or minutes > 59:
                    self.updated_time = (
                        str(hours +
                            (minutes // 60)).zfill(2) +
                        ':' +
                        str((minutes % 60) +
                            (seconds // 60)).zfill(2) +
                        ':' +
                        str(seconds % 60).zfill(2)
                    )

                    # Makes sure the time is properly displayed.
                    if len(self.updated_time) == 9:
                        countdown_time_label.configure(
                            text=self.updated_time,
                            font=('Arial', 52, 'bold')
                        )
                        set_countdown_button.configure(
                            text='Start',
                            command=start_countdown
                        )
                    else:

                        countdown_time_label.configure(text=self.updated_time)
                        set_countdown_button.configure(
                            text='Start',
                            command=start_countdown
                        )

                # Used if the numbers entered already constitute an actual
                # time.
                else:
                    set_countdown_button.configure(
                        text='Start',
                        command=start_countdown
                    )

        # Used to fill blank areas around the countdown
        random_label = tk.Label(
            self,
            height=4, width=6
        )
        random_label.grid(row=0, columnspan=6, sticky='ne')

        # Displays the hours, minutes, and seconds on the countdown
        countdown_time_label = tk.Label(
            self,
            text='00:00:00', font=('Arial', 58, 'bold')
        )
        countdown_time_label.grid(row=0, columnspan=6, sticky='w')

        # Displays the deciseconds on the countdown
        countdown_mini_time_label = tk.Label(
            self,
            width=2,
            text='.0', font=('Arial', 24, 'bold')
        )
        countdown_mini_time_label.grid(row=0, columnspan=6, sticky='se')

        number_button_0 = tk.Button(
            self,
            text='0', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(0)
        )
        number_button_0.grid(row=2, column=0)

        number_button_1 = tk.Button(
            self,
            text='1', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(1)
        )
        number_button_1.grid(row=2, column=1)

        number_button_2 = tk.Button(
            self,
            text='2', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(2)
        )
        number_button_2.grid(row=2, column=2)

        number_button_3 = tk.Button(
            self,
            text='3', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(3)
        )
        number_button_3.grid(row=2, column=3)

        number_button_4 = tk.Button(
            self,
            text='4', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(4)
        )
        number_button_4.grid(row=2, column=4)

        number_button_5 = tk.Button(
            self,
            text='5', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(5)
        )
        number_button_5.grid(row=1, column=0)

        number_button_6 = tk.Button(
            self,
            text='6', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(6)
        )
        number_button_6.grid(row=1, column=1)

        number_button_7 = tk.Button(
            self,
            text='7', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(7)
        )
        number_button_7.grid(row=1, column=2)

        number_button_8 = tk.Button(
            self,
            text='8', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(8)
        )
        number_button_8.grid(row=1, column=3)

        number_button_9 = tk.Button(
            self,
            text='9', font=('Arial', 25, 'bold'),
            fg='black', bg='green',
            command=lambda: number_buttons(9)
        )
        number_button_9.grid(row=1, column=4)

        set_countdown_button = tk.Button(
            self,
            text='Set', font=('Arial', 25, 'bold'),
            width=5,
            fg='black', bg='green',
            command=set_countdown
        )
        set_countdown_button.grid(row=1, column=5)

        clear_countdown_button = tk.Button(
            self,
            text='Clear', font=('Arial', 25, 'bold'),
            fg='black', bg='grey',
            command=clear_countdown
        )
        clear_countdown_button.grid(row=2, column=5)

        # Used to create extra space between
        # the back button and the number buttons.
        random_label_2 = tk.Label(
            self,
            height=3
        )
        random_label_2.grid(row=3, column=0)

        back_button_2 = tk.Button(
            self,
            text='<--Back', font=('Arial', 10, 'bold'),
            fg='black', bg='blue',
            height=4, width=44,
            command=lambda: [
                controller.r_frame(Home),
                clear_countdown()
                ]
        )
        back_button_2.grid(row=4, columnspan=6)


app = Clockity_Window()
app.mainloop()
