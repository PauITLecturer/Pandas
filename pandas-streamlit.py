import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_ace import st_ace
import io
import sys
import numpy as np

# Set page config to wide layout
st.set_page_config(layout="wide", page_title="Learn Pandas & Matplotlib", page_icon="📊")

# Custom CSS for prettier design
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #e6f0ff;
        padding: 15px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stHeader {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
    }
    .stSubheader {
        color: #34495e;
        font-family: 'Arial', sans-serif;
    }
    .stMarkdown {
        font-family: 'Arial', sans-serif;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'current_stage_idx' not in st.session_state:
    st.session_state['current_stage_idx'] = 0

# Main title
st.title("📊 Paul’s Amazing Pandas & Matplotlib Learning Adventure")

# File uploader
st.header("Upload Your Dataset", anchor=None)
uploaded_file = st.file_uploader("Drag and drop a CSV file here", type="csv")
if uploaded_file is not None:
    try:
        st.session_state['df'] = pd.read_csv(uploaded_file)
        st.success("🎉 File uploaded successfully!")
        st.write("### Preview of Uploaded Dataset")
        st.dataframe(st.session_state['df'].head(), use_container_width=True)
    except Exception as e:
        st.error(f"🚨 Error loading CSV: {e}")
        st.session_state['df'] = None

# Stop if no dataset is loaded
if st.session_state['df'] is None:
    st.warning("⚠️ Please upload a CSV file to proceed.")
    st.stop()

# Define learning stages
stages = [
    {"name": "Basic Pandas - Shape", 
     "desc": "Learn about the dimensions of your DataFrame with shape.", 
     "example": "import pandas as pd\n\n# Show number of rows and columns\nprint(df.shape)", 
     "task": "Display the shape of the dataset using `print(df.shape)`."},
    {"name": "Basic Pandas - Head and Tail", 
     "desc": "Inspect the first and last rows of your dataset.", 
     "example": "# Show first 5 rows\nprint(df.head())\n# Show last 5 rows\nprint(df.tail())", 
     "task": "Display the first 5 rows with `print(df.head())` and last 5 rows with `print(df.tail())`."},
    {"name": "Basic Pandas - Data Types (dtypes)", 
     "desc": "Check the data types of each column.", 
     "example": "# Show data types\nprint(df.dtypes)", 
     "task": "Show the data types of all columns with `print(df.dtypes)`."},
    {"name": "Basic Pandas - Selecting a Single Column", 
     "desc": "Select one column from the DataFrame.", 
     "example": "# Select a single column\nprint(df['column_name'])", 
     "task": "Select and display one column with `print(df['col'])`."},
    {"name": "Basic Pandas - Selecting Multiple Columns", 
     "desc": "Select multiple columns from the DataFrame.", 
     "example": "# Select multiple columns\nprint(df[['col1', 'col2']])", 
     "task": "Select and display two columns with `print(df[['col1', 'col2']])`."},
    {"name": "Basic Pandas - Selecting Rows (Filtering)", 
     "desc": "Filter rows based on a condition.", 
     "example": "# Filter rows\nprint(df[df['column'] > 10])", 
     "task": "Filter rows where a numeric column exceeds a value, e.g., `print(df[df['col'] > 10])`."},
    {"name": "Basic Pandas - Value Counts", 
     "desc": "Count unique values in a column.", 
     "example": "# Count unique values\nprint(df['column'].value_counts())", 
     "task": "Display value counts for a categorical column with `print(df['col'].value_counts())`."},
    {"name": "Basic Pandas - loc", 
     "desc": "Select data by label using loc.", 
     "example": "# Select rows and columns by label\nprint(df.loc[0:2, ['col1', 'col2']])", 
     "task": "Use `loc` to select the first 3 rows of two columns, e.g., `print(df.loc[0:2, ['col1', 'col2']])`."},
    {"name": "Basic Pandas - iloc", 
     "desc": "Select data by position using iloc.", 
     "example": "# Select rows and columns by position\nprint(df.iloc[0:3, 0:2])", 
     "task": "Use `iloc` to select the first 3 rows and first 2 columns, e.g., `print(df.iloc[0:2, 0:2])`."},
    {"name": "Basic Data Cleaning - Describe", 
     "desc": "Get summary statistics of numeric columns.", 
     "example": "# Summary statistics\nprint(df.describe())", 
     "task": "Show descriptive statistics with `print(df.describe())`."},
    {"name": "Basic Data Cleaning - Averages", 
     "desc": "Calculate the mean of numeric columns.", 
     "example": "# Calculate averages\nprint(df.mean(numeric_only=True))", 
     "task": "Display the mean of numeric columns with `print(df.mean(numeric_only=True))`."},
    {"name": "Basic Visualizations - Line Graph", 
     "desc": "Create a line graph with X and Y axes specified in code.", 
     "example": "import matplotlib.pyplot as plt\n\nplt.figure(figsize=(6, 4))\nplt.plot(df['x_col'], df['y_col'])\nplt.xlabel('X Axis')\nplt.ylabel('Y Axis')\nplt.title('Line Graph')\nst.pyplot(plt)", 
     "task": "Plot a line graph with `plt.plot(df['x_col'], df['y_col'])`, label axes, add a title, and display with `st.pyplot(plt)` using columns from your dataset."},
    {"name": "Basic Visualizations - Bar Chart", 
     "desc": "Create a bar chart with X and Y axes specified in code.", 
     "example": "import matplotlib.pyplot as plt\n\nplt.figure(figsize=(6, 4))\nplt.bar(df['x_col'], df['y_col'])\nplt.xlabel('X Axis')\nplt.ylabel('Y Axis')\plt.title('Bar Chart')\nst.pyplot(plt)", 
     "task": "Plot a bar chart with `plt.bar(df['x_col'], df['y_col'])`, label axes, add a title, and display with `st.pyplot(plt)` using columns from your dataset."},
    {"name": "Basic Visualizations - Histogram", 
     "desc": "Visualize the distribution of a numeric column", 
     "example": "import matplotlib.pyplot as plt\nimport numpy as np\n\n# Auto-bin selection using auto mode\nplt.figure(figsize=(6, 4))\nplt.hist(df['numeric_col'], bins='auto', edgecolor='black')\nplt.xlabel('Value')\nplt.ylabel('Frequency')\nplt.title('Histogram')\nst.pyplot(plt)", 
     "task": "Create a histogram with label axes, add a title, and display with `st.pyplot(plt)`."},
    {"name": "Basic Visualizations - Specific Value Charts", 
     "desc": "Create a bar chart for rows matching a specific value in a column.", 
     "example": "import matplotlib.pyplot as plt\n\n# Subset the data\nsubset = df[df['col'] == 'value']\n\n# Create figure and bar chart\nplt.figure(figsize=(6, 4))\nplt.bar(subset['x_col'], subset['y_col'])\nplt.xlabel('x_col')\nplt.ylabel('y_col')\nplt.title('Chart for (specific data)')\nst.pyplot(plt)", 
     "task": "Filter rows where a column equals a specific value (e.g., `df[df['col'] == 'value']`), then plot a bar chart with `plt.bar()` using two columns (e.g., 'x_col' and 'y_col'), label axes, add a title, and display with `st.pyplot(plt)`."},
]

# Sidebar layout
with st.sidebar:
    st.markdown("### 📚 Instructions", unsafe_allow_html=True)
    st.write("**How to Use:**")
    st.write("- Upload a CSV file to begin your journey.")
    st.write("- Select a stage from the dropdown.")
    st.write("- Study the example and task.")
    st.write("- Write code in the editor, adapting column names to your dataset.")
    st.write("- Use `print()` for text output.")
    st.write("- Use `st.pyplot(plt)` for plots.")
    st.write("- Click 'Run Code' to see results.")
    st.markdown("---", unsafe_allow_html=True)

    # Stage selection
    st.markdown("### 🚀 Select a Stage", unsafe_allow_html=True)
    current_stage_idx = st.selectbox(
        "Choose a stage", 
        range(len(stages)), 
        format_func=lambda x: stages[x]["name"], 
        index=st.session_state['current_stage_idx'],
        label_visibility="collapsed"
    )
    st.session_state['current_stage_idx'] = current_stage_idx
    st.markdown("---", unsafe_allow_html=True)

    # Sponsored by section
    st.markdown("### Sponsored by:", unsafe_allow_html=True)
    st.image("cassiecorp.png", width=200)
    st.image("throngler.png", width=200)

# Display stage content in main area
def display_stage(stage_idx):
    stage = stages[stage_idx]
    st.header(stage["name"], anchor=None)
    st.markdown(f"<div class='stMarkdown'>{stage['desc']}</div>", unsafe_allow_html=True)

    st.subheader("Example Code", anchor=None)
    st.code(stage["example"], language="python")

    st.subheader("Your Task", anchor=None)
    st.markdown(f"<div class='stMarkdown'>{stage['task']}</div>", unsafe_allow_html=True)

    # Code editor
    st.write("✍️ Enter your code here:")
    code = st_ace(
        language="python",
        theme="monokai",
        key=f"editor_{stage['name']}",
        height=200,
        show_gutter=True,
        wrap=True,
        value="",
        font_size=14
    )

    # Run button
    if st.button("Run Code", key=f"run_{stage['name']}"):
        if not code or code.strip() == "":
            st.warning("⚠️ Please enter code to run!")
            return

        # Define globals for exec
        globals_dict = {
            'st': st,
            'df': st.session_state['df'],
            'pd': pd,
            'plt': plt,
            'np': np
        }

        # Capture output
        output_io = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = output_io

        try:
            plt.close('all')  # Clear all existing figures
            exec(code, globals_dict)
            sys.stdout = sys_stdout
            output_text = output_io.getvalue()

            if output_text:
                st.subheader("Text Output", anchor=None)
                try:
                    lines = output_text.strip().split('\n')
                    last_output = lines[-1] if lines else ""
                    if ' ' in last_output and any(c.isdigit() for c in last_output):
                        local_vars = {}
                        exec(code, globals_dict, local_vars)
                        for var in local_vars.values():
                            if isinstance(var, (pd.DataFrame, pd.Series)):
                                st.dataframe(var, use_container_width=True)
                                break
                        else:
                            st.code(output_text, language=None)
                    else:
                        st.code(output_text, language=None)
                except Exception:
                    st.code(output_text, language=None)
            else:
                st.info("ℹ️ No text output. Use `print()` to display results.")

            # Display plot if created
            if plt.get_fignums():
                st.subheader("Plot Output", anchor=None)
                fig = plt.gcf()
                fig.set_size_inches(6, 4)
                st.pyplot(fig)
                plt.close(fig)  # Close immediately after display

            st.success("🎉 Code ran successfully!")
            
            # Detailed explanation
            st.markdown("#### What This Code Does:", unsafe_allow_html=True)
            explanation = f"This code executed the task: \"{stage['task']}\"\n\nHere’s what it did:\n"
            
            if "df.shape" in code:
                explanation += "- **Shape**: Showed dimensions of the DataFrame as (rows, columns)."
            elif "df.head()" in code or "df.tail()" in code:
                explanation += "- **Head and Tail**: Displayed the first and/or last 5 rows of the DataFrame."
            elif "df.dtypes" in code:
                explanation += "- **Data Types**: Listed the data type of each column."
            elif "df['" in code and "df[[" not in code:
                explanation += "- **Single Column**: Selected a single column as a Series."
            elif "df[[" in code:
                explanation += "- **Multiple Columns**: Selected multiple columns as a DataFrame."
            elif "df[df[" in code and "'Asia'" not in code:
                explanation += "- **Filtering**: Filtered rows based on a condition."
            elif ".value_counts()" in code:
                explanation += "- **Value Counts**: Counted unique values in a column."
            elif "df.loc[" in code:
                explanation += "- **loc**: Selected data by label."
            elif "df.iloc[" in code:
                explanation += "- **iloc**: Selected data by position."
            elif "df.describe()" in code:
                explanation += "- **Describe**: Generated detailed summary statistics for numeric columns:\n" \
                              "  - **count**: Number of non-null values in each column.\n" \
                              "  - **mean**: Arithmetic average of the values.\n" \
                              "  - **std**: Standard deviation, measuring the spread of data around the mean.\n" \
                              "  - **min**: Smallest value in the column.\n" \
                              "  - **25%**: First quartile (Q1), value below which 25% of the data lies.\n" \
                              "  - **50%**: Median (Q2), middle value splitting the data in half.\n" \
                              "  - **75%**: Third quartile (Q3), value below which 75% of the data lies.\n" \
                              "  - **max**: Largest value in the column."
            elif "df.mean(" in code:
                explanation += "- **Averages**: Calculated means of numeric columns."
            elif "plt.plot(" in code and "label=" in code:
                explanation += "- **Overlay Plot**: Plotted two numeric columns to explore correlations."
            elif "plt.plot(" in code:
                explanation += "- **Line Graph**: Created a line graph with coded X and Y axes."
            elif "plt.bar(" in code and "df[df[" in code:
                explanation += "- **Specific Value Chart**: Filtered rows by a specific value and plotted a bar chart."
            elif "plt.bar(" in code:
                explanation += "- **Bar Chart**: Created a bar chart with coded X and Y axes."
            elif "plt.hist(" in code:
                explanation += "- **Histogram**: Showed the distribution of a numeric column.\n" \
                              "  - **Bins**: The number of intervals or buckets the data is divided into. Each bar’s height shows the frequency (count) of values within that bin’s range."
            elif "df.groupby(" in code:
                explanation += "- **Groupby**: Grouped data and calculated averages."
            elif "IQR" in code or "quantile" in code:
                explanation += "- **Outliers**: Identified and highlighted outliers using the IQR method."

            if "st.pyplot(plt)" in code:
                explanation += "\n- **Display**: Rendered the plot in Streamlit."

            st.markdown(explanation, unsafe_allow_html=True)

        except Exception as e:
            sys.stdout = sys_stdout
            st.error(f"🚨 Error: {e}")
            st.exception(e)
        finally:
            sys.stdout = sys_stdout  # Always restore stdout

# Show the selected stage
display_stage(st.session_state['current_stage_idx'])
