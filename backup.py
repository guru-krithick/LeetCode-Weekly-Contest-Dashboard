import streamlit as st
import pandas as pd
import plotly.express as px
from background import BackgroundCSSGenerator
# Load data

st.session_state.data = pd.read_csv('data.csv')
data = st.session_state.data

st.set_page_config(layout="wide")
st.session_state.filtered = data

# Define unique values for filters
departments = ["All"] + list(st.session_state.data['Department'].unique())
years = ["All"] + list(st.session_state.data['Year'].unique())
domains = ["All"] + list(st.session_state.data['Domain'].unique())

# Sidebar layout
st.sidebar.header("Filter Data")
dept_val = st.session_state.get('department')
department = st.session_state.department = st.sidebar.selectbox('Department', departments, index=0 if not dept_val else departments.index(dept_val))

year_val = st.session_state.get('year')
year = st.session_state.year = st.sidebar.selectbox('Year', years, index=0 if not year_val else years.index(year_val))

domain_val = st.session_state.get('domain')
domain = st.session_state.domain = st.sidebar.selectbox('Domain', domains, index=0 if not domain_val else domains.index(domain_val))

# background_generator = BackgroundCSSGenerator()
# page_bg_img = background_generator.generate_background_css()
# st.markdown(page_bg_img, unsafe_allow_html=True)

# Filter data based on selections
filtered_data = st.session_state.filtered
if year != 'All':
    filtered_data = filtered_data[filtered_data['Year'] == year]
if department != 'All':
    filtered_data = filtered_data[filtered_data['Department'] == department]
if domain != 'All':
    filtered_data = filtered_data[filtered_data['Domain'] == domain]

# Main content layout
st.title("LeetCode Weekly Contest Analysis:")


filtered_data_rank_not_zero = filtered_data[filtered_data['Rank'] != 0]



col1,col2 = st.columns([1,1])
domain_counts = filtered_data['Domain'].value_counts()

with col2:
    coooo1,coooo2,coooo3,coooo4 = st.columns([1,1,1,1])
    with coooo1:
# Problems Solved Count
        problem_counts = range(5)  # Assuming max problems solved can be 4
        problems_count = filtered_data_rank_not_zero['ProbCount'].value_counts()
        problem_data = pd.DataFrame({'Problems': problem_counts,
                                    'Count': [problems_count.get(count, 0) for count in problem_counts]})

        # Create the bar chart
        fig_problems = px.bar(problem_data, x='Problems', y='Count', color='Problems')  # Assigning colors based on x-axis values
        fig_problems.update_layout(title_text="Problems Solved")

# Display the chart
        st.plotly_chart(fig_problems)
        # Calculate the count of participants who solved each specific number of problems
        problem_0_count = sum(filtered_data_rank_not_zero['ProbCount'] == 0)
        problem_1_count = sum(filtered_data_rank_not_zero['ProbCount'] == 1)
        problem_2_count = sum(filtered_data_rank_not_zero['ProbCount'] == 2)
        problem_3_count = sum(filtered_data_rank_not_zero['ProbCount'] == 3)
        problem_4_count = sum(filtered_data_rank_not_zero['ProbCount'] == 4)
    with coooo2:
        st.write("")

    with coooo3:
        st.write("")

    with coooo4:
        # Display total problems solved metric
        st.metric("Total Problems Solved", sum(problem_data['Count']))

 
        st.metric("Problem 0 Solved", problem_0_count)

        st.metric("Problem 1 Solved", problem_1_count)

        st.metric("Problem 2 Solved", problem_2_count)
          
        st.metric("Problem 3 Solved", problem_3_count)

        st.metric("Problem 4 Solved", problem_4_count)

    

    
        
