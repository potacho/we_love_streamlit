import pandas as pd 
import re

# Setup methods

def cat_var(df, cols):
    '''
    Return: a Pandas dataframe object with the following columns:
        - "categorical_variable" => every categorical variable include as an input parameter (string).
        - "number_of_possible_values" => the amount of unique values that can take a given categorical variable (integer).
        - "values" => a list with the posible unique values for every categorical variable (list).

    Input parameters:
        - df -> Pandas dataframe object: a dataframe with categorical variables.
        - cols -> list object: a list with the name (string) of every categorical variable to analyse.
    '''
    cat_list = []
    for col in cols:
        cat = df[col].unique()
        cat_num = len(cat)
        cat_dict = {"categorical_variable":col,
                    "number_of_possible_values":cat_num,
                    "values":cat}
        cat_list.append(cat_dict)
    df = pd.DataFrame(cat_list).sort_values(by="number_of_possible_values", ascending=False)
    return df.reset_index(drop=True)

def cause_types(cause):
    '''
    Return: a string indicating whether the death cause is single or a compound of many single causes.
        
    Input parameters:
        - df -> string: a string with the information about the death cause (e.g.: '001-102 I-XXII.Todas las causas').
    '''
    pattern = '\d+-\d+'
    x = re.findall(pattern, cause)
    if len(x) == 0:
        return 'Single cause'
    else:
        return 'Multiple causes'

def cause_code(text):
    '''
    Return: a string with the code of a give death cause (e.g.: '001-102').
        
    Input parameters:
        - df -> string: a string with the information about the death cause (e.g.: '001-102 I-XXII.Todas las causas').
    '''
    return text.split(" ", 1)[0]

def cause_name(text):
    '''
    Return: a string with the name of a give death cause  (e.g.: 'I-XXII.Todas las causas').
        
    Input parameters:
        - df -> string: a string with the information about the death cause (e.g.: '001-102 I-XXII.Todas las causas').
    '''
    return text.split(" ", 1)[1].strip()


# Transformation methods

def row_filter(df, cat_var, cat_values):
    '''
    Return: a Pandas dataframe object where columns have been filtered by a set of values from a given column (categorical variable). 
            The resulting dataframe will be sorted descending from highest to lowest amount of deaths and the index column will be reset.

    Input parameters:
        - df -> Pandas dataframe object: a dataframe with categorical variables.
        - cat_var -> string: a string with the name of a categorical variable (e.g.: 'Sexo').
        - cat_values -> list object: a list of values (string) which rows will be INCLUDED into the returned dataframe (e.g.: ['Hombres', 'Mujeres'])
    '''
    df = df[df[cat_var].isin(cat_values)].sort_values(by='Total', ascending=False)
    return df.reset_index(drop=True)

def nrow_filter(df, cat_var, cat_values):
    '''
    Return: a Pandas dataframe object where columns have been filtered by a set of values from a given column (categorical variable). 
            The resulting dataframe will be sorted descending from highest to lowest amount of deaths and the index column will be reset.

    Input parameters:
        - df -> Pandas dataframe object: a dataframe with categorical variables.
        - cat_var -> string: a string with the name of a categorical variable (e.g.: 'Sexo').
        - cat_values -> list object: a list of values (string) which rows will be EXCLUDED into the returned dataframe (e.g.: ['Hombres', 'Mujeres'])
    '''
    df = df[~df[cat_var].isin(cat_values)].sort_values(by='Total', ascending=False)
    return df.reset_index(drop=True)

def groupby_sum(df, group_vars, agg_var='Total', sort_var='Total'):
    '''
    Return: a Pandas dataframe object where rows have been gruped by a given group of columns (categorical variables). 
            The resulting dataframe will be sorted descending from highest to lowest amount of deaths and the index column will be reset.

    Input parameters:
        - df -> Pandas dataframe object: a dataframe with categorical variables and an aggregation variable.
        - group_vars -> list object: a list of values with the name of a group of categorical variables (e.g.: ['Sexo', 'Edad']).
        - agg_var -> string: a string with the name of the variable to be aggregated. In this case the variable 'Total' (number of deaths) is set as default.
        - sort_var -> string: a string with the name of the variable to sort the dataframe by. In this case the variable 'Total' (number of deaths) is set as default.
    '''
    df = df.groupby(group_vars, as_index=False).agg({agg_var:'sum'})
    df = df.sort_values(by=sort_var, ascending=False)
    return df.reset_index(drop=True)

def pivot_table(df, col, x_axis, value='Total'):
    '''
    Return: a Pandas dataframe object where categorical variable values have been pivoted. 
            The resulting dataframe index column will be reset.

    Input parameters:
        - df -> Pandas dataframe object: a dataframe with categorical variables and an aggregation variable.
        - col -> string: a string with the name of a categorical variable to be pivoted (e.g.: 'cause_code').
        - x_axis -> string: a string with the name of a categorical variable to represent the x-axis (e.g.: 'Periodo').
        - value -> string: string: a string with the name of the variable to be aggregated. In this case the variable 'Total' (number of deaths) is set as default.
    '''
    df = df.pivot_table(values=value,
                        columns=col,
                        index=x_axis,
                        aggfunc='sum')
    return df.reset_index()