import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_ace import st_ace
import io
import sys

# Set page config to wide layout
st.set_page_config(layout="wide")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'progress' not in st.session_state:
    st.session_state['progress'] = []

# Main title
st.title("Learn Pandas and Matplotlib with Streamlit")

# File uploader
st.header("Upload Your Dataset")
uploaded_file = st.file_uploader("Drag and drop a CSV file here", type="csv")
if uploaded_file is not None:
    try:
        st.session_state['df'] = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("### Preview of Uploaded Dataset")
        st.dataframe(st.session_state['df'].head())
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.session_state['df'] = None

# Stop if no dataset is loaded
if st.session_state['df'] is None:
    st.warning("Please upload a CSV file to proceed.")
    st.stop()

# Define learning stages
stages = [
    {"name": "Introduction to Pandas", 
     "desc": "Learn to load and inspect data with Pandas.", 
     "example": "import pandas as pd\n\n# Show first 5 rows\nprint(df.head())", 
     "task": "Display the first 5 rows of the dataset using `print(df.head())`."},
    {"name": "Data Cleaning - Missing Values", 
     "desc": "Check for missing values in your dataset.", 
     "example": "# Check missing values\nprint(df.isnull().sum())", 
     "task": "Show the count of missing values per column with `print(df.isnull().sum())`."},
    {"name": "Data Cleaning - Drop Missing Values", 
     "desc": "Remove rows with missing values.", 
     "example": "# Drop rows with missing values\ndf_cleaned = df.dropna()\nprint(df_cleaned.head())", 
     "task": "Drop rows with missing values, assign to `df_cleaned`, and show the first 5 rows with `print(df_cleaned.head())`."},
    {"name": "Data Selection - Columns", 
     "desc": "Select specific columns from the DataFrame.", 
     "example": "# Select columns\nprint(df[['column1', 'column2']])", 
     "task": "Select and display two columns of your choice with `print(df[['col1', 'col2']])`."},
    {"name": "Data Selection - Rows (Filtering)", 
     "desc": "Filter rows based on a condition.", 
     "example": "# Filter rows\nprint(df[df['column'] > value])", 
     "task": "Filter rows where a numeric column exceeds a value, e.g., `print(df[df['col'] > 10])`."},
    {"name": "Descriptive Statistics", 
     "desc": "Calculate summary statistics for numeric columns.", 
     "example": "# Summary stats\nprint(df.describe())", 
     "task": "Show descriptive statistics with `print(df.describe())`."},
    {"name": "Value Counts", 
     "desc": "Count occurrences in a categorical column.", 
     "example": "# Value counts\nprint(df['column'].value_counts())", 
     "task": "Display value counts for a categorical column with `print(df['col'].value_counts())`."},
    {"name": "Basic Line Plot", 
     "desc": "Create a line plot of a numeric column.", 
     "example": "import matplotlib.pyplot as plt\n\nplt.figure(figsize=(6, 4))\nplt.plot(df['numeric_col'])\nplt.title('Line Plot')\nst.pyplot(plt)", 
     "task": "Plot a numeric column with `plt.plot(df['col'])`, add a title, and display with `st.pyplot(plt)`."},
    {"name": "Scatter Plot", 
     "desc": "Create a scatter plot of two numeric columns.", 
     "example": "import matplotlib.pyplot as plt\n\nplt.figure(figsize=(6, 4))\nplt.scatter(df['col1'], df['col2'])\nplt.title('Scatter Plot')\nst.pyplot(plt)", 
     "task": "Make a scatter plot with `plt.scatter(df['col1', df['col2'])`, add a title, and show with `st.pyplot(plt)`."},
    {"name": "Bar Chart", 
     "desc": "Create a bar chart from categorical data.", 
     "example": "import matplotlib.pyplot as plt\n\nplt.figure(figsize=(6, 4))\ndf['col'].value_counts().plot(kind='bar')\nplt.title('Bar Chart')\nst.pyplot(plt)", 
     "task": "Plot a bar chart of value counts with `df['col'].value_counts().plot(kind='bar')`, add a title, and use `st.pyplot(plt)`."},
    {"name": "Histograms", 
     "desc": "Visualize a numeric column’s distribution.", 
     "example": "import matplotlib.pyplot as plt\n\nplt.figure(figsize=(6, 4))\nplt.hist(df['numeric_col'], bins=10)\nplt.title('Histogram')\nst.pyplot(plt)", 
     "task": "Create a histogram with `plt.hist(df['col'], bins=10)`, add a title, and display with `st.pyplot(plt)`."},
    {"name": "Groupby and Aggregation", 
     "desc": "Group data and compute aggregates.", 
     "example": "# Group and aggregate\nprint(df.groupby('cat_col')['num_col'].mean())", 
     "task": "Group by a categorical column and show the mean of a numeric column with `print(df.groupby('cat_col')['num_col'].mean())`."},
    {"name": "Sorting DataFrames", 
     "desc": "Sort the DataFrame by a column.", 
     "example": "# Sort DataFrame\ndf_sorted = df.sort_values(by='column')\nprint(df_sorted.head())", 
     "task": "Sort by a column, assign to `df_sorted`, and show the head with `print(df_sorted.head())`."},
    {"name": "Adding New Columns", 
     "desc": "Add a new column to the DataFrame.", 
     "example": "# Add column\ndf['new_col'] = df['col1'] + df['col2']\nprint(df.head())", 
     "task": "Add a new column (e.g., `df['new_col'] = df['col1'] * 2`) and show the head with `print(df.head())`."},
    {"name": "Renaming Columns", 
     "desc": "Rename a column in the DataFrame.", 
     "example": "# Rename column\ndf = df.rename(columns={'old': 'new'})\nprint(df.head())", 
     "task": "Rename a column (e.g., `df = df.rename(columns={'old': 'new'})`) and show the head with `print(df.head())`."},
]

