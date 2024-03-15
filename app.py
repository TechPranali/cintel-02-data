from shiny import render
from shiny.express import input, ui
from shinywidgets import render_plotly
import pandas as pd
import plotly.express as px
import seaborn as sns
import palmerpenguins 

penguins_df = palmerpenguins.load_penguins()
ui.page_opts(title="Pranali's Penguin Data", fillable=True)

with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Choose Plotly attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly Bin Number", 40)

    # Number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "seaborn bin Number", 1, 40, 20)

    # Species
    ui.input_checkbox_group(
        "selected_species_list",
        "species",
        ["Gentoo", "Chinstrap", "Adelie"],
        selected=["Gentoo", "Chinstrap"],
        inline=True,
    )

    #horizontal rule to the sidebar
    ui.hr()

    # Use ui.a() to add a hyperlink to the sidebar
    ui.a(
        "Pranali's GitHub Repo",
        href="https://github.com/TechPranali/cintel-02-data",
        target="_blank",
    )

# create a layout to include 2 cards
with ui.layout_columns():
    with ui.card(full_screen=True):  
        ui.h2("Penguin Data Table")

        @render.data_frame
        def penguins_datatable():
            return render.DataTable(penguins_df)

    with ui.card(full_screen=True): 
        ui.h2("Penguin Data Grid")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(penguins_df)


# added a horizontal rule
ui.hr()

# create a layout to include 3 cards with different plots
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.h2("Species Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(
                penguins_df,
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            )

    with ui.card(full_screen=True):
        ui.h2("Seaborn Histogram")

        @render.plot(alt="Species Seaborn Histogram")
        def seaborn_histogram():
            seaborn_plot = sns.histplot(
                data=penguins_df,
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
                multiple="dodge",
                hue="species",
            )
            seaborn_plot.set_title("Species Seaborn Histogram")
            seaborn_plot.set_ylabel("Measurement")

    with ui.card(full_screen=True):
        ui.h2("Species Plotly Scatterplot")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                penguins_df,
                title="Plotly Scatterplot",
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                symbol="species",
            )
