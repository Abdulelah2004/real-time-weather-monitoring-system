import tkinter as tk
from tkinter import ttk
import random, time, threading, csv, os
from datetime import datetime
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Observer Pattern ----------------
class Observer(ABC):
    @abstractmethod
    def update(self, temperature, humidity, pressure): pass

class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer): pass
    @abstractmethod
    def remove_observer(self, observer): pass
    @abstractmethod
    def notify_observers(self): pass

# ---------------- WeatherData (Subject) ----------------
class WeatherData(Subject):
    def __init__(self):
        self.observers = []
        self.temperature = self.humidity = self.pressure = 0

    def register_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.temperature, self.humidity, self.pressure)

    def set_measurements(self, temperature, humidity, pressure):
        self.temperature, self.humidity, self.pressure = temperature, humidity, pressure
        self.notify_observers()

# ---------------- Observers ----------------
class WeatherDisplay(Observer):
    def __init__(self, label):
        self.label = label

    def update(self, temperature, humidity, pressure):
        self.label.config(
            text=f"🌡 Temp: {temperature}°C\n💧 Humidity: {humidity}%\n📉 Pressure: {pressure} hPa"
        )

class WeatherLogger(Observer):
    def __init__(self, filename="weather_log.csv"):
        self.filename = filename
        with open(self.filename, 'w', newline='') as file:
            csv.writer(file).writerow(["Timestamp", "Temperature", "Humidity", "Pressure"])

    def update(self, temperature, humidity, pressure):
        with open(self.filename, 'a', newline='') as file:
            csv.writer(file).writerow([datetime.now(), temperature, humidity, pressure])

class WeatherGraph(Observer):
    def __init__(self, figure):
        self.temps, self.humids, self.pressures = [], [], []
        self.ax = figure.add_subplot(111)
        self.canvas = None

    def update(self, temperature, humidity, pressure):
        self.temps.append(temperature)
        self.humids.append(humidity)
        self.pressures.append(pressure)
        if len(self.temps) > 20:
            self.temps.pop(0)
            self.humids.pop(0)
            self.pressures.pop(0)
        self.refresh()

    def refresh(self):
        self.ax.clear()
        self.ax.plot(self.temps, 'r-', label='🌡 Temp (°C)', linewidth=2)
        self.ax.plot(self.humids, 'b--', label='💧 Humidity (%)', linewidth=1.5)
        self.ax.plot(self.pressures, 'g-.', label='📉 Pressure (hPa)', linewidth=1.5)
        self.ax.axhspan(22, 26, color='green', alpha=0.1, label='✅ Ideal Temp Zone')
        self.ax.set_title("📈 Weather Trends", fontsize=13, fontweight='bold')
        self.ax.set_xlabel("⏱ Time (latest 20)", fontsize=10)
        self.ax.set_ylabel("📊 Value", fontsize=10)
        self.ax.grid(True, linestyle='--', alpha=0.4)
        self.ax.legend(loc='upper right', fontsize=8)
        if self.canvas:
            self.canvas.draw()

# ---------------- Main App ----------------
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌦 Real-Time Weather Monitor")
        self.root.geometry("630x580")
        self.root.configure(bg="#f0f4f7")

        self.running = True
        self.weather_data = WeatherData()

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), background="#f0f4f7")
        style.configure("TButton", font=("Arial", 11), padding=6)

        # Display Area
        self.weather_label = ttk.Label(root, text="", anchor="center", font=("Arial", 16, "bold"))
        self.weather_label.pack(pady=20)

        display = WeatherDisplay(self.weather_label)
        self.logger = WeatherLogger()  # save the logger for export
        fig = plt.Figure(figsize=(5.5, 2.8), dpi=100)
        graph = WeatherGraph(fig)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack(pady=10)
        graph.canvas = canvas

        # Register Observers
        self.weather_data.register_observer(display)
        self.weather_data.register_observer(self.logger)
        self.weather_data.register_observer(graph)

        # Buttons
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="📄 Export CSV", command=self.export_csv).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="❌ Exit", command=self.quit_app).grid(row=0, column=1, padx=10)

        self.start_simulation()

    def start_simulation(self):
        def simulate():
            while self.running:
                temp = round(random.uniform(20, 35), 1)
                humid = round(random.uniform(40, 80), 1)
                press = round(random.uniform(1000, 1025), 1)
                self.weather_data.set_measurements(temp, humid, press)
                time.sleep(2)

        threading.Thread(target=simulate, daemon=True).start()

    def export_csv(self):
        try:
            os.startfile(self.logger.filename)
        except Exception as e:
            print("Error opening file:", e)

    def quit_app(self):
        self.running = False
        self.root.destroy()

# ---------------- Launch ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
