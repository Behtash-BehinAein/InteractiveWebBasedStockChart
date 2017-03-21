# -*- coding: utf-8 -*-
"""
@author: bbehinae
"""
from flask import Flask, render_template
app = Flask(__name__)   # Instantiate the object

@app.route('/Charts/')  
def Daily_Chart():
    from pandas_datareader import data as web
    import datetime
    from bokeh.plotting import figure#, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN


    # Define the time-span of interest via t0 and t1 ------------------------------
    t0=datetime.datetime(2016,11,1)
    t1=datetime.datetime(2017,3,1)
    # Get the data from either Yahoo finance or Google finance --------------------
    #df = web.DataReader('GLD','yahoo',t0,t1)
    df = web.DataReader('GLD','google',t0,t1)


    # C: Close    O: Open
    def Change(C,O):
        if C>O:
            value='UP'
        elif C<O:
            value= 'DN'
        else:
            value= 'EQ'
        return value
    # Change is to classify the UP/DN days
    df['Change'] = [Change(C,O) for C,O in zip(df.Close, df.Open)]
    df['HCenter'] = (df.Open+df.Close)/2
    df['Height'] = abs(df.Open-df.Close)


    # Create the Bokeh figure object and its labels
    f = figure(width=1000,height=300, x_axis_type='datetime', responsive=True)
    #
    f.yaxis.axis_label = 'Price ($)'
    f.yaxis.axis_label_text_font_style = 'normal'
    f.yaxis.axis_label_text_font_size = '18pt'
    #
    f.xaxis.axis_label = 'Time (days)'
    f.xaxis.axis_label_text_font_style = 'normal'
    f.xaxis.axis_label_text_font_size = '18pt'


    # Adjust the figure background and grid line colors
    f.background_fill_color = 'DimGray'
    f.grid.grid_line_color='white'
    f.grid.grid_line_alpha=0.3
    f.xgrid.minor_grid_line_color='white'
    f.grid.grid_line_alpha=0.3
    f.title.text = 'Daily Candlestick Chart of GLD ETF'


    # datetime axis's resolution is in milliseconds
    day_width = 12*3600*1e3
    #  Add glyphs to the figure
    f.segment(df.index[df.Change=='UP'], df.Low[df.Change=='UP'], df.index[df.Change=='UP'], df.High[df.Change=='UP'], color='linen' )
    f.segment(df.index[df.Change=='DN'], df.Low[df.Change=='DN'], df.index[df.Change=='DN'], df.High[df.Change=='DN'], color='darkorange' )
    # -----------------------------------------------------------
    f.rect(df.index[df.Change=='UP'], df.HCenter[df.Change=='UP'],
           day_width, df.Height[df.Change=='UP'],
           fill_color='linen', line_color='linen')
    # -----------------------------------------------------------
    f.rect(df.index[df.Change=='DN'] , df.HCenter[df.Change=='DN'],
           day_width, df.Height[df.Change=='DN'],
           fill_color='darkorange', line_color='darkorange')
    # -------------------------------------------------------------
    components(f)
    script1, div1 = components(f)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template('Daily_Chart.html', 
                           script1=script1, div1=div1,
                           cdn_css=cdn_css,
                           cdn_js=cdn_js)


@app.route('/')   # Homepage for the webpage
def home():
    return render_template('home.html')

@app.route('/Charts/')   # Homepage for the webpage
def Charts():
    return render_template('Charts.html')

if __name__=='__main__':
    app.run(debug=True)
