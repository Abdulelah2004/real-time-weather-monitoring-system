# real-time-weather-monitoring-system
this is my article used code for software design pattern course a real time weather monitoring system using python programming language 


Here's a professional `README.md` file for your GitHub repository:

```markdown
# 🌦 Real-Time Weather Monitoring System

A Python implementation of the Observer design pattern for real-time weather data visualization and logging.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

## 📌 Features

- **Observer Pattern Implementation**: Demonstrates clean separation between data source and displays
- **Real-time Monitoring**: Simulates weather data updates every 2 seconds
- **Multiple Display Formats**:
  - Graphical UI (Tkinter)
  - CSV data logging
  - Live Matplotlib graphs
- **Thread-safe Design**: Background data generation with main thread GUI updates
- **Export Capability**: Save weather data to CSV with one click

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Abdulelah2004/real-time-weather-monitoring-system.git
   cd real-time-weather-monitoring-system
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the application:
```bash
python weather_monitor.py
```

The system will:
1. Display current weather metrics (temperature, humidity, pressure)
2. Update a live graph showing trends
3. Log all data to `weather_log.csv`

## 🧩 System Architecture

```
[WeatherData Subject]
       │
       ├── WeatherDisplay (Tkinter UI)
       ├── WeatherLogger (CSV Writer)
       └── WeatherGraph (Matplotlib Plot)
```

## 📚 Design Patterns Used

- **Observer Pattern**: For decoupled data-display architecture
- **Abstract Base Classes**: To enforce interface contracts
- **Threading**: For concurrent data generation and UI updates

## 📝 Requirements

- Python 3.9+
- Packages:
  - `tkinter` (standard library)
  - `matplotlib` (for visualization)
  - `csv`, `random`, `threading` (standard libraries)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Developed by [Abdulelah Ahmed](https://github.com/Abdulelah2004)


