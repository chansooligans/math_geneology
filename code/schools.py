# general functions for school network analysis

import pandas as pd
import numpy as np
import networkx as nx


def check_cols(df):
    """
    return rows that have certain columns populated
    """
    cols = ['advisor_year','student_year','advisor_school','student_school']
    for col in cols:
        df = df.loc[df[col].notnull() & (df[col] != ' '),:]
    return df
        

def clean_school_names(df):
    """
    remove extra spaces in school names
    """
    for col in ['student_school','advisor_school']:
        df[col] = [x.strip() for x in df[col]]    
    return df


def try_to_int(x):
    """
    try converting x to int, if raises exception then return -1
    """
    try:
        conv = int(x)
    except:
        conv = -1
    finally:
        return conv


def fix_years(chars, cols):
    """
    spilt multiple years and convert to int
    """
    def _(df):
        for c in chars:
            for col in cols:
                df[col] = df[col].astype(str).str.split(c).map(lambda x: x[0]).map(try_to_int).astype(int)
        return df
    return _
                        
def add_decade(year_cols):
    """
    add decade for year cols
    """
    def _(df):
        for col in year_cols:
            df[col + "_dec"] = df[col].map(lambda x: str(int(np.floor(x / 10) * 10)) + "s")
        return df
    return _
    

def get_all_students():
    """
    grab all student data
    includes cleaning
    """
    df = pd.read_csv("../data/math_geneology_final.csv").fillna(" ")
    for clean_func in [
        check_cols,
        clean_school_names,
        fix_years(
            chars = [',','/',' ','-'],
            cols = ["advisor_year", "student_year"]),
        add_decade(year_cols = ["advisor_year", "student_year"])]:
        df = clean_func(df)
    return df

def make_school_digraph(student_df):
    """
    make a schools digraph from student data
    """
    schools_df = pd.concat([student_df[[c]].rename(columns = {c: "school"}) for c in ["student_school", "advisor_school"]]).drop_duplicates()
    
    school_digraph = nx.DiGraph()
    # Nodes are schools (student and advisors) identified by name
    school_digraph.add_nodes_from(schools_df.school.values)
    
    # Edges connect advisor and student schools and are weighted by the number of advisor-students
    edges_df = student_df.groupby(["student_school", "advisor_school"], as_index = False).agg({"student_id": "count"})
    edges = [(e["advisor_school"], e["student_school"], {"weight": e["student_id"]}) for e in edges_df.to_dict(orient = "records")]
    school_digraph.add_edges_from(edges)
    return school_digraph


def draw_graph_layout(graph, layout, ax):
    """
    draw the graph with the given layout on the given axis
    """
    ax.scatter([v[0] for k, v in layout.items()], [v[1] for k, v in layout.items()], s = 2)
    for e in [e for e in graph.edges]:
        ax.plot([layout[i][0] for i in e], [layout[i][1] for i in e], c = "steelblue", lw = 0.1)