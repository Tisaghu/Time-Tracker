# Time Tracker

This is a time tracking app developed with Flask. The goal of this project is to eventually replace my current time tracking app on my phone and to improve my skills in Flask web development.

### Features
- Track your time by selecting categories.
- Start and stop timers for each category.
- Save time entries in a CSV file for easy access and analysis.
- Add, edit, and delete categories.
- View time usage in a simple, user-friendly interface.

### Requirements
- Python 3.x
- Flask

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Tisaghu/Time-Tracker.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Time-Tracker
    ```

3. Create and activate the virtual environment:
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

1. Navigate to the `Time-Tracker` directory (if not already there):
    ```bash
    cd Time-Tracker
    ```

2. Run the Flask development server:
    ```bash
    flask run
    ```

3. Open your browser and go to `http://127.0.0.1:5000` to start using the app.

### Future Enhancements
- Add graph visualizations for time usage.
- Implement user authentication for personalized tracking.
