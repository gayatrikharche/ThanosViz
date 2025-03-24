# ThanosViz

This project automates the process of querying Thanos/Prometheus and visualizing the results using AI-powered systems. The pipeline involves the following steps:

### 1. **Generate PromQL Queries with AI**
   - I defined a system prompt to instruct an AI model to generate valid PromQL queries based on user input.
   - The AI interprets user requests (e.g., "Get GPU usage over the last month in hourly intervals") and formulates a corresponding PromQL query.

### 2. **Fetch Data from Thanos**
   - Once the PromQL query is generated, I send it to Thanos via an API request.
   - The response contains time-series data in JSON format, which I can use for visualization.

### 3. **Generate Plotting Code with AI**
   - I used another AI model to generate Python code for visualizing the fetched data.
   - The AI model decides on the appropriate plot type (e.g., scatter plot, line chart) based on the user's request.

### 4. **Execute the Generated Code**
   - I clean the generated Python code, save it as a script, and then execute it.
   - The Python code processes the fetched data and generates a plot, which I can view.
