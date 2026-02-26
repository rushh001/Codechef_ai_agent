# CodeChef AI Agent

An automated agent that scrapes a daily easy problem from CodeChef, generates a Python solution using the Groq LLM API, and submits it — all on a configurable schedule via a Flask web dashboard.

## Features

- **Automated scraping** – Fetches problems from the CodeChef *Basic Programming Concepts* practice section using Selenium.
- **AI-powered solving** – Sends the problem statement to the Groq API (`llama-3.3-70b-versatile`) and receives a ready-to-submit Python solution.
- **Automated submission** – Logs into CodeChef and submits the generated solution through the browser using `undetected-chromedriver`.
- **Web dashboard** – A Flask UI lets you run the agent immediately, schedule it at a specific time, or set a recurring interval.
- **Live output streaming** – Watch the agent's progress in real time via Server-Sent Events.
- **Persistent counter** – Tracks which problem was last fetched so each run picks the next one in the list.

## Project Structure

```
.
├── app.py           # Flask web server and scheduler
├── main.py          # Orchestrates the full solve-and-submit pipeline
├── scraper.py       # Selenium scraper – fetches problem name & link
├── parser.py        # Parses the problem statement from the problem page
├── ai_solver.py     # Calls the Groq API to generate a Python solution
├── tester.py        # (Optional) Runs the solution against sample inputs
├── submitter.py     # Logs into CodeChef and submits the solution
├── notifier.py      # Sends email notifications on completion
├── utils.py         # Logs solved problems to a local file
├── config.py        # Reads credentials from environment variables
├── counter.txt      # Tracks the current problem index
├── templates/
│   └── index.html   # Web dashboard UI
└── requirments.txt  # Python dependencies
```

## Prerequisites

- Python 3.9+
- Google Chrome installed
- ChromeDriver matching your Chrome version (managed automatically by `undetected-chromedriver`)

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/rushh001/Codechef_ai_agent.git
   cd Codechef_ai_agent
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirments.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   CODECHEF_USERNAME=your_codechef_username
   CODECHEF_PASSWORD=your_codechef_password
   GROQ_API_KEY=your_groq_api_key
   SMTP_EMAIL=your_email@example.com      # optional, for notifications
   SMTP_PASSWORD=your_email_password      # optional, for notifications
   ```

## Usage

### Run once (command line)

```bash
python main.py
```

### Run via the web dashboard

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser. From the dashboard you can:

- **Run Now** – Execute the agent immediately.
- **Schedule at time** – Run the agent once at a specific time each day (HH:MM format).
- **Run on interval** – Run the agent every *N* minutes (minimum 30 minutes).

Live output from the agent is streamed directly to the dashboard.

## Environment Variables

| Variable             | Description                                    | Required |
|----------------------|------------------------------------------------|----------|
| `CODECHEF_USERNAME`  | Your CodeChef account username                 | Yes      |
| `CODECHEF_PASSWORD`  | Your CodeChef account password                 | Yes      |
| `GROQ_API_KEY`       | API key for the Groq LLM service               | Yes      |
| `SMTP_EMAIL`         | Email address used to send notifications       | No       |
| `SMTP_PASSWORD`      | Password for the notification email account    | No       |

## How It Works

1. `scraper.py` opens the CodeChef practice page and extracts the problem at the current counter index, then increments the counter.
2. `parser.py` visits the problem link and extracts the full problem statement.
3. `ai_solver.py` sends the statement to the Groq API and returns a clean Python solution containing a `main()` function.
4. `submitter.py` opens CodeChef in a browser, logs in, navigates to the problem, injects the solution into the code editor, and clicks **Submit**.
5. `utils.py` records the problem name and submission status to the local log.

## License

This project is open source. Feel free to use and modify it.
