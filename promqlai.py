# -*- coding: utf-8 -*-
"""PromQLai.ipynb
"""

pip install litellm

import openai
import requests
import re
import json
from prometheus_api_client import PrometheusConnect
import datetime

client = openai.OpenAI(
    api_key="",
    base_url=""
)

system_prompt1 = """
You are an expert in monitoring and observability, specializing in Thanos and Prometheus. Your task is to generate valid PromQL (Prometheus Query Language) queries for Thanos based on user requests. Follow these guidelines:

1. **Understand the Request**:
   - The user will describe the metric or data they want to query (e.g., CPU usage, HTTP requests, target status).
   - Identify the metric name and any relevant labels (e.g., `job`, `instance`).
   - Check what is asked hour, minutes, months, etc.

2. **Generate PromQL Queries**:
   - Use PromQL syntax to create the query.
   - For calculating total usage over time, use the sum_over_time() function.
   - For time-series data, use functions like rate(), sum(), or avg() as needed.
   - For instant queries, return the current value of the metric.
   - For range queries, specify the time range using [time] (e.g., [5m] for the last 5 minutes).
   - Use correct metrics name.

3. **Examples**:
   - User: "Get the HTTP request rate over the last 5 minutes."
     Query: rate(http_requests_total[5m]
   - User: "Check if all targets are up."
     Query: up
   - User: "Get the total memory usage for a specific job."
     Query: sum(memory_usage{job="my-service"})
   - User: "Calculate the total GPU usage over the past year, aggregated at 1-hour intervals."
     Query: sum_over_time(namespace_gpu_usage[1y:1h])

4. **Clarify Ambiguities**:
   - If the user's request is unclear, ask for clarification (e.g., "Which job or instance are you interested in?").

5. **Output**:
   - Return only the PromQL query, no inverted commas.
   - Do not include explanations unless explicitly asked.

Now, generate a query based on the user's request.
"""

# # Define the user's request
# user_prompt1 = "a scatter plot that visualizes CPU vs. GPU usage per namespace over the last year"
user_prompt1 = """
Get GPU usage over last month in an hour interval. And use a scatter plot to visualize it over time.
"""

def generate_promql_query(user_prompt, system_prompt):
    """
    Generate a PromQL query using the AI agent.
    """
    response = client.chat.completions.create(
    model="llama3", # model to send to the proxy
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",  # User's request
            "content": user_prompt
        }
    ])
    prompt_query = response.choices[0].message.content
    return prompt_query

queries = generate_promql_query(user_prompt1, system_prompt1)

print(queries)

queries

import requests
def fetch_data(query):

  url = "https://thanos.nrp-nautilus.io/api/v1/query"

  # Send the GET request
  response = requests.get(url, params={'query': query})
  data = response.json()
  return data
 

llm1_data = fetch_data(queries)

llm1_data

# system_prompt2= """You are an expert in data visualization. Your task is to a generate plots based on time-series data fetched from Thanos. Follow these guidelines:

# 1. **Understand the Data**:
#    - The data consists of timestamps and corresponding values for a specific metric.
#    - The metric name and time range are provided.

# 2. **Generate Plots**:
#    - Use a plotting library (e.g., Matplotlib, Plotly) to visualize the data.
#    - For time-series data, create a line plot with timestamps on the x-axis and values on the y-axis.
#    - Add titles, labels, and grid lines for clarity.

# 3. **Examples**:
#    - Metric: `cpu_usage`, Time Range: `5m`
#      Plot: A line plot showing CPU usage over the last 5 minutes.
#    - Metric: `http_requests_total`, Time Range: `1h`
#      Plot: A line plot showing HTTP request rates over the last hour.

# 4. **Output**:
#    - Return the generated plot or a link to the visualization.

# Now, generate a plot based on the provided data.
# """

# system_prompt2 = """
#     You are a data visualization expert. Your task is to generate Python code to plot the fetched data. Follow these rules:
#     4. Use different colors.
#     5. Add proper labels, titles, and grid lines.
#     6. Return only the Python code as a string, without any explanations, markdown formatting, or additional text so that I can use exec() on the output and run directly in my notebook.
#     """

plot_prompt_template = """
Given the following data and user request, generate an appropriate plot.

User Request: "{user_request}"

Fetched Data (JSON format):
{fetched_data}

Instructions:
1. Parse the fetched data and convert timestamps into a readable format (e.g., datetime).
2. Choose the appropriate plot type based on the user request (e.g., scatter, line, bar).
3. Generate the plot using Matplotlib, Seaborn, or Plotly.
4. Return a Python script that processes the data and creates the requested visualization.
5. Return only the Python code as a string, without any comments, explanations, markdown formatting, or additional text.
6. Do not write python comments starting with "#" or "'''".

"""

# Prepare the system prompt
system_prompt2 = plot_prompt_template.format(user_request= user_prompt1, fetched_data=llm1_data)

type(system_prompt2)

fetched_data_str = json.dumps(llm1_data, indent=4)

def generate_plot_code(user_prompt, system_prompt):
    """
    Generate plots
    """
    response = client.chat.completions.create(
    model="llama3", # model to send to the proxy
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",  # User's request
            "content": user_prompt
        }
    ])
    plot = response.choices[0].message.content
    return plot

plot_code = generate_plot_code(fetched_data_str, system_prompt2)

plot_code

def clean_plot_code(plot_code):
    """Removes markdown-style code block indicators like ```python and ```"""
    plot_code = plot_code.replace("```python", "").replace("```", "").strip()
    return plot_code

# Clean the generated code before saving or executing
cleaned_plot_code = clean_plot_code(plot_code)

def save_plot_code(cleaned_plot_code, filename="generated_plot.py"):
    """Saves the generated Python code to a file."""
    with open(filename, "w") as f:
        f.write(cleaned_plot_code)

# Save the generated code
save_plot_code(cleaned_plot_code)

import generated_plot  # Import the generated script as a module

# If the function name is known (e.g., plot_gpu_usage)
data = fetched_data  # Pass the actual data
generated_plot.plot_gpu_usage(data)

help(prom)