# Single sidebar layout
with st.sidebar:
    # Instructions first
    st.title("Instructions")
    st.write("**How to Use:**")
    st.write("- Upload a CSV file to start.")
    st.write("- Select a stage from the dropdown below.")
    st.write("- Study the example and task.")
    st.write("- Write code in the editor.")
    st.write("- Use `print()` for text output (e.g., DataFrames).")
    st.write("- Use `st.pyplot(plt)` for plots.")
    st.write("- Click 'Run Code' to see results.")
    st.write("- Mark the stage complete when done.")
    st.write("---")

    # Stage selection
    st.write("### Select a Stage")
    current_stage = st.selectbox("Choose a stage", [s["name"] for s in stages], label_visibility="collapsed")
    st.write("---")

    # Ticked-off stages
    st.write("### Progress")
    for stage in stages:
        status = "✅" if stage["name"] in st.session_state['progress'] else "⬜"
        st.write(f"{status} {stage['name']}")

# Display stage content in main area
def display_stage(stage_name):
    stage = next(s for s in stages if s["name"] == stage_name)
    st.header(stage["name"])
    st.write(stage["desc"])

    st.subheader("Example Code")
    st.code(stage["example"], language="python")

    st.subheader("Your Task")
    st.write(stage["task"])

    # Code editor
    st.write("Enter your code here:")
    code = st_ace(
        language="python",
        theme="monokai",
        key=f"editor_{stage_name}",
        height=200,
        show_gutter=True,
        wrap=True,
        value=""
    )

    # Run button
    if st.button("Run Code", key=f"run_{stage_name}"):
        if not code or code.strip() == "":
            st.warning("Please enter code to run!")
            return

        # Define globals for exec
        globals_dict = {
            'st': st,
            'df': st.session_state['df'],
            'pd': pd,
            'plt': plt
        }

        # Capture output
        output_io = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = output_io

        try:
            plt.close('all')  # Clear all previous figures
            exec(code, globals_dict)
            sys.stdout = sys_stdout
            output_text = output_io.getvalue()

            if output_text:
                st.subheader("Text Output")
                # Parse output to detect DataFrame or Series and display as table
                try:
                    lines = output_text.strip().split('\n')
                    last_output = lines[-1] if lines else ""
                    if ' ' in last_output and any(c.isdigit() for c in last_output):
                        local_vars = {}
                        exec(code, globals_dict, local_vars)
                        for var in local_vars.values():
                            if isinstance(var, (pd.DataFrame, pd.Series)):
                                st.dataframe(var)
                                break
                        else:
                            st.code(output_text, language=None)
                    else:
                        st.code(output_text, language=None)
                except Exception:
                    st.code(output_text, language=None)
            else:
                st.info("No text output. Use `print()` to display results.")

            # Display plot if created
            if plt.get_fignums():  # Check if a figure exists
                st.subheader("Plot Output")
                fig = plt.gcf()  # Get current figure
                fig.set_size_inches(6, 4)  # Set smaller size
                st.pyplot(fig)
                plt.close(fig)  # Close the figure after display

            st.success("Code ran successfully!")
            
            # Detailed explanation based on the code
            st.write("#### What This Code Does:")
            explanation = f"This code executed the task: \"{stage['task']}\"\n\nHere’s what it did:\n"
            
            if "df.describe()" in code:
                explanation += "- **Descriptive Statistics**: You used `df.describe()` to compute summary statistics for numeric columns in the DataFrame. This includes:\n  - **count**: Number of non-null entries.\n  - **mean**: Average value.\n  - **std**: Standard deviation (spread of data).\n  - **min**: Minimum value.\n  - **25%**: 25th percentile (value below which 25% of the data falls).\n  - **50%**: Median (middle value, 50th percentile).\n  - **75%**: 75th percentile (value below which 75% of the data falls).\n  - **max**: Maximum value."
            
            elif "df.dropna()" in code:
                explanation += "- **Dropping Missing Values**: You used `df.dropna()` to remove rows containing any missing (NaN) values from the DataFrame. This creates a new DataFrame (`df_cleaned`) with only complete rows, ensuring no gaps in the data for further analysis."
            
            elif "df[[" in code and "]]" in code:
                explanation += "- **Column Selection**: You selected specific columns from the DataFrame using `df[['col1', 'col2']]`. This extracts only the named columns, creating a new DataFrame with just those subsets of the original data."
            
            elif "df[df[" in code:
                explanation += "- **Row Filtering**: You filtered rows based on a condition (e.g., `df[df['col'] > value]`). This keeps only the rows where the condition is true, reducing the DataFrame to a subset that meets your criteria."
            
            elif "df['" in code and ".value_counts()" in code:
                explanation += "- **Value Counts**: You used `.value_counts()` on a column (e.g., `df['col'].value_counts()`) to count the frequency of each unique value in that column. This is useful for understanding the distribution of categorical data."
            
            elif "plt.plot(" in code:
                explanation += "- **Line Plot**: You created a line plot with `plt.plot()`. This connects data points in a numeric column with a continuous line, showing trends or patterns over the data’s index."
            
            elif "plt.scatter(" in code:
                explanation += "- **Scatter Plot**: You created a scatter plot with `plt.scatter()`. This plots individual points for two numeric columns, showing their relationship without connecting them."
            
            elif ".plot(kind='bar')" in code:
                explanation += "- **Bar Chart**: You created a bar chart with `.plot(kind='bar')`. This displays categorical data as bars, where the height represents the count or value of each category."
            
            elif "plt.hist(" in code:
                explanation += "- **Histogram**: You created a histogram with `plt.hist()`. This shows the distribution of a numeric column by grouping values into bins (e.g., `bins=10`), with bar heights indicating frequency."
            
            elif "df.groupby(" in code:
                explanation += "- **Grouping and Aggregation**: You used `df.groupby()` to group the DataFrame by a categorical column and applied an aggregation (e.g., `.mean()`) to summarize a numeric column for each group."
            
            elif "df.sort_values(" in code:
                explanation += "- **Sorting**: You sorted the DataFrame with `df.sort_values(by='col')`, ordering rows based on the values in the specified column, either ascending or descending."
            
            elif "df['" in code and "=" in code and not ".value_counts()" in code:
                explanation += "- **Adding a Column**: You added a new column to the DataFrame (e.g., `df['new_col'] = ...`). This creates or modifies a column based on an operation, such as adding two existing columns or applying a calculation."
            
            elif "df.rename(" in code:
                explanation += "- **Renaming Columns**: You used `df.rename(columns={'old': 'new'})` to change the name of one or more columns in the DataFrame, making it more readable or consistent."

            if "st.pyplot(plt)" in code:
                explanation += "\n- **Displaying the Plot**: You used `st.pyplot(plt)` to render the Matplotlib plot in the Streamlit app."

            st.write(explanation)

        except Exception as e:
            sys.stdout = sys_stdout
            st.error(f"Error: {e}")
            st.exception(e)
        finally:
            sys.stdout = sys_stdout  # Always restore stdout

    # Mark as complete
    if st.button("Mark as Complete", key=f"complete_{stage_name}"):
        if stage_name not in st.session_state['progress']:
            st.session_state['progress'].append(stage_name)
            st.success(f"{stage_name} completed!")
            st.rerun()

# Show the selected stage
display_stage(current_stage)