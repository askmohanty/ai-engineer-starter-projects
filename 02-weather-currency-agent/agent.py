"""Project 02: an agent that calls real APIs.

Uses two free APIs that need no key: Open-Meteo (weather) and Frankfurter
(exchange rates from the European Central Bank).

    python 02-weather-currency-agent/agent.py "Should I carry an umbrella in Pune tomorrow? And what's 500 USD in INR?"
"""

import sys

import httpx

from agentkit import Tool, run_agent

HTTP = httpx.Client(timeout=10)


def get_weather(city: str) -> dict:
    places = HTTP.get(
        "https://geocoding-api.open-meteo.com/v1/search", params={"name": city, "count": 1}
    ).raise_for_status().json()
    if not places.get("results"):
        raise ValueError(f"no place called {city!r}")
    place = places["results"][0]

    forecast = HTTP.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "auto",
            "forecast_days": 3,
        },
    ).raise_for_status().json()
    return {
        "place": f"{place['name']}, {place.get('country', '')}",
        "current": forecast["current"],
        "daily": forecast["daily"],
        "units": {"current": forecast["current_units"], "daily": forecast["daily_units"]},
    }


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    data = HTTP.get(
        "https://api.frankfurter.dev/v1/latest",
        params={"base": from_currency.upper(), "symbols": to_currency.upper()},
    ).raise_for_status().json()
    rate = data["rates"][to_currency.upper()]
    return {"rate": rate, "converted": round(amount * rate, 2), "rate_date": data["date"]}


TOOLS = [
    Tool(
        "get_weather",
        "Current weather and a 3-day forecast (max/min temperature, chance of rain) for a city.",
        {"city": {"type": "string"}},
        get_weather,
    ),
    Tool(
        "convert_currency",
        "Convert money using today's ECB reference rate. Currencies are ISO codes like USD, INR, EUR.",
        {
            "amount": {"type": "number"},
            "from_currency": {"type": "string"},
            "to_currency": {"type": "string"},
        },
        convert_currency,
    ),
]

SYSTEM = "You are a helpful travel assistant. Use the tools for live data and say which date a rate is from."

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Should I carry an umbrella in Pune tomorrow? And what's 500 USD in INR?"
    answer, _ = run_agent(question, TOOLS, SYSTEM)
    print(answer)