with col1:

    cde1,cde2,cde3,cde4 = st.columns([1,1,1,1])
    with cde1:
        rank_presence = filtered_data['Rank'].apply(lambda x: 'Absent' if x == 0 else 'Present')
        presence_data = pd.DataFrame({'Presence': rank_presence.value_counts().index,
                                    'Count': rank_presence.value_counts().values})
        colors = ['green', 'red']
        fig_presence = px.pie(presence_data, values='Count', names='Presence', 
                            color_discrete_sequence=colors)
        fig_presence.update_layout(legend=dict(title='Presence', orientation='h', x=0.8, y=0.7)) 
        fig_presence.update_layout(title_text="Presence Distribution")

        # Display the chart
        st.plotly_chart(fig_presence)

    with cde2:

        st.write("")

    with cde3:
        st.write("")
    
    
    with cde4:
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        st.metric("Total Students", sum(domain_counts))
        st.metric("Total Present", presence_data[presence_data['Presence'] == 'Present']['Count'].values[0])  
        st.metric("Total Absent", presence_data[presence_data['Presence'] == 'Absent']['Count'].values[0])
        
# Department-wise Distribution of Participants
        


colf1 , colf2 = st.columns([1,1])

with colf2:
    filtered_no_zero = filtered_data[filtered_data['Rank'] > 0]
    sorted_filtered = filtered_no_zero.sort_values(by='Rank').head(10)
    sorted_filtered = sorted_filtered.sort_values(by='Rank', ascending=True)  # Sort by Rank ascending for better visualization

    sorted_filtered = sorted_filtered[::-1]

    # Add a new column 'Rank_Label' to represent the rank label for each name
    # Create a list of strings with names and their corresponding ranks in brackets
    names_with_ranks = [f"{name} ({len(sorted_filtered) - rank}{'th' if (len(sorted_filtered) - rank) % 10 == 0 or (len(sorted_filtered) - rank) % 10 >= 4 or 10 < (len(sorted_filtered) - rank) % 100 < 20 else ['st', 'nd', 'rd'][(len(sorted_filtered) - rank) % 10 - 1]} Rank)" for rank, name in enumerate(sorted_filtered['Name'][::-1])]

    # Update the y-axis with the modified list
    fig_top_performers = px.bar(sorted_filtered, y=names_with_ranks, x='Rank', 
                                hover_data=['Year', 'Domain', 'Department', 'Score', 'ProbCount'],
                                labels={'Rank': 'Ranking'},
                                color='Rank',
                                color_continuous_scale='viridis',
                                title='Top 10 Performers (Intra College Ranking)',
                                orientation='h')
    fig_top_performers.update_layout(xaxis_title='Ranking Score', yaxis_title='Name')
    st.plotly_chart(fig_top_performers)
    
    
with colf1:
    coq1,coq2,coq3,coq4 = st.columns([1,1,1,1])
    with coq1:

        # Rank Distribution by Range
        bins = [0, 5000, 10000, 15000, 20000, 25000, 30000]
        bin_labels = ['0-5000', '5000-10000', '10000-15000', '15000-20000', '20000-25000', '25000-30000']

        categories = pd.cut(filtered_data_rank_not_zero['Rank'], bins=bins, labels=bin_labels, ordered=True)
        rank_counts = categories.value_counts().reindex(bin_labels, fill_value=0)  # Reindex to ensure correct order
        rank_data = pd.DataFrame({'Rank Range': rank_counts.index, 'Count': rank_counts.values})

        # Create the bar chart
        fig_rank = px.bar(rank_data, x='Rank Range', y='Count', color='Rank Range')  # Assigning colors based on x-axis values
        fig_rank.update_layout(title_text="Rank Range Distribution")

        # Display the chart
        st.plotly_chart(fig_rank)
    with coq2:
        st.write("")
    
    with coq3:
        st.write("")

    with coq4:

    #st.subheader("Rank Range:")rank_data.iloc[0]['Rank Range'], rank_data.iloc[0]['Count']


        st.metric(rank_data.iloc[0]['Rank Range'], rank_data.iloc[0]['Count'])

        st.metric(rank_data.iloc[1]['Rank Range'], rank_data.iloc[1]['Count'])

        st.metric(rank_data.iloc[2]['Rank Range'], rank_data.iloc[2]['Count'])

        st.metric(rank_data.iloc[3]['Rank Range'], rank_data.iloc[3]['Count'])

        st.metric(rank_data.iloc[4]['Rank Range'], rank_data.iloc[4]['Count'])

        st.metric(rank_data.iloc[5]['Rank Range'], rank_data.iloc[5]['Count'])
   

